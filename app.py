from flask import Flask, render_template, request, session, jsonify, redirect, url_for, flash
from bloodline_skills import BLOODLINE_SKILLS
import re
import os
import constants
import exceptions as exc
from prebuilts import PREBUILTS
import Skills
import skills_db
from skills_db import SKILL_REF, construct_skill_ref
from Skills import Construct_Skill
import twin_maskify as tm
from session_manager import (
    reset_skills,
    reset_session,
    reset_skill_selections,
    back_to_the_death_realms_with_you,
    inject_bloodline_skills,
    Update_Points,
)
from character_builder import create_char

try:
    app
except NameError:
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")

def construct_display_dict(character): 
    display_dict = {}
    skill_dict = character.skills_added.copy()
    flags=constants.FLAGS
    for flag in flags:
        try:
            del skill_dict[flag]
        except KeyError:
            pass
    for skill in skill_dict:
        input = Skills.SkillChangeInput({'skill': skill, 'quantity': skill_dict[skill]})
        character = tm.Character.from_session(session)
        try:
            skill_ = Construct_Skill(input, character)
        except exc.Skill_Not_Exist:
            continue
        skill_.construct_display_name()
        display_dict[skill_.display_name] = skill_.display_quant

    if 'Weapon Master' in display_dict:
        for weapon in constants.WEAPON_MASTER_SKILLS:
            if weapon in display_dict:
                del display_dict[weapon]

    return display_dict

@app.route("/")
def buttons():
    return render_template('load_character_sheet.html')

def contains_google_doc_link(text):
    LINK_REGEX = re.compile(r"(https?://[^\s]+|www\.[^\s]+)", re.IGNORECASE)
    return bool(re.search(LINK_REGEX, text))

@app.context_processor
def inject_globals():
    if 'Toughness' in session['skills_added']:
        session['character_details']['health points']=5+session['skills_added']['Toughness']
    else:
        session['character_details']['health points']=5
    character = tm.Character.from_session(session)
    display_dict = construct_display_dict(character)

    char_dict=dict(session['character_details'])
    flags=['points','flaw_points','memory_flaws','health points','flaws_added']
    for flag in flags:
        try:
            del char_dict[flag]
        except KeyError:
            continue

    try:
        player_details=session['person_details']
    except KeyError:
        player_details={}

    return {
        'gathering': session.get('gathering', 0),
        "points": session.get("character_details", {}).get("points", 0), 
        'display_dict': display_dict,
        'char_dict': char_dict,
        'HP': session.get("character_details", {}).get("health points", 5),
        'name': session.get("character_details", {}).get("name", 'no name selected'),
        'culture': session.get("character_details", {}).get("culture", 'no culture selected'),
        'bloodline': session.get("character_details", {}).get("bloodline", 'no bloodline selected'),
        'faith': session.get("character_details", {}).get("faith", 'no faith selected'),
        'player_info': player_details
    }

@app.before_request
def init_session():
    for cat in constants.DEFAULT_SESSION:
        if cat not in session:
            session[cat]=constants.DEFAULT_SESSION[cat].copy()
    
    session.modified=True

@app.route("/new_player_landing")
def new_player_landing():
    session['character_type'] = 'new_character'
    session.modified = True
    return render_template('set_character.html')

@app.route("/submit")
def submit_page():

    character = tm.Character.from_session(session)

    display_dict = construct_display_dict(character)

    char_ref=dict(session['character_details'])

    char_dict={'name':char_ref['name'],'Culture':char_ref['culture'],'bloodline':char_ref['bloodline'],'faith':char_ref['faith'],'HP':char_ref['health points']}

    player_ref=session['person_details']

    player_details={'name':player_ref['name'],'email':player_ref['email'],'discord':player_ref['discord']}

    try:
        backstory=session['character_details']['backstory']
    except KeyError:
        backstory='No backstory submitted...'

    return render_template(
    "submit_character.html",
    player_info=player_details,
    char_info=char_dict,
    skill_info=display_dict,
    char_backstory=backstory)

@app.errorhandler(exc.MissingBackstory)
def handle_missing_backstory(e):
    return {
        "success": False,
        "error": "MISSING_BACKSTORY",
        "message": "Backstory is required before submission."
    }, 400

@app.errorhandler(exc.Too_Many_Points)
def handle_missing_backstory(e):
    return {
        "success": False,
        "error": "Too Many Points",
        "message": "You have spent more points than allowed. Please remove a skill and/or add a flaw."
    }, 400

@app.errorhandler(exc.Backstory_Is_Link)
def handle_missing_backstory(e):
    return jsonify({
        "success": False,
        "error": "NO LINKS",
        "message": "NO LINKS!!!"
    }), 400

@app.errorhandler(exc.ReliantSkills)
def handle_reliant_skills(e):
    return jsonify({'success':False,'error':'Reliant skill must be removed', 'message':'slimmery'}), 400

@app.errorhandler(exc.MissingBackstory)
def handle_missing_backstory(e):
    return {
        "success": False,
        "error": "MISSING_BACKSTORY",
        "message": "Backstory is required before submission."
    }, 400

@app.errorhandler(exc.UnspentPoints)
def handle_missing_backstory(e):
    return {
        "success": False,
        "error": "UNSPENT_POINTS",
        "message": "Warning- you have unspent points.\n\nSubmit your character if you are okay with this."
    }, 400

@app.route('/submission_placeholder')
def submission_placeholder():
    return render_template('submission_placeholder.html')

@app.route("/alt_char_landing")
def alt_char_landing():
    return render_template('enter_sheet_id.html')

@app.route("/show_prebuilts")
def show_prebuilts():

    reset_skill_selections()

    session.modified=True

    return render_template(
        "select_premade.html",
        PREBUILTS=PREBUILTS
    )

@app.route("/make_choice")
def custom_or_prebuilt():
    
    if session['character_details']['bloodline'].lower() in ['human', 'effendal']:
        return render_template('premade_or_custom.html')
    else: 
        return maliks_idea()

@app.route("/add_gathering_row", methods=["POST"])
def add_gathering_row():
    # Table as it currently exists in the HTML, sent from the client
    incoming_table = request.get_json(silent=True) or []

    last_gathering_row = incoming_table[-1]


    if last_gathering_row[4]:
        food_tag = 1
    else:
        food_tag = 0

    last_gathering = tm.Gathering(last_gathering_row[0],last_gathering_row[1],last_gathering_row[2],
                                  last_gathering_row[3],food_tag,last_gathering_row[5])
    last_gathering.sum_CP()
 
    if incoming_table:
        next_gathering = int(incoming_table[-1][0]) + 1
    else:
        next_gathering = 1
 
    new_row = [
        next_gathering,  
        "",              
        3,               
        0,               
        False,           
        last_gathering.new_cp         
    ]
 
    incoming_table.append(new_row)

    session['gatherings_skills'][str(next_gathering)] = session['gatherings_skills'][str(next_gathering-1)].copy()

    session["gatherings_table"] = incoming_table
    session.modified = True

 
    return jsonify(new_row)

@app.route('/remove_gathering_row', methods=['POST'])
def remove_gathering_row():
    data = request.get_json()
    index = data.get("index")
    table = data.get("table", [])
    removing_gat = data['table'][index][0]

    if index is None or not (0 <= index < len(table)):
        return jsonify({"error": "Invalid index"}), 400

    table = table[:index]

    for gat in session['gatherings_skills'].copy():
        if int(gat) >= int(removing_gat):
            del session['gatherings_skills'][gat]

    session['gatherings_table'] = table
    return jsonify({"success": True})

@app.route("/create_character")
def create_character():
    return render_template('landing_page.html')

@app.route("/submit_gathering_row", methods=["POST"])
def submit_gathering_row():
    row_data = request.get_json()

    gathering = tm.Gathering(
        row_data['gathering'],
        row_data['date'],
        row_data['cp_earned'],
        row_data['ip_converted'],
        row_data['food_tag'],
        row_data['total_cp']
    )

    global session

    session['character_details']['points'] = gathering.total_cp

    session['character_details']['base_points'] = gathering.total_cp

    Update_Points()

    session = substitute_gathering(session['gatherings_skills'], row_data['gathering'])

    session.modified = True

    Update_Points()

    return redirect(url_for('planning_skills'))

def substitute_gathering(skills_ref, gathering):
    session['gathering'] = gathering
    session['skills_added'] = skills_ref[gathering].copy()
    return session

@app.route("/planning_skills", methods=["GET"])
def planning_skills():
    skills_db_dict = construct_skill_ref()

    utilities = ['SKILL REF', 'BLOODLINE SKILLS']
    for ut in utilities:
        del skills_db_dict[ut]

    skills_db_dict = inject_bloodline_skills(session, skills_db_dict)

    return render_template(
        'planning_skills.html',
        skills_db=skills_db_dict,
        back_url=url_for("character_setup"),
        modify_route=url_for("modify_skill"),
        increase_route = url_for('increase_skill')
    )

@app.route("/increase_skill", methods=["POST"])
def increase_skill():
    data = request.get_json(silent=True) or {}
 
    delta = data['quantity'] - session['skills_added'][data['skill']]
 
    input={'skill':data['skill'], 'quantity':delta}
    input = tm.SkillChangeInput(input)
    character = tm.Character.from_session(session)
    skill = Construct_Skill(input, character)
 
    if delta>0:
        try:
            skill.add()
        except exc.Max_Points_Spent:
            return jsonify({"success": False, "error": f"You do not have enough points."})
    else:
        skill_check = session['skills_added'].copy()
        skill_check[data['skill']] = session['skills_added'][data['skill']]-abs(delta)
        for skill in skill_check:
            if skill in constants.FLAGS:
                continue
            input={'skill':skill, 'quantity':skill_check[skill]}
            input = tm.SkillChangeInput(input)
            character = tm.Character.from_session(session)
            skill_ = Construct_Skill(input, character)
            if hasattr(skill_,'prereqs') and skill_.prereqs is not None:
                for prereq in skill_.prereqs:
                    if skill_.prereqs[prereq] > skill_check[prereq]:
                        return jsonify({'success':False, "error": f"You must first remove {skill}"})

 
    session['skills_added'][data['skill']] = data['quantity']
 
    Update_Points()
 
    return {
            'success': True,
            "message": "Added Skill",
            "points": session["character_details"]["points"],
            "HP": session["character_details"]["health points"],
            "name": session["character_details"].get("name", "no name selected"),
            "culture": session["character_details"].get("culture", "no culture selected"),
            "bloodline": session["character_details"].get("bloodline", "no bloodline selected"),
            "faith": session["character_details"].get("faith", "no faith selected"),
        }

@app.route("/gatherings_table", methods=["GET"])
def gatherings_table():
    for gat in session['gatherings_skills']:
        if int(gat) >= int(session['gathering']):
            for key, value in session['skills_added'].items():
                if key not in session['gatherings_skills'][gat] or value > session['gatherings_skills'][gat][key]:
                    session['gatherings_skills'][gat][key] = value
    session['gatherings_skills'][session['gathering']] = session['skills_added'].copy()
    session.modified = True
    next_gathering_num = str(session['gatherings_table'][1][0])
    if next_gathering_num not in session['gatherings_skills']:
        session['gatherings_skills'][next_gathering_num] = session['skills_added'].copy()
    if session['character_details']['faith'] == 'Total CP:':
        session['character_details']['faith'] = 'None'
        session.updated = True
    return render_template("gatherings_table.html")

@app.route("/select_prebuilt", methods=["POST"])
def select_prebuilt():
    # there's some oddity going on in here. Azzy thinks she fixed it. We will see.
    #Azzy the health points calculation is broken. Fix!!!
    # oh also charisx   ic courtier is throwing a key error. fix it azzy! Fixed- Azzy

    reset_skill_selections()

    Update_Points()

    data = request.get_json()

    prebuilt = data.get("prebuilt")

    session['skills_added'][f'Native Lore: {session['character_details']['culture']}']=1
    try:
        session['skills_added'][f'Native Lore: {session['character_details']['second_culture']}']=1
    except KeyError:
        pass

    for skill in PREBUILTS[prebuilt]['skills']:
        input={'skill':skill, 'quantity':PREBUILTS[prebuilt]['skills'][skill]}
        input = tm.SkillChangeInput(input)
        character = tm.Character.from_session(session)
        skill_=Construct_Skill(input, character)

        if hasattr(skill_, "flags") and skill_.flags is not None:
            skill_.flag_modifier = 1 
            skill_.modify_flags(character.skills_added)
        
        if isinstance(skill_, Skills.Memory_Flaw):
            session['skills_added']['memory_flaws']=1
            session['character_details']['flaws_added'].append(skill)

        elif isinstance(skill_, Skills.Background_Flaw):
            session['character_details']['flaws_added'].append(skill)

        session['skills_added'][skill]=PREBUILTS[prebuilt]['skills'][skill]

    return "", 204

@app.route('/start_planning')
def start_plan():
    return render_template('load_character_sheet.html')

@app.route('/skill_plan')
def skill_plan():
    skills_db_dict = construct_skill_ref()

    utilities = ['SKILL REF','BLOODLINE SKILLS']

    for ut in utilities:
        del skills_db_dict[ut]

    skills_db_dict=inject_bloodline_skills(session,skills_db_dict)

    if session['character_details']['faith'] == 'Total CP:':
        session['character_details']['faith'] = 'None'
        session.updated = True

    return render_template('planning_skills.html', skills_db=skills_db_dict,back_url=url_for("character_setup"))

@app.route('/plan_skills')
def plan_skills():
    skills_db_dict = construct_skill_ref()

    utilities = ['SKILL REF','BLOODLINE SKILLS']

    for ut in utilities:
        del skills_db_dict[ut]

    skills_db_dict=inject_bloodline_skills(session,skills_db_dict)

    Update_Points()

    if session['character_details']['faith'] == 'Total CP:':
        session['character_details']['faith'] = 'None'
        session.updated = True

    return render_template('planning_skills.html', skills_db=skills_db_dict,back_url=url_for("character_setup"))

@app.route("/skills_display")
def skills_display():
    return render_template('skills_display.html')

@app.route("/start_respec", methods=["GET"])
def start_respec():
    session['character_type']='respec'
    session.modified = True
    return render_template("start_respec.html") 

@app.route('/add_replacement', methods=['POST'])
def add_replacement():
    data = request.get_json()

    session['unrecognizeds'][session['unrecognized']] = f'{data['skill']} x{data['quantity']}'

    session['original_skills'][data['skill']] = data['quantity']

    return jsonify(
        success=True,
        redirect=url_for("insert_unrecognizeds")
    )   

@app.route("/replace_unrecognized", methods=["POST"])
def replace_unrecognized():
    session['unrecognized'] = request.form["unrecognized"]
    skills_db_dict = construct_skill_ref()

    utilities = ['SKILL REF','BLOODLINE SKILLS']

    for ut in utilities:
        del skills_db_dict[ut]

    skills_db_dict=inject_bloodline_skills(session,skills_db_dict)
    return render_template('replace_skills.html', modify_route=url_for("add_replacement"), skills_db=skills_db_dict,back_url=url_for("character_setup"))

@app.route("/submit_substitutions", methods=["POST"])
def submit_substitutions():
    for skill in session['unrecognizeds']:
        entry = session['unrecognizeds'][skill]
        entry = entry.split('x')
        session['skills_added'][entry[0].strip()] = entry[1]
    Update_Points()
    session.modified = True
    return gatherings_table()

@app.route('/insert_unrecognizeds')
def insert_unrecognizeds():
    return render_template('unrecognizeds.html')

@app.route('/load_existing_character')
def load_existing_character():
    unrecognized = {}

    sheet_url = request.args.get('sheet_url')

    if not sheet_url:
        return "Missing sheet_url parameter", 400

    details = sheet_creator.character_sheet_to_dict(sheet_url)

    session.clear()

    for cat in constants.DEFAULT_SESSION:
        session[cat] = constants.DEFAULT_SESSION[cat].copy()

    session['character_type'] = 'character_plan'

    for cat in details:
        session[cat] = details[cat]

    for flag in constants.DEFAULT_SESSION['skills_added']:
        if flag not in session['skills_added']:
            session['skills_added'][flag] = constants.DEFAULT_SESSION['skills_added'][flag]

    for skill in session['skills_added'].copy():
        if skill in constants.DEFAULT_SESSION['skills_added']:
            continue

        input = Skills.SkillChangeInput({'skill': skill, 'quantity': session['skills_added'][skill]})
        character = tm.Character.from_session(session)
        if ' (' in skill:
            skill = skill.split(' (',1)
            input.name = skill[0]
        try:
            skill_ = Construct_Skill(input, character)
        except exc.Skill_Not_Exist:
            unrecognized[skill] = ''
        if hasattr(skill_,'flags'):
            skill_.flag_modifier = 1
            skill_.modify_flags(session['skills_added'])

    session['first_gat'] = session['gathering']

    for sk in unrecognized.copy():
        if sk[:2] == 'R.':
            session['skills_added'][sk] = 1
            del unrecognized[sk]

    if unrecognized != {}:
        session['unrecognizeds'] = unrecognized
        session.modified = True
        session['original_skills'] = session['skills_added'].copy()
        session['gatherings_skills'][session['gathering']] = session['skills_added'].copy()
        return insert_unrecognizeds()
    
    session['original_skills'] = session['skills_added'].copy()
    
    session['gatherings_skills'][session['gathering']] = session['skills_added'].copy()

    return gatherings_table()

@app.route('/confirm_submission', methods=['POST'])
def confirm_submission():
    #sheet_creator.export_char(session)

    if session['character_details']['points']<0:
        raise exc.Too_Many_Points()

    try:
        backstory=session['character_details']['backstory']
    except KeyError:
        raise exc.MissingBackstory()

    points=session['character_details']['points']

    if points>0 and session['flags']['points_warning_given'] is False:
        session['flags']['points_warning_given']=True
        session.modified=True
        raise exc.UnspentPoints()
    
    return render_template("submission_placeholder.html")

@app.route("/character_setup", methods=["GET"])
def character_setup():
    return render_template("character_setup.html")

@app.route("/all_skills")
def maliks_idea():
    skills_db_dict = construct_skill_ref()

    utilities = ['SKILL REF','BLOODLINE SKILLS']

    for ut in utilities:
        del skills_db_dict[ut]

    skills_db_dict=inject_bloodline_skills(session,skills_db_dict)

    Update_Points()

    return render_template('all_skills.html', modify_route=url_for("modify_skill"), skills_db=skills_db_dict,back_url=url_for("character_setup"))

@app.route('/premade_or_custom')
def premade_or_custom():
    return render_template('premade_or_custom.html')

@app.route('/submission_test', methods=['POST'])
def new_player():
    session['skills_added'] = constants.DEFAULT_SESSION['skills_added'].copy()
    session.modified = True  

    data = request.get_json()
    create_char(data)

    return ('', 204)

@app.route("/set_character/<category>")
def set_character(category):
    return render_template("set_character.html", category=category)

@app.route("/planning_reset", methods=["POST"])
def planning_reset():
    skills_db_dict = construct_skill_ref()

    utilities = ['SKILL REF', 'BLOODLINE SKILLS']
    for ut in utilities:
        del skills_db_dict[ut]

    skills_db_dict = inject_bloodline_skills(session, skills_db_dict)
    session['skills_added'] = session['original_skills'].copy()
    for gat in session['gatherings_skills' ]:
        session['gatherings_skills'][gat] = session['skills_added'].copy()
    return render_template(
        'planning_skills.html',
        skills_db=skills_db_dict,
        back_url=url_for("character_setup"),
        modify_route=url_for("modify_skill"),
        increase_route = url_for('increase_skill')
    )

@app.route("/reset_plan", methods=["POST"])
def reset_plan():
    skills_db_dict = construct_skill_ref()

    utilities = ['SKILL REF', 'BLOODLINE SKILLS']
    for ut in utilities:
        del skills_db_dict[ut]

    skills_db_dict = inject_bloodline_skills(session, skills_db_dict)
    second_gat = str(int(session['first_gat'])+1)
    session['skills_added'] = session['original_skills'].copy()
    for gat in session['gatherings_skills'].copy():
        if int(gat) > int(second_gat):
            del session['gatherings_skills'][gat]
    session['gatherings_table'] = session['gatherings_table'][:2]
    session['gatherings_skills'][second_gat] = session['skills_added'].copy()
    return render_template(
        'gatherings_table.html'
    )

@app.route("/submit_character", methods=["POST"])
def submit_character():

    return "",204

@app.route("/skills/<category>")
def skills_page(category):
    all_skills={
        'features':skills_db.BACKGROUND_FEATURES,
        'flaws':skills_db.BACKGROUND_FLAWS,
        "weapon":skills_db.WEAPON_PROFICIENCIES,
        "armor":skills_db.ARMOR_PROFICIENCIES,
        "general":skills_db.GENERAL_COMBAT_SKILLS,
        "archery":skills_db.ARCHERY,
        "officer_training":skills_db.OFFICER_TRAINING,
        'the_art_of_dueling':skills_db.THE_ART_OF_DUELING,
        'the_school_of_suffering':skills_db.THE_SCHOOL_OF_SUFFERING,
        'the_assasins_art':skills_db.THE_ASSASSINS_ARTS,
        'berserker':skills_db.THE_HONOURED_PATH_OF_THE_BERSERKER,
        'mundane_healing':skills_db.MUNDANE_HEALING,
        'religious_worship':skills_db.RELIGIOUS_WORSHIP,
        'bardic_arts':skills_db.THE_BARDIC_ARTS,
        'magical_arts':skills_db.MAGICAL_ARTS,
        'skullduggery':skills_db.SKULLDUGGERY,
        'knowledge':skills_db.KNOWLEDGE,
        'gathering':skills_db.GATHERING,
        'crafting_skills':skills_db.CRAFTING_SKILLS,
        'crafting':skills_db.CRAFTING_CIRCLES,
        'lore':skills_db.LORE
    }

    skills=all_skills.get(category)

    if skills is None:
        return "Invalid category", 404

    flags = ['can_assassinate', 'can_instruct', 'can_invent', 'gm_mage', 'is_crafter', 'Literate','has_faith', 'can_field_repair']

    character = tm.Character.from_session(session)

    display_dict = construct_display_dict(character)

    return render_template(
        "skill_page.html",
        skills=skills,
        category=category,
        skills_added=session.get("skills_added", {}),
        display_dict=display_dict
    )

@app.route("/reset_character", methods=["GET"])
def reset_character():
    back_to_the_death_realms_with_you()
    return render_template('set_character.html')

@app.route("/enter_backstory", methods=["POST"])
def trauma_dump_and_or_explode():
    return render_template('submit_backstory.html')

@app.route("/submit_backstory", methods=["POST"])
def submit_backstory():
    backstory = request.form.get("backstory")

    if contains_google_doc_link(backstory):
        return jsonify({
            "success": False,
            "error": "Links are not allowed in backstories"
        }), 400

    session['character_details']['backstory'] = backstory
    session.modified = True

    return jsonify({
        "success": True,
        "message": "Backstory saved"
    })

@app.route("/modify_skill", methods=["POST"])
def modify_skill(data=None):
        data=request.get_json()

        global session

        character = tm.Character.from_session(session)

        input = tm.SkillChangeInput(data)
        input.validate()

        if input.modifier not in (1,-1):
            return {"success":False,"error":"INVALID_MODIFIER"},

        skill = Construct_Skill(input, character)

        flag_location = session['skills_added']

        try:
            if input.modifier==1:
                modification= flask_add_skill(skill)
                
            else:
                modification = flask_remove_skill(skill)

            if hasattr(skill, 'flags'):
                skill.modify_flags(flag_location)

            Update_Points()

            t_points = session['skills_added'].get('Toughness',0)
            modification['HP'] = 5 + t_points

            try:
                modification['points']=Update_Points()
            except TypeError:
                pass

            session.modified = True
            
            if SKILL_REF[input.name].get("redirect"):
                modification['redirect']=SKILL_REF[input.name]['redirect']

            return modification
        
        except exc.Not_Same_Gathering:
            return jsonify({'success':False, 'error':f'A skill and its prerequisite cannot be added in the same gathering'})
        except exc.Prereq_Flag_Raised:
            return jsonify({'success':False, 'error':f'You need one of the following skills:\n\n {'\n'.join(prereq for prereq in skill.missing_prereqs if prereq not in constants.FLAGS)}'})
        except exc.Prereq_Not_Met:
            return jsonify({"success": False, "error": f"you need the following skills to add {skill.name}:\n\n{', '.join(prereq for prereq in skill.missing_prereqs if prereq not in constants.FLAGS)}", "message":"haahahahahahha"})
        except exc.Max_Points_Spent:
            return jsonify({"success": False, "error": f"You do not have enough points."})
        except exc.Memory_Flaw_Already_Added:
            return jsonify({'success':False, 'error':'You have already added a memory flaw'})
        except exc.Weapon_Master_Added:
            return jsonify({'success':False, 'error':'In order to remove this skill, you must instead remove WEAPON MASTER'})
        except exc.ReliantSkills as e:
            try:
                for rel in skill.reliant_skills:
                    if rel in constants.FLAGS:
                        character = tm.Character.from_session(session)
                        raise exc.Removal_Not_Allowed_Flag(rel, character.skills_added)
            except exc.Removal_Not_Allowed_Flag as e:
                return jsonify({'success':False,'error':f'{e}'})
            return jsonify({'success':False,'error':f'You must remove these skills first:\n\n{skill.failed_skill}'})
        except exc.Future_Gat_Dependancy as e:
            return jsonify({'success':False,'error': e.message})
        except exc.Bloodline_Requirement:
            return jsonify({'success':False,'error':'Newborn dreams are required to take Tethered'})

@app.route("/add_skill",methods=["POST"])
def flask_add_skill(skill):
        tm.add_skill(skill)
        if session['character_type'] == 'character_plan':
            if hasattr(skill,'prereqs'):
                try:
                    skill.check_prereqs(session['gatherings_skills'][str(int(session['gathering'])-1)])
                except exc.Prereq_Not_Met or exc.Prereq_Flag_Raised:
                    raise exc.Not_Same_Gathering
        session['skills_added'][skill.name] = skill.quantity   
        session.modified = True
        return {
            'success': True,
            "message": "Added Skill",
            "points": session["character_details"]["points"],
            "HP": session["character_details"]["health points"],
            "name": session["character_details"].get("name", "no name selected"),
            "culture": session["character_details"].get("culture", "no culture selected"),
            "bloodline": session["character_details"].get("bloodline", "no bloodline selected"),
            "faith": session["character_details"].get("faith", "no faith selected"),
        }

@app.route("/remove_skill", methods=["POST"])
def flask_remove_skill(skill):
    tm.remove_skill(skill)

    try:
        del session['skills_added'][skill.name]
    except KeyError:
        if skill.name == 'Weapon Master':
            pass
        else:
            raise KeyError
        
    if session['character_type'] == 'character_plan':
        check = session['skills_added'].copy()
        skill.flag_modifier = -1
        if hasattr(skill,'flags'):
            skill.modify_flags(check)
        try:
            check_downstream_sessions(check)
        except exc.Future_Gat_Dependancy as e:
            session['skills_added'][skill.name] = skill.quantity
            raise exc.Future_Gat_Dependancy(e.gat, e.skill)

    return {
            'success': True,
            "message": "Added Skill",
            "points": session["character_details"]["points"],
            "HP": session["character_details"]["health points"],
            "name": session["character_details"].get("name", "no name selected"),
            "culture": session["character_details"].get("culture", "no culture selected"),
            "bloodline": session["character_details"].get("bloodline", "no bloodline selected"),
            "faith": session["character_details"].get("faith", "no faith selected"),
        }

def check_downstream_sessions(check):
    for gat in session['gatherings_skills']:
        if int(gat) > int(session['gathering']):
            for skill in session['gatherings_skills'][gat]:
                if skill in constants.FLAGS:
                    continue
                input={'skill':skill, 'quantity':session['gatherings_skills'][gat][skill]}
                input = tm.SkillChangeInput(input)
                character = tm.Character.from_session(session)
                skill_=Construct_Skill(input, character)
                if hasattr(skill_, 'prereqs'):
                    if skill_.prereqs is not None:
                        for prereq in skill_.prereqs:
                            try:
                                if skill_.prereqs[prereq] > check[prereq]:
                                    raise exc.Future_Gat_Dependancy(gat, skill)
                            except KeyError:
                                raise exc.Future_Gat_Dependancy(gat, skill)

@app.route("/reset", methods=["POST"])
def reset():
    reset_skills()
    
    skills_db_dict = {
        k: v
        for k, v in vars(skills_db).items()
        if isinstance(v, dict)
    }
    del skills_db_dict['__builtins__']

    Update_Points()

    if '/' in session['character_details']['culture']:
        cultures = session['character_details']['culture'].split('/')
    else:
        cultures = [session['character_details']['culture'],]
    
    for culture in cultures:
        session['skills_added'][f'Native Lore: {culture}'] = 1

    session.modified=True
    
    return maliks_idea()

skill_reference=None

skills_added={}

import sheet_creator

if __name__=="__main__":
    app.run(debug=True)