from flask import Flask, render_template, request, session, jsonify, redirect, url_for, flash
from abc import ABC
import json
import skills_db
from bloodline_skills import BLOODLINE_SKILLS

app=Flask(__name__)
app.secret_key="fennec"

def Construct_Skill(data):
    route=Determine_Route(data['skill'].lower())
    try:
        prereqs=skills_db[data['skill']]['Prereq']
    except:
        prereqs=None
    if route==0:
        choice=Assassin_Eligibility_Skill(data['skill'],data['cost'])
    elif route==1:
        choice=Lockpicking(data['skill'],data['quantity'])
    elif route==2:
        choice=Magic(data['skill'],data['quantity'])
    elif route==3:
        choice=Priest_Level(data['quantity'],session['character_details']['faith'])
    elif route==4:
        choice=Craft(data['skill'],data['quantity'])
    elif route==5:
        choice=Instruction_Ability(data['skill'],data['quantity'],SKILL_REF[data['skill']]['Cost'],SKILL_REF[data['skill']]['Prereq'])
    elif route==6:
        choice=Field_Repair_Skill(data['skill'],SKILL_REF[data['skill']]['Cost'],SKILL_REF[data['skill']]['Prereqs'])
    elif route==7:
        choice=Memory_Flaw(data['skill'])
    elif route==8:
        choice=Background_Flaw(data['skill'],data['quantity'])
    else:
        choice=Skill(data['skill'],data['cost'],quantity=data['quantity'],prereqs=prereqs)
    return choice

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
        'frail':8,
        'illiterate':8
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

    session['person_details']={'name':name,'email':email,'discord':discord}

    skills_db_dict = {
        k: v
        for k, v in vars(skills_db).items()
        if isinstance(v, dict)
    }
    del skills_db_dict['__builtins__']

    return render_template('character_setup.html',back_url=url_for("home"))

@app.context_processor
def inject_globals():
    display_dict=dict(session['skills_added'])
    flags=['Literate', 'can_assassinate', 'can_instruct', 'can_invent', 'gm_mage', 'has_faith', 'is_crafter']
    for flag in flags:
        del display_dict[flag]
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
    if "skills_added" not in session:
        session["skills_added"]={
            "gm_mage":0,
            "is_crafter":0,
            "can_invent":0,
            "can_instruct":0,
            "can_assassinate":0,
            'Literate':0,
            'has_faith':0
        }
        session.modified=True
    
    if 'character_details' not in session:
        session['character_details']={
            'points':40,
            'flaw_points':0,
            'memory_flaws':0,
            'health points':5,
            'flaws_added':[]
        }

    if 'flags' not in session:
        session['flags']={
            'points_warning_given':False,
            'lore_score':0}

def reset_session():
    session["skills_added"]={
        "gm_mage":0,
        "is_crafter":0,
        "can_invent":0,
        "can_instruct":0,
        "can_assassinate":0,
        'Literate':0,
        'has_faith':0,
        'memory_flaws':0
    }

    session['character_details']={
        'points':40,
        'flaw_points':0,
        'memory_flaws':0,
        'health points':5,
        'flaws_added':[]
    }

    session['flags']={
        'points_warning_given':False,
        'memory_flaws':0,
        'lore_score':0
        }
    
    session['Point_Cats']={
        'lore_score':0
    }
    
    session.modified=True

def Update_Points():
    new_total=40
    flaw_points=0

    for flaw in session['character_details']['flaws_added']:
        new_flaw_points = flaw_points + -SKILL_REF[flaw]['Cost']
        
        if new_flaw_points >= 10:
            flaw_points = 10
            break
        elif new_flaw_points<10:
            flaw_points=new_flaw_points

    new_total+=flaw_points
    
    flaws=['Sovereign Zeal','Religious Zeal','Religious Zeal','Corrupted','Frail',
           'Clouded Memory','Fractured Memory','Fading Memory','Illiterate','Oath Bound',
           'Tethered']

    dict_ref=session['Point_Cats']
    lore_score=dict_ref['lore_score']
    for skill,quantity in session['skills_added'].items():
        if skill in flaws:
            continue
        try:
            skill_cost=SKILL_REF[skill]['Cost']
        except KeyError:
            continue
        new_total-=skill_cost*quantity
    if 'Pursuit of Knowledge' in session['skills_added']:
        if lore_score >= 12:
            new_total+=12
        else:
            new_total+=lore_score
    if 'Weapon Master' in session['skills_added']:
        new_total-=13
    
    session['character_details']['points']=new_total
    return new_total

@app.route("/modify_skill", methods=["POST"])
def modify_skill():
        skill_name=request.form.get("skill")
        quantity=int(request.form.get("quantity",1))
        modifier=int(request.form.get("modifier",0))

        if modifier not in (1,-1):
            return {"success":False,"error":"INVALID_MODIFIER"},400

        if modifier==1:
            modification= add_skill(skill_name,quantity)
        else:
            modification= remove_skill(skill_name,quantity)

        try:
            modification['points']=Update_Points()
        except TypeError:
            pass

        return modification

@app.route("/submit")
def submit_page():
    display_dict=dict(session['skills_added'])
    flags=['Literate', 'can_assassinate', 'can_instruct', 'can_invent', 'gm_mage', 'has_faith', 'is_crafter']
    for flag in flags:
        del display_dict[flag]

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

@app.route("/confirm_character")
def confirm():
    return render_template('confirm_character.html')

class UnspentPoints(Exception):
    pass


class MissingBackstory(Exception):
    pass

class ReliantSkills(Exception):
    pass

@app.errorhandler(MissingBackstory)
def handle_missing_backstory(e):
    return {
        "success": False,
        "error": "MISSING_BACKSTORY",
        "message": "Backstory is required before submission."
    }, 400

@app.errorhandler(ReliantSkills)
def handle_reliant_skills(e):
    return jsonify({'success':False,'error':'Reliant skill must be removed', 'message':'slimmery'}), 400

@app.errorhandler(MissingBackstory)
def handle_missing_backstory(e):
    return {
        "success": False,
        "error": "MISSING_BACKSTORY",
        "message": "Backstory is required before submission."
    }, 400

@app.errorhandler(UnspentPoints)
def handle_missing_backstory(e):
    return {
        "success": False,
        "error": "UNSPENT_POINTS",
        "message": "Warning- you have unspent points.\n\nSubmit your character if you are okay with this."
    }, 400


@app.route('/confirm_submission', methods=['POST'])
def confirm_submission():
    try:
        backstory=session['character_details']['backstory']
    except KeyError:
        raise MissingBackstory()

    points=session['character_details']['points']

    if points>0 and session['flags']['points_warning_given'] is False:
        session['flags']['points_warning_given']=True
        session.modified=True
        raise UnspentPoints()
    
    return "", 204

@app.route("/character_setup", methods=["GET"])
def character_setup():
    return render_template("character_setup.html")

@app.route("/all_skills")
def maliks_idea():
    skills_db_dict = {
        k: v
        for k, v in vars(skills_db).items()
        if isinstance(v, dict)
    }
    del skills_db_dict['__builtins__']

    print(skills_db_dict)

    print(session["character_details"]["bloodline"])
    print(BLOODLINE_SKILLS[session["character_details"]["bloodline"]])

    bloodline=session["character_details"]["bloodline"]

    skills_db_dict[bloodline]=BLOODLINE_SKILLS.get(bloodline,{})


    return render_template('all_skills.html', skills_db=skills_db_dict,back_url=url_for("character_setup"))

@app.route("/")
def home():
    return render_template('set_character.html')

@app.route('/submission_test', methods=['POST'])
def submission_test():
    player_name     = request.form.get('player_name', '')
    email           = request.form.get('email', '')
    discord         = request.form.get('discord', '')
    character_name  = request.form.get('character_name', '')
    name            = request.form.get('name', '')
    culture         = request.form.get('culture', '')
    bloodline       = request.form.get('bloodline', '')
    faith           = request.form.get('faith', '')

    per_ref=session['person_details']
    per_ref['name']=player_name
    per_ref['discord']=discord
    per_ref['email']=email

    char_ref=session['character_details']
    char_ref['name']=name
    char_ref['culture']=culture
    char_ref['bloodline']=bloodline
    char_ref['faith']=faith

    session.modified=True

    return '', 204

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

    flags = ['can_assassinate', 'can_instruct', 'can_invent', 'gm_mage', 'is_crafter', 'Literate','has_faith']

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
    session["skills_added"]={
            "gm_mage":0,
            "is_crafter":0,
            "can_invent":0,
            "can_instruct":0,
            "can_assassinate":0,
            'Literate':0,
            'has_faith':0
        }
    session['character_details']['points']=40
    try:
        del session['character_details']['backstory']
    except KeyError:
        pass
    session.modified=True

@app.route("/enter_backstory", methods=["POST"])
def trauma_dump_and_or_explode():
    return render_template('submit_backstory.html')

@app.route("/submit_backstory", methods=["POST"])
def submit_backstory():
    backstory=request.form.get("backstory")

    session['character_details']['backstory']=backstory

    session.modified=True

    skills_db_dict = {
        k: v
        for k, v in vars(skills_db).items()
        if isinstance(v, dict)
    }
    del skills_db_dict['__builtins__']

    return render_template('all_skills.html',skills_db=skills_db_dict)

@app.route("/add_skill",methods=["POST"])
def add_skill(skill,quantity):
    cost=SKILL_REF[skill]['Cost']

    data={
        "skill":skill,
        "quantity":quantity,
        "cost":cost
    }

    skill=Construct_Skill(data)

    try:
        skill.add()
        session["skills_added"][skill.name] = quantity
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
    
    except Prereq_Not_Met:
        return jsonify({"success": False, "error": f"you need the following skills to add {skill.name}:\n\n{', '.join(skill.missing_prereqs)}", "message":"haahahahahahha"})
    except Max_Points_Spent:
        return jsonify({"success": False, "error": f"You do not have enough points."})
    except Memory_Flaw_Already_Added:
        return jsonify({'success':False, 'error':'You have already added a memory flaw'})
        

@app.route("/reset", methods=["POST"])
def reset():
    init_session()

    reset_session()

    session.modified=True
    skills_db_dict = {
        k: v
        for k, v in vars(skills_db).items()
        if isinstance(v, dict)
    }
    del skills_db_dict['__builtins__']

    return render_template('all_skills.html',skills_db=skills_db_dict)

@app.route("/remove_skill", methods=["POST"])
def remove_skill(skill,quantity):
    cost=SKILL_REF[skill]['Cost']
    data={
        "skill":skill,
        "quantity":quantity,
        "cost":cost
    }

    skill=Construct_Skill(data)

    try:
        skill.remove()
    except ReliantSkills:
        return jsonify({'success':False,'error':f'You must remove these skills first:\n\n{', '.join(skill.reliant_skills)}'})
    session.modified=True

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

@app.route("/create_character", methods=["POST"])
def create_character():

    session["character_details"].update({
    "name": request.form.get("name"),
    "culture": request.form.get("culture"),
    "bloodline": request.form.get("bloodline"),
    "faith": request.form.get("faith")
    })

    forty_points=['human','effendal']

    if session['character_details']['bloodline'].lower() not in forty_points:
        session['character_details']['points']=20

    session.modified = True

    skills_db_dict = {
        k: v
        for k, v in vars(skills_db).items()
        if isinstance(v, dict)
    }
    del skills_db_dict['__builtins__']

    return render_template('all_skills.html',skills_db=skills_db_dict)  # or wherever your main UI is

skill_reference=None

skills_added={}

class points_exhausted(Exception):
    pass

class Character:
    def __init__(self,char_points=40):
        self.skills_added={}
        self.skills_added['Literate']=1
        self.char_points=char_points
    
    def add_skill(self,skill):
        self.check_budget(skill.cost)
        skill.validate()
        self.skills_added[skill.name]=skill.quantity

    def check_budget(self,cost):
        new_point_total=self.char_points-cost
        if new_point_total<0:
            raise points_exhausted

class Prereq_Not_Met(Exception):
    pass

class Max_Quantity_Exceeded(Exception):
    pass

class Skill_Not_Exist(Exception):
    pass

class Max_Points_Spent(Exception):
    pass

class Memory_Flaw_Already_Added(Exception):
    pass

class Skill(ABC):   
    def __init__(self, name: str, cost: int, quantity=1, max_quant=None, prereqs: dict = None):
        self.name = name
        self.cost = SKILL_REF[name]['Cost']*quantity
        self.quantity = quantity
        if prereqs is None:
            try:
                self.prereqs = SKILL_REF[name]['Prereq']
            except KeyError:
                self.prereqs=None
        self.max_quant = max_quant
        if self.name=='Research':
            self.flags=['Literate']

    def add(self):
        self.validate()
        if hasattr(self, "flags") and self.flags is not None:
            self.modify_flags(1,session['skills_added'])
        if 'lore' in self.name[:4].lower():
            session['flags']['lore_score']+=4
        #session['character_details']['points']-=self.cost
        if self.name=='Toughness':
            session['character_details']['health points']+=self.quantity
        session.modified=True

    def remove(self):
        new_skills = dict(session["skills_added"])
        del new_skills[self.name]
        if hasattr(self, "flags") and self.flags is not None:
            self.modify_flags(-1,flag_location=new_skills)
        self.check_reliance(new_skills)
        session['skills_added']=new_skills
        if 'lore' in self.name[:4].lower():
            session['flags']['lore_score']-=4
        #session['character_details']['points']+=self.cost
        if self.name=='Toughness':
            session['character_details']['health points']-=self.quantity
        session.modified=True
    
    def check_reliance(self,skill_check):
        self.reliant_skills=[]
        for skill,quantity in skill_check.items():
            try:
                skill_cost=SKILL_REF[skill]['Cost']
            except KeyError:
                continue
            cost=skill_cost*quantity
            data={
                'skill':skill,
                'quantity':quantity,
                'cost':cost
            }
            current_skill=Construct_Skill(data)
            if hasattr(current_skill, "prereqs") and current_skill.prereqs is not None:
                try:
                    current_skill.check_prereqs(check_dict=skill_check)
                except Prereq_Not_Met:
                    self.reliant_skills.append(current_skill.name)
        if self.reliant_skills != []:
            raise ReliantSkills

    def validate(self):
        self.check_points()
        if self.max_quant is not None:
            self.check_quantity()
        if hasattr(self, "prereqs") and self.prereqs is not None:
            self.missing_prereqs=[]
            self.check_prereqs(check_dict=session)

    def check_points(self):
        current_points=session['character_details']['points']
        new_points=current_points-self.cost
        if new_points<0:
            raise Max_Points_Spent
    
    def check_quantity(self):
        if self.quantity > self.max_quant:
            raise Max_Quantity_Exceeded("Quantity exceeds maximum allowed")

    def check_prereqs(self, check_dict):
        self.missing_prereqs=[]
        if 'skills_added' in check_dict:
            check_dict=check_dict['skills_added']
        if self.prereqs is not None:
            for skill, quant in self.prereqs.items():
                if skill not in check_dict or check_dict[skill] < quant:
                    if quant==1:
                        self.missing_prereqs.append(skill)
                    else:
                        self.missing_prereqs.append(f'{skill} x {quant}')
        if self.missing_prereqs != []:
            raise Prereq_Not_Met("Prerequisite not met")
    
    def modify_flags(self,modification,flag_location):
        for flag in self.flags:
            flag_location[flag]+=modification

class Quad_Level_Skill(Skill):
    def __init__(self, name, level, prereqs,cost_per_level=6):
        if level>4:
            raise Skill_Not_Exist('This skill maxes out at level 4.')
        cost=level*cost_per_level
        super().__init__(name,cost,prereqs=prereqs,quantity=level)

class Lockpicking(Quad_Level_Skill):
    def __init__(self,name,level):
        self.prereqs={}
        super().__init__(name,level=level,prereqs=self.prereqs,cost_per_level=4)

class Magic(Quad_Level_Skill):
    def __init__(self, school, level):
        self.flags=[]
        self.prereqs={}
        min_mana=level*5
        self.prereqs['Mana Focus']=min_mana
        self.prereqs['Magical Aptitude']=1
        self.prereqs[f'Lore: {school}']=1
        if level==4:
            self.flags.append('gm_mage')
        super().__init__(school,level,self.prereqs)

class Priest_Level(Quad_Level_Skill):
    def __init__(self, level, faith):
        self.prereqs={'Prayer':1}
        if session['character_details']=='':
            raise Prereq_Not_Met
        super().__init__(name=f'Priesthood', level=level, prereqs=self.prereqs)

class Craft(Quad_Level_Skill):
    def __init__(self, name, level):
        self.prereqs={}
        self.flags=['is_crafter',]
        if level==4:
            self.flags.append('can_invent')
        if name.lower()=='armorsmithing' or name.lower()=='tailoring':
            self.flags.append('can_fortify')
        super().__init__(name, level,prereqs=self.prereqs)

class Lore(Skill):
    def __init__(self, name):
        super().__init__(name=f"Lore: {name}", cost=4, max_quant=1)

class Instruction_Ability(Skill):
    def __init__(self, name, quantity,cost_per,prereqs):
        cost=quantity*cost_per
        self.flags=['can_instruct']
        super().__init__(name, cost,quantity=quantity,prereqs=prereqs)

class Assassin_Eligibility_Skill(Skill):
    def __init__(self, name,cost):
        self.flags=['can_assassinate']
        super().__init__(name, cost)
    
class Fortification_Skill(Skill):
    def __init__(self, name, cost, quantity, prereqs):
        self.flags=['can_fortify']
        super().__init__(name, cost, quantity=quantity, prereqs=prereqs)

class Field_Repair_Skill(Skill):
    def __init__(self, name, cost, prereqs):
        self.flags=['can_field_repair']
        super().__init__(name, cost, prereqs=prereqs)

class Background_Flaw(Skill):
    def __init__(self, name, quantity):
        self.name=name
        self.quantity=quantity
        self.max_quant=None

        try:
            self.prereqs=SKILL_REF[name]['Prereq']
        except KeyError:
            pass
        self.cost=SKILL_REF[name]['Cost']*quantity
    
    def remove(self):
        if self.name=='Illiterate':
            session['skills_added']['Literate']+=1
        if self.name=='Frail':
            session['character_details']['health points']+=self.quantity
        for i in range(self.quantity):
            session['character_details']['flaws_added'].remove(self.name)

    def check_flaw_count(self):
        current_flaw_points=session['character_details']['flaw_points']
        new_total=self.cost+current_flaw_points
        if new_total>=-10:
            return self.cost
        else:
            if current_flaw_points==-10:
                return 0
            else:
                return -10+(current_flaw_points*-1)
    
    def add(self):
        if hasattr(self, "prereqs") and self.prereqs is not None:
            super().check_prereqs(session)
        if self.name=='Frail':
            session['character_details']['health points']-=self.quantity
        if self.name=='Illiterate':
            session['skills_added']['Literate']-=1

        for i in range(self.quantity):
            session['character_details']['flaws_added'].append(self.name)
            
class Memory_Flaw(Background_Flaw):
    def __init__(self, name):
        super().__init__(name,quantity=1)
    
    def add(self):
        self.check_prereq()
        session['character_details']['flaws_added'].append(self.name)
        session['skills_added']['memory_flaws']=1
        session.modifed=True

    def check_prereq(self):
        try:
            if session['skills_added']['memory_flaws']:
                raise Memory_Flaw_Already_Added
        except KeyError:
            pass
    
    def remove(self):
        session['skills_added']['memory_flaws']-=1
        session.modifed=True
        super().remove()

all_skill_sets = {
    k: v
    for k, v in vars(skills_db).items()
    if isinstance(v, dict)
}

SKILL_REF = {}

for skills in all_skill_sets.values():
    for skill_name, skill_details in skills.items():
        SKILL_REF[skill_name] = skill_details

for bloodline in BLOODLINE_SKILLS:
    pull_dict=BLOODLINE_SKILLS[bloodline]
    for skill_name, skill_details in pull_dict.items():
        SKILL_REF[skill_name]=skill_details

if __name__=="__main__":
    app.run(debug=True)