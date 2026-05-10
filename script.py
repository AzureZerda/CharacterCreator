from abc import ABC
import json
from app import session

with open("skills.json","r",encoding="utf-8") as f:
    skills=json.load(f)

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
        self.cost = cost
        self.quantity = quantity
        self.prereqs = prereqs if prereqs is not None else {}
        self.max_quant = max_quant

    def validate(self):
        self.check_eligiblity()
        self.check_quantity()
        self.check_prereqs()
    
    def check_eligiblity(self):
        if self.max_quant is not None:
            self.check_quantity()
        self.check_prereqs()
    
    def check_quantity(self):
        if self.quantity >= self.max_quant:
            raise Max_Quantity_Exceeded("Quantity exceeds maximum allowed")

    def check_prereqs(self):
        for skill, quant in self.prereqs.items():
            if skill not in skills_added or skills_added[skill] < quant:
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
        session[skills_added['can_assassinate']]+=1
        super().__init__(name, cost)

class Fortification_Skill(Skill):
    def __init__(self, name, cost, quantity, prereqs):
        session.skills_added['can_fortify']=1
        super().__init__(name, cost, quantity=quantity, prereqs=prereqs)

class Field_Repair_Skill(Skill):
    def __init__(self, name, cost, prereqs):
        session.skills_added['can_field_repair']=1
        super().__init__(name, cost, prereqs=prereqs)

def Process_Choice(data,route):
    try:
        prereqs=skills[data['skill']]['Prereq']
    except:
        prereqs=None
    if route==0:
        choice=Assassin_Eligibility_Skill(data['skill'],data['cost'])

router={
    'short weapons':0,
    'thrown weapons':0,
    'bow and arrow':0
}