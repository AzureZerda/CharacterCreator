from abc import ABC
from skills_db import SKILL_REF
import exceptions as exc
import skills_db
import constants
from twin_maskify import add_skill

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

class Skill(ABC):   
    def __init__(self, character, name: str, quantity=1, max_quant=None, prereqs: dict = None):
        self.character = character
        self.name = name
        try:
            self.cost = SKILL_REF[name]['Cost']*quantity
        except KeyError:
            if name[:6]=='Native':
                self.cost=4
            else:
                raise KeyError
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
        self.flag_modifier = 1
        #if hasattr(self, "prereqs") and self.prereqs is not None:
        #    self.process_prereq_chain()
        self.validate()
        if 'lore' in self.name[:4].lower():
            self.character.flags['lore_score']+=4
        #session['character_details']['points']-=self.cost
        if self.name=='Toughness':
            self.character.details['health points']+=self.quantity

    def remove(self):
        if self.name in constants.WEAPON_MASTER_SKILLS and 'Weapon Master' in self.character.skills_added:
            raise exc.Weapon_Master_Added
        self.flag_modifier = -1
        if self.name=='Tethered':
            raise exc.Bloodline_Requirement
        new_skills = dict(self.character.skills_added).copy()
        del new_skills[self.name]
        if hasattr(self, 'flags'):
            for flag in self.flags:
                new_skills[flag] += self.flag_modifier
        
        for reliant_skill in new_skills:
            input = SkillChangeInput({'skill': reliant_skill, 'quantity': new_skills[reliant_skill]})
            try:
                check_skill = Construct_Skill(input, self.character)
            except KeyError:
                self.verify_removal
                continue

            self.reliant_skills = []
            if hasattr(check_skill, 'prereqs') and check_skill.prereqs is not None:
                for skill in check_skill.prereqs:
                    self.verify_removal(skill,check_skill.prereqs[skill],new_skills)
            if self.reliant_skills != []:
                self.failed_skill = reliant_skill
                raise exc.ReliantSkills

    def verify_removal(self,skill,required_quantity,check):
        try:
            if check[skill] >= required_quantity:
                pass
            else:
                self.reliant_skills.append(skill)
        except KeyError:
            self.reliant_skills.append(skill)
    
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
            input=SkillChangeInput(data)
            current_skill=Construct_Skill(input, self.character)
            if hasattr(current_skill, "prereqs") and current_skill.prereqs is not None:
                try:
                    current_skill.check_prereqs(check_dict=skill_check)
                except exc.Prereq_Not_Met:
                    self.reliant_skills.append(current_skill.name)

        if self.reliant_skills != []:
            raise exc.ReliantSkills

    def validate(self):
        self.check_points()
        if self.max_quant is not None:
            self.check_quantity()
        if hasattr(self, "prereqs") and self.prereqs is not None:
            self.missing_prereqs=[]
            self.check_prereqs(check_dict = self.character.skills_added)

    def check_points(self):
        current_points = self.character.details['points']
        new_points=current_points-self.cost
        if new_points<0:
            raise exc.Max_Points_Spent
    
    def check_quantity(self):
        if self.quantity > self.max_quant:
            raise exc.Max_Quantity_Exceeded("Quantity exceeds maximum allowed")

    def check_prereqs(self, check_dict):
        self.missing_prereqs=[]
        if 'skills_added' in check_dict:
            check_dict=check_dict['skills_added']
        if self.prereqs is not None:
            for skill, quant in self.prereqs.items():
                if skill not in check_dict or check_dict[skill] < quant:
                    if skill in constants.FLAGS:
                        if skill=='Weapon_Master':
                            raise exc.Weapon_Master_Added
                        self.missing_prereqs=constants.FLAGS[skill]
                        
                    if quant==1:
                        self.missing_prereqs.append(skill)
                    else:
                        self.missing_prereqs.append(f'{skill} x {quant}')
        if self.missing_prereqs != []:
            for m in self.missing_prereqs:
                if m in constants.FLAGS:
                    raise exc.Prereq_Flag_Raised
            raise exc.Prereq_Not_Met("Prerequisite not met")
    
    def modify_flags(self,flag_location):
        for flag in self.flags:
            flag_location[flag]+= self.flag_modifier

    def process_prereq_chain(self):
        self.prereq_chain={}
        self.add_prereqs()
        points = self.character.details['points']
        if self.prereq_cost>points:
            pass #something that happens when prereq chain costs too much
        
    def add_prereqs(self):
        self.prereq_cost=0
        if hasattr(self,'prereqs') and self.prereqs is not None:
            chain=self.construct_prereq_chain()
            prereq_objs=self.get_prereq_objs(chain)
            #chain_cost=self.get_chain_cost(prereq_objs)

    def get_chain_cost(self,chain):
        for prereq_obj in chain:
            self.prereq_cost+=prereq_obj.cost
            prereq_obj.add_prereqs()
            #if prereq_obj.prereqs is not None:
            #    self.all_prereqs.update(prereq_obj.prereqs)
            self.prereq_cost+=prereq_obj.prereq_cost

    def get_prereq_objs(self,chain):
        prereq_objs=[]
        for skill in chain:
            skill_quant=self.prereqs[skill]
            skill_cost=skill_quant*SKILL_REF[skill]['Cost']
            skill_data={'skill':skill, 'quantity':skill_quant, 'cost':skill_cost, 'modifier':None}
            skill_data=SkillChangeInput(skill_data)
            skill_obj=Construct_Skill(skill_data, self.character)
            prereq_objs.append(skill_obj)
        return prereq_objs

    def prereq_costs(self,chain):
        pass
    
    def construct_prereq_chain(self):
        prereqs_to_add=[]
        for skill in self.prereqs:
            if skill not in self.character.skills_added:
                prereqs_to_add.append(skill)
        return prereqs_to_add

class Weapon_Master(Skill):
    def __init__(self,character):
        self.name='Weapon Master'
        self.character = character
        self.cost=6
        self.quantity=1
        self.max_quant=1
        self.weapons_gained=['Short Weapons', 'One-Handed Weapons', 'Two-Handed Weapons', 'Oversized Weapon Use',
                             'Thrown Weapons', 'Bow and Arrow']
    
    def add(self):
        for weapon in self.weapons_gained:
            skill_info=SkillChangeInput({'skill':weapon,'quantity':1})
            skill=Construct_Skill(skill_info,self.character)
            add_skill(skill)
            self.character.skills_added[weapon]=1
            if hasattr(skill,'flags'):
                skill.modify_flags(self.character.skills_added)
        self.character.skills_added['Weapon_Master']-=1

    def remove(self):
        for weapon in self.weapons_gained[::-1]:
            del self.character.skills_added[weapon]
        self.character.skills_added['can_assassinate'] = 0
            
        del self.character.skills_added[self.name]
        self.character.skills_added['Weapon_Master']+=1
    
    def check_reliance(self,pass_dict):
        self.prereqs={}
        for weapon in self.weapons_gained:
            self.prereqs[weapon]=1
        super().check_reliance(pass_dict)

class Quad_Level_Skill(Skill):
    def __init__(self, name, level, prereqs, character, cost_per_level=6):
        if level>4:
            raise exc.Skill_Not_Exist('This skill maxes out at level 4.')
        cost=level*cost_per_level
        super().__init__(character,name,prereqs=prereqs,quantity=level)

class Lockpicking(Quad_Level_Skill):
    def __init__(self,name,level, character):
        self.prereqs={}
        super().__init__(name,level=level, character=character,prereqs=self.prereqs,cost_per_level=4)

class Magic(Quad_Level_Skill):
    def __init__(self, school, level, character):
        self.flags=[]
        self.prereqs={}
        min_mana=level*5
        self.prereqs['Mana Focus']=min_mana
        self.prereqs['Magical Aptitude']=1
        self.prereqs[f'Lore: {school}']=1
        if level==4:
            self.flags.append('gm_mage')
        super().__init__(school,level,self.prereqs, character=character)

class Priest_Level(Quad_Level_Skill):
    def __init__(self, level, faith, character):
        self.prereqs={'Prayer':1}
        if character.details=='':
            raise exc.Prereq_Not_Met
        super().__init__(name=f'Priesthood', level=level, prereqs=self.prereqs, character = character)

class Craft(Quad_Level_Skill):
    def __init__(self, name, level, character):
        self.prereqs={}
        self.flags=['is_crafter',]
        if level==4:
            self.flags.append('can_invent')
        if name.lower()=='armorsmithing' or name.lower()=='tailoring':
            self.flags.append('can_fortify')
        super().__init__(name, level,prereqs=self.prereqs, character=character)

class Lore(Skill):
    def __init__(self, name, character):
        super().__init__(name=f"Lore: {name}", cost=4, max_quant=1)

class Instruction_Ability(Skill):
    def __init__(self, name, quantity,prereqs, character):
        self.flags=['can_instruct']
        super().__init__(name=name, quantity=quantity,prereqs=prereqs,character=character)

class Assassin_Eligibility_Skill(Skill):
    def __init__(self, name, character):
        self.flags=['can_assassinate']
        super().__init__(character, name)
    
class Fortification_Skill(Skill):
    def __init__(self, name, cost, quantity, prereqs, character):
        self.flags=['can_fortify']
        super().__init__(name, cost, quantity=quantity, prereqs=prereqs)

class Field_Repair_Skill(Skill):
    def __init__(self, name, prereqs, character):
        self.prereqs=prereqs
        self.flags=['can_field_repair']
        super().__init__(character, name, prereqs=prereqs)

class Background_Flaw(Skill):
    def __init__(self, name, quantity, character):
        self.name=name
        self.quantity=quantity
        self.max_quant=None
        self.character = character

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
            self.character.details['health points']-=self.quantity
        if self.name=='Illiterate':
            self.character.skills_added['Literate']-=1

        for i in range(self.quantity):
            self.character.details['flaws_added'].append(self.name)
            
class Memory_Flaw(Background_Flaw):
    def __init__(self, name, character):
        super().__init__(name,quantity=1, character = character)
    
    def add(self):
        self.check_prereq()
        self.character.details['flaws_added'].append(self.name)
        self.character.skills_added['memory_flaws']=1

    def check_prereq(self):
        try:
            if self.character.skills_added['memory_flaws']:
                raise exc.Memory_Flaw_Already_Added
        except KeyError:
            pass
    
    def remove(self):
        session['skills_added']['memory_flaws']-=1
        session.modifed=True
        super().remove()

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

def Construct_Skill(input, character):
    route=Determine_Route(input.name.lower())
    try:
        prereqs=skills_db[input.name]['Prereq']
    except:
        prereqs=None
    if route==0:
        choice=Assassin_Eligibility_Skill(input.name, character)
    elif route==1:
        choice=Lockpicking(input.name,input.quant, character)
    elif route==2:
        choice=Magic(input.name,input.quant, character)
    elif route==3:
        choice=Priest_Level(input.quant,character.details['faith'],character)
    elif route==4:
        choice=Craft(input.name,input.quant, character)
    elif route==5:
        choice=Instruction_Ability(input.name,input.quant,SKILL_REF[input.name]['Prereq'],character)
    elif route==6:
        choice=Field_Repair_Skill(input.name,SKILL_REF[input.name]['Prereq'],character)
    elif route==7:
        choice=Memory_Flaw(input.name, character)
    elif route==8:
        choice=Background_Flaw(input.name,input.quant, character)
    elif route==9:
        choice=Weapon_Master(character)
    else:
        choice=Skill(character,input.name,quantity=input.quant,prereqs=prereqs)
    return choice