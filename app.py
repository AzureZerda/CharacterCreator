from flask import Flask, render_template, request, session, jsonify, redirect, url_for, flash
from abc import ABC
import json
import skills_db

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
    else:
        choice=Skill(data['skill'],data['cost'],prereqs=prereqs)
    return choice

def Determine_Route(skill):
    router={
        'short weapons':0,
        'thrown weapons':0,
        'bow and arrow':0
        }
    
    try:
        route=router[skill]
    except KeyError:
        route=99
    
    return route

@app.context_processor
def inject_globals():
    return {
        "points": session.get("character_details", {}).get("points", 0)
    }

@app.before_request
def init_session():
    if "skills_added" not in session:
        session["skills_added"]={
            "gm_mage":0,
            "is_crafter":0,
            "can_invent":0,
            "can_instruct":0,
            "can_assassinate":0
        }
        session.modified=True
    
    if 'character_details' not in session:
        session['character_details']={
            'points':40
        }

@app.route("/")
def home():
    return render_template("landing_page.html")

@app.route("/skills/<category>")
def skills_page(category):
    all_skills={
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
        'crafting':skills_db.CRAFTING_CIRCLES
    }

    skills=all_skills.get(category)

    if skills is None:
        return "Invalid category", 404

    print(skills)

    return render_template(
        "skill_page.html",
        skills=skills,
        category=category
    )

@app.route("/add_skill",methods=["POST"])
def add_skill():
    print(session['character_details']['points'])
    skill=request.form.get("skill")
    quantity=int(request.form.get("quantity"))
    cost=int(request.form.get("cost"))

    data={
        "skill":skill,
        "quantity":quantity,
        "cost":cost
    }

    skill=Construct_Skill(data)

    try:
        skill.add()
        session["skills_added"][skill.name]=quantity
        session.modified=True
        print(session['character_details']['points'])
        return jsonify({'success':True,"message":"Added Skill","points": session["character_details"]["points"]})
    except Prereq_Not_Met:
       return jsonify({"success":False,"error":"Prerequisite not met"})

@app.route("/reset", methods=["POST"])
def reset():
    session.clear()
    return redirect(request.referrer or url_for("home"))

@app.route("/remove_skill", methods=["POST"])
def remove_skill():
    skill=request.form.get("skill")
    quantity=int(request.form.get("quantity"))
    cost=int(request.form.get("cost"))
    data={
        "skill":skill,
        "quantity":quantity,
        "cost":cost
    }

    skill=Construct_Skill(data)

    try:
        skill.remove()
    except Prereq_Not_Met:
        return jsonify({'success':False,'error':'Reliant skill must be removed'})
    session.modified=True

    return jsonify({"success": True,"points": session["character_details"]["points"]})

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

class Skill(ABC):   
    def __init__(self, name: str, cost: int, quantity=1, max_quant=None, prereqs: dict = None):
        self.name = name
        self.cost = SKILL_REF[name]['Cost']*quantity
        self.quantity = quantity
        try:
            self.prereqs = SKILL_REF[name]['Prereq']
        except KeyError:
            self.prereqs=None
        self.max_quant = max_quant

    def add(self):
        self.validate()
        session['character_details']['points']-=self.cost*self.quantity

    def remove(self):
        new_skills = dict(session["skills_added"])
        del new_skills[self.name]
        self.check_reliance(new_skills)
        session['skills_added']=new_skills
        session['character_details']['points']+=self.cost*self.quantity
    
    def check_reliance(self,skill_check):
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
            if current_skill.prereqs is not None:
                current_skill.check_prereqs(check_dict=skill_check)

    def validate(self):
        self.check_points()
        if self.max_quant is not None:
            self.check_quantity()
        if self.prereqs is not None:
            self.check_prereqs(check_dict=session)

    def check_points(self):
        current_points=session['character_details']['points']
        new_points=current_points-self.cost
    
    def check_quantity(self):
        if self.quantity >= self.max_quant:
            raise Max_Quantity_Exceeded("Quantity exceeds maximum allowed")

    def check_prereqs(self, check_dict):
        if 'skills_added' in check_dict:
            check_dict=check_dict['skills_added']
        for skill, quant in self.prereqs.items():
            if skill not in check_dict or check_dict[skill] < quant:
                raise Prereq_Not_Met("Prerequisite not met")

class Quad_Level_Skill(Skill):
    def __init__(self, name, level, prereqs,cost_per_level=6):
        if level>4:
            raise Skill_Not_Exist('This skill maxes out at level 4.')
        if level !=1:
            prereqs[name]=level-1
        cost=level*cost_per_level
        super().__init__(name,cost,prereqs=prereqs)

class Lockpicking(Quad_Level_Skill):
    def __init__(self,name,level):
        self.prereqs={}
        if level != 1:
            self.prereqs['lockpicking']=level-1
        super().__init__(name,level=level,prereqs=self.prereqs,cost_per_level=4)

class Magic(Quad_Level_Skill):
    def __init__(self, school, level):
        self.prereqs={}
        min_mana=level*5
        self.prereqs['mana_focus']=min_mana
        self.prereqs['magical_aptitude']=1
        self.prereqs[f'lore: {school}']=1
        if level==4:
            session.skills_added['gm_mage']=1
        super().__init__(school,level,self.prereqs)

class Priest_Level(Quad_Level_Skill):
    def __init__(self, level, faith):
        prereqs={}
        prereqs[f'lore: {faith}']=1
        super().__init__(name=f'Priesthood', level=level, prereqs=prereqs)

class Craft(Quad_Level_Skill):
    def __init__(self, name, level):
        self.prereqs={}
        session.skills_added['is_crafter']=1
        if level==4:
            session.skills_added['can_invent']+=1
        super().__init__(name, level,prereqs=self.prereqs)

class Lore(Skill):
    def __init__(self, name):
        super().__init__(name=f"Lore: {name}", cost=4, max_quant=1)

class Instruction_Ability(Skill):
    def __init__(self, name, quantity,cost_per,prereqs):
        cost=quantity*cost_per
        session.skills_added['can_instruct']+=1
        super().__init__(name, cost,quantity=quantity,prereqs=prereqs)

class Assassin_Eligibility_Skill(Skill):
    def __init__(self, name,cost):
        super().__init__(name, cost)
    
    def add(self):
        session['skills_added']['can_assassinate']+=1
        super().add()
    
    def remove(self):
        session['skills_added']['can_assassinate']-=1
        super().remove()

class Fortification_Skill(Skill):
    def __init__(self, name, cost, quantity, prereqs):
        session.skills_added['can_fortify']=1
        super().__init__(name, cost, quantity=quantity, prereqs=prereqs)

class Field_Repair_Skill(Skill):
    def __init__(self, name, cost, prereqs):
        session.skills_added['can_field_repair']=1
        super().__init__(name, cost, prereqs=prereqs)

all_skill_sets = {
    k: v
    for k, v in vars(skills_db).items()
    if isinstance(v, dict)
}

SKILL_REF = {}

for skills in all_skill_sets.values():
    for skill_name, skill_details in skills.items():
        SKILL_REF[skill_name] = skill_details

if __name__=="__main__":
    app.run(debug=True)