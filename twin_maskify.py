import exceptions as exc
from skills_db import SKILL_REF

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

class Gathering:
    def __init__(self, number, date, cp_earned=3, ip_converted=0, food_tag=False, total_cp = 0):
        self.number = number
        self.date = date
        self.cp_earned = cp_earned
        self.ip_converted = ip_converted
        self.food_tag = food_tag
        self.total_cp = total_cp

    def sum_CP(self):
        self.new_cp = int(self.cp_earned) + int(self.ip_converted) + int(self.food_tag) + int(self.total_cp)

class Character:
    def __init__(self):
        self.flags = {}
        self.skills_added = {}
        self.details = {}

    @classmethod
    def from_session(cls, session):
        character = cls()
        character.flags = session.get("flags", {})
        character.skills_added = session["skills_added"]
        character.details = session.get("character_details", {})
        return character
    
    @classmethod
    def from_character_sheet(cls, sheet):
        pass

    def sync(self, persistence_layer):
        self.skills_added = persistence_layer['skills_added']

        return persistence_layer

def add_skill(skill):
    skill.add()

def remove_skill(skill):
    skill.remove()

craft_level_map = {
    1:'Apprentice',
    2:'Journeyman',
    3:'Master',
    4:'Grandmaster'
}