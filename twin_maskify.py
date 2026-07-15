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