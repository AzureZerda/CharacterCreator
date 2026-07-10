from flask import Flask, render_template, request, session, jsonify, redirect, url_for, flash
from abc import ABC
import json
from bloodline_skills import BLOODLINE_SKILLS
import re
import os
import constants
import exceptions as exc
from prebuilts import PREBUILTS
import skills_db
from skills_db import SKILL_REF
from Skills import Construct_Skill
import twin_maskify as tm

app=Flask(__name__)
app.secret_key=os.getenv("SECRET_KEY")

@app.route("/")
def buttons():
    return render_template('landing_page.html')

def construct_skill_ref():
    all_skill_sets = {
        k: v
        for k, v in vars(skills_db).items()
        if isinstance(v, dict)
    }

    if '__builtins__' in all_skill_sets:
        del all_skill_sets['__builtins__']

    new_skill_sets={}

    for skills in all_skill_sets.values():
        for skill_name, skill_details in skills.items():
            SKILL_REF[skill_name] = skill_details

    for bloodline in BLOODLINE_SKILLS:
        pull_dict=BLOODLINE_SKILLS[bloodline]
        for skill_name, skill_details in pull_dict.items():
            SKILL_REF[skill_name]=skill_details
            SKILL_REF[skill_name]['Sheet_Box']='Bloodline'

    for key in all_skill_sets:
        new_skill_sets[key.replace('_',' ')]=all_skill_sets[key]

    return new_skill_sets

def contains_google_doc_link(text):
    LINK_REGEX = re.compile(r"(https?://[^\s]+|www\.[^\s]+)", re.IGNORECASE)
    return bool(re.search(LINK_REGEX, text))

def Determine_Route(skill):
    router={
        'short weapons':0,
        'thrown weapons':0,
        'bow and arrow':0,
        'lockpicking':1,
        'alchemy':2,
        'channeling':2,
        'divination':2,
        'sorcery':2,
        'warding':2,
        'priesthood':3,
        'blacksmithing':4,
        'armorsmithing':4,
        'weaponsmithing':4,
        'shieldsmithing':4,
        'enchanting':4,
        'scroll scribing':4,
        'artificing':4,
        'cooking':4,
        'stable alchemy':4,
        'tailoring':4,
        'fletching':4,
        'engineering':4,
        'defensive instruction':5,
        'offensive instruction':5,
        'evasive instruction':5,
        'repair shield':6,
        'fortify armor':6,
        'clouded memory':7,
        'fractured memory':7,
        'fading memory':7,
        'sovereign zeal':8,
        'religious zeal':8,
        'corrupted':8,
        'oathbound':8,
        'frail':8,
        'illiterate':8,
        'weapon master':9
        }
    
    try:
        route=router[skill]
    except KeyError:
        route=99
    
    return route

@app.route("/process_person", methods=["POST"])
def process_person():
    name = request.form.get("name")
    email = request.form.get("email")
    discord = request.form.get("discord")
    character_name = request.form.get("character_name")
    emergency = request.form.get('emergency_contact')

    session['person_details']={'name':name,'email':email,'discord':discord, 'emergency_contact':emergency}

    skills_db_dict = {
        k: v
        for k, v in vars(skills_db).items()
        if isinstance(v, dict)
    }
    del skills_db_dict['__builtins__']

    return render_template('character_setup.html',back_url=url_for("home"))

@app.context_processor
def inject_globals():
    if 'Toughness' in session['skills_added']:
        session['character_details']['health points']=5+session['skills_added']['Toughness']
    else:
        session['character_details']['health points']=5
    display_dict=dict(session['skills_added'])
    flags=constants.FLAGS
    for flag in flags:
        try:
            del display_dict[flag]
        except KeyError:
            pass
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

def reset_skills():
    for cat in constants.DEFAULT_SESSION:
        if cat=='character_details':
            continue
        session[cat]=constants.DEFAULT_SESSION[cat].copy()

    session['character_details']['flaws_added']=[]
    
    session.modified=True

def reset_session():
    for cat in constants.DEFAULT_SESSION:
        if cat=='character_details':
            continue
        session[cat]=constants.DEFAULT_SESSION[cat].copy()
    
    session.modified=True

def Update_Points():
    # at some point the base native lore started showing up in here. Fix it azzy
    character = tm.Character.from_session(session)

    if session['character_details']['bloodline'].lower() not in constants.FORTY_POINTS:
        base_total=20
    else:
        base_total=40 

    if 'points_earned' in session:
        base_total+=session['points_earned']

    base_total+=int(character.details['incentive_points'])

    flaw_points=0
    
    skills_list= dict(session['skills_added'])

    native_skips=0

    for skill in skills_list.copy(): 
        if skill[:6]=='Native' and native_skips==0:
            del skills_list[skill]
            native_skips+=1

    if session['character_details']['bloodline'].lower() != 'newborn dream' and 'Tethered' in session['character_details']['flaws_added']:
        session['character_details']['flaws_added'].remove('Tethered')

    for flaw in session['character_details']['flaws_added']:
        new_flaw_points = flaw_points + -SKILL_REF[flaw]['Cost']
        
        if new_flaw_points >= 10:
            flaw_points = 10
            break
        elif new_flaw_points<10:
            flaw_points=new_flaw_points

    base_total+=flaw_points
    
    if 'Pursuit of Knowledge' in skills_list:
        lore_score=session['flags']['lore_score']

        if lore_score>=12:
            base_total+=12
        elif lore_score==0:
            pass
        else:
            base_total+=lore_score

    dict_ref=session['Point_Cats']
    lore_score=dict_ref['lore_score']

    if 'Weapon Master' in skills_list:
        for skill in constants.WEAPON_MASTER_SKILLS:
            del skills_list[skill]

    for skill,quantity in skills_list.items():
  
        if skill in constants.FLAWS:
            continue
        if skill[:7]=='Native':
            continue
        try:
            skill_cost=SKILL_REF[skill]['Cost']
        except KeyError:
            if skill[:6]=='Native':
                skill_cost=4
            else:
                continue

        base_total-=skill_cost*quantity

    if 'Pursuit of Knowledge' in skills_list:
        if lore_score >= 12:
            base_total+=12
        else:
            base_total+=lore_score
    
    session['character_details']['points']=base_total

    return base_total

class SkillChangeInput:
    def __init__(self,data):
        self.name=data['skill']
        self.quant=data['quantity']
        self.modifier=data.get('modifier')
    
    def validate(self):
        if self.name not in SKILL_REF:
            raise exc.Skill_Not_Exist
        
        if SKILL_REF[self.name]['Max'] is not None:
            if self.quant>SKILL_REF[self.name]['Max']:
                raise exc.Max_Quantity_Exceeded
        
        if not isinstance(self.quant,int):
            raise TypeError

@app.route("/new_player_landing")
def new_player_landing():
    session['character_type'] = 'new_character'
    session.modified = True
    return render_template('set_character.html')

@app.route("/submit")
def submit_page():
    display_dict=dict(session['skills_added'])
    flags=constants.FLAGS
    for flag in flags:
        try:
            del display_dict[flag]
        except KeyError:
            pass

    if 'Weapon Master' in display_dict:
        for weapon in constants.WEAPON_MASTER_SKILLS:
            del display_dict[weapon]

    char_ref=dict(session['character_details'])

    char_dict={'name':char_ref['name'],'Culture':char_ref['culture'],'bloodline':char_ref['bloodline'],'faith':char_ref['faith'],'HP':char_ref['health points']}

    display_dict[f'Native Lore: {char_dict['Culture']}']=1

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

@app.route("/confirm_character")
def confirm():
    return render_template('confirm_character.html')

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
    return render_template('premade_or_custom.html')

def reset_skill_selections():
    session['character_details']['health_points']=5
    char_ref=session['character_details']
    char_ref['flaws_added']=[]
    session['skills_added']={'Literate': 0, 'Weapon_Master': 0, 
                             'can_assassinate': 0, 'can_field_repair': 0, 'can_fortify': 0, 
                             'can_instruct': 0, 'can_invent': 0, 'gm_mage': 0, 'has_faith': 0, 
                             'is_crafter': 0, 'memory_flaws': 0}
    session.modified=True

@app.route("/select_prebuilt", methods=["POST"])
def select_prebuilt():
    # there's some oddity going on in here. Azzy thinks she fixed it. We will see.
    #Azzy the health points calculation is broken. Fix!!!
    # oh also charismatic courtier is throwing a key error. fix it azzy! Fixed- Azzy

    reset_skill_selections()

    Update_Points()

    data = request.get_json()

    prebuilt = data.get("prebuilt")

    session['skills_added'][f'Native Lore: {session['character_details']['culture']}']=1
    session['skills_added'][f'Native Lore: {session['character_details']['second_culture']}']=1

    for skill in PREBUILTS[prebuilt]['skills']:
        input={'skill':skill, 'quantity':PREBUILTS[prebuilt]['skills'][skill]}
        input=SkillChangeInput(input)
        skill_=Construct_Skill(input)

        if hasattr(skill_, "flags") and skill_.flags is not None:
            skill_.modify_flags(1)
        
        if isinstance(skill_,Memory_Flaw):
            session['skills_added']['memory_flaws']=1
            session['character_details']['flaws_added'].append(skill)

        elif isinstance(skill_, Background_Flaw):
            session['character_details']['flaws_added'].append(skill)

        session['skills_added'][skill]=PREBUILTS[prebuilt]['skills'][skill]

    return "", 204

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

def inject_bloodline_skills(session,dictionary):
    bloodline=session["character_details"]["bloodline"]

    dictionary[f'{bloodline.upper()} ONLY SKILLS']=BLOODLINE_SKILLS.get(bloodline,{})

    return dictionary

@app.route("/all_skills")
def maliks_idea():
    skills_db_dict = construct_skill_ref()

    skills_db_dict=inject_bloodline_skills(session,skills_db_dict)

    Update_Points()

    return render_template('all_skills.html', skills_db=skills_db_dict,back_url=url_for("character_setup"))

class Player_Details_Input:
    def __init__(self,input):
        self.name=input['player_name']
        self.email=input['email']
        self.emergency = input['emergency_contact']
        if input['discord']=='':
            self.discord='None'
        else:
            self.discord=input['discord']

class Character_Details_Input:
    def __init__(self,input):
        self.name=input['name']
        self.culture=input['culture']
        self.bloodline=input['bloodline']
        self.faith=input['faith']
        self.incentive_points = input['incentive_points']

def insert_char_details(player):
    session['person_details']={}
    per_ref=session['person_details']
    per_ref['name']=player.name
    per_ref['discord']=player.discord
    per_ref['email']=player.email
    per_ref['emergency_contact']=player.emergency

@app.route('/submission_test', methods=['POST'])
def new_player():
    session['skills_added'] = constants.DEFAULT_SESSION['skills_added'].copy()
    session.modifed=True

    data = request.get_json()
    create_char(data)
    return '', 204

def create_char(data):

    data = request.get_json()

    player=Player_Details_Input(data)

    character_ = Character_Details_Input(data)

    global session

    for cat in session:
        try:
            session[cat] = constants.DEFAULT_SESSION[cat].copy()
        except KeyError:
            continue

    if character_.bloodline.lower()=='newborn dream':
        skills_db.BACKGROUND_FLAWS['Tethered']={'Max':1,'Cost':-10}
        SKILL_REF['Tethered']={'Max':1,'Cost':-10}
        session['character_details']['flaws_added'].append('Tethered')
        session.modified=True
        session['skills_added']['Tethered']=1

    else:
        session['character_details']['flaws_added']=[]
        if 'Tethered' in SKILL_REF:
            del SKILL_REF['Tethered']

    insert_char_details(player)

    char_ref=session['character_details']
    char_ref['name']=character_.name
    char_ref['culture']=character_.culture
    char_ref['bloodline']=character_.bloodline
    char_ref['faith']=character_.faith

    input={'skill':f'Native Lore: {data['culture']}',
        'quantity':1,'modifer':1}
    input=SkillChangeInput(input)

    character = tm.Character.from_session(session)

    skill=Construct_Skill(input, character)
    tm.add_skill(skill)
    
    if 'second_culture' in data:
        char_ref['second_culture']=data['second_culture']
        input={'skill':f'Native Lore: {data['second_culture']}',
        'quantity':1,'modifer':1}
        input=SkillChangeInput(input)
        skill=Construct_Skill(input, character)
        tm.add_skill(skill)
    if 'incentive_points' in data:
        char_ref['incentive_points']=data['incentive_points']
    else:
        char_ref['incentive_points']=0

    session['character_details']['points']=Update_Points()

@app.route("/set_character/<category>")
def set_character(category):
    return render_template("set_character.html", category=category)

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

    display_dict = dict(session.get("skills_added", {}))
    for flag in flags:
        display_dict.pop(flag, None)

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

def back_to_the_death_realms_with_you():
    for cat in session:
        try:
            session[cat]=constants.DEFAULT_SESSION[cat].copy()
        except KeyError:
            continue
    session.modified=True

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
def modify_skill():
        data=request.get_json()

        global session

        character = tm.Character.from_session(session)

        input=SkillChangeInput(data)
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

            session.modified = True

            Update_Points()

            try:
                modification['points']=Update_Points()
            except TypeError:
                pass

            if SKILL_REF[input.name].get("redirect"):
                modification['redirect']=SKILL_REF[input.name]['redirect']

            return modification
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
        except exc.Bloodline_Requirement:
            return jsonify({'success':False,'error':'Newborn dreams are required to take Tethered'})

@app.route("/add_skill",methods=["POST"])
def flask_add_skill(skill):
        tm.add_skill(skill)
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

    session.modified=True

    return maliks_idea()

#@app.route("/create_character", methods=["POST"])
#def create_character():
#
#    #session['skills_added'] = constants.DEFAULT_SESSION['skills_added']
#
#    session["character_details"].update({
#    "name": request.form.get("name"),
#    "culture": request.form.get("culture"),
#    "bloodline": request.form.get("bloodline"),
#    "faith": request.form.get("faith")
#    })
#
#    session.modified = True
#
#    skills_db_dict = {
#        k: v
#        for k, v in vars(skills_db).items()
#        if isinstance(v, dict)
#    }
#    del skills_db_dict['__builtins__']
#
#    return maliks_idea()

skill_reference=None

skills_added={}

#import sheet_creator

if __name__=="__main__":
    app.run(debug=True)