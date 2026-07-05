from app import session, SKILL_REF, SkillChangeInput,Construct_Skill, add_skill
from abc import ABC
import constants
import exceptions as exc

class Skill(ABC):   
    def __init__(self, name: str, quantity=1, max_quant=None, prereqs: dict = None):
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
        if hasattr(self, "prereqs") and self.prereqs is not None:
            self.process_prereq_chain()
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
        if self.name=='Tethered':
            raise exc.Bloodline_Requirement
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
            input=SkillChangeInput(data)
            current_skill=Construct_Skill(input)
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
            self.check_prereqs(check_dict=session)

    def check_points(self):
        current_points=session['character_details']['points']
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
                        raise exc.Prereq_Flag_Raised
                    if quant==1:
                        self.missing_prereqs.append(skill)
                    else:
                        self.missing_prereqs.append(f'{skill} x {quant}')
        if self.missing_prereqs != []:
            raise exc.Prereq_Not_Met("Prerequisite not met")
    
    def modify_flags(self,modification,flag_location = None):
        if flag_location is None:
            flag_location = session['skills_added']
        for flag in self.flags:
            flag_location[flag]+=modification

    def process_prereq_chain(self):
        self.prereq_chain={}
        self.add_prereqs()
        points=session['character_details']['points']
        if self.prereq_cost>points:
            pass #something that happens when prereq chain costs too much
        
    
    def add_prereqs(self):
        self.prereq_cost=0
        if hasattr(self,'prereqs') and self.prereqs is not None:
            chain=self.construct_prereq_chain()
            prereq_objs=self.get_prereq_objs(chain)
            chain_cost=self.get_chain_cost(prereq_objs)

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
            skill_obj=Construct_Skill(skill_data)
            prereq_objs.append(skill_obj)
        return prereq_objs

    def prereq_costs(self,chain):
        pass
    
    def construct_prereq_chain(self):
        prereqs_to_add=[]
        for skill in self.prereqs:
            if skill not in session['skills_added']:
                prereqs_to_add.append(skill)
        return prereqs_to_add

class Weapon_Master(Skill):
    def __init__(self):
        self.name='Weapon Master'
        self.cost=6
        self.quantity=1
        self.max_quant=1
        self.weapons_gained=['Short Weapons', 'One-Handed Weapons', 'Two-Handed Weapons', 'Oversized Weapon Use',
                             'Thrown Weapons', 'Bow and Arrow']
    
    def add(self):
        for weapon in self.weapons_gained:
            skill_info=SkillChangeInput({'skill':weapon,'quantity':1})
            skill=Construct_Skill(skill_info)
            add_skill(skill)
        session['skills_added'][self.name]=1
        session.modified=True
        session['skills_added']['Weapon_Master']-=1

    def remove(self):
        for weapon in self.weapons_gained[::-1]:
            del session['skills_added'][weapon]
        session.modified=True
        del session['skills_added'][self.name]
        session['skills_added']['Weapon_Master']+=1
    
    def check_reliance(self,pass_dict):
        self.prereqs={}
        for weapon in self.weapons_gained:
            self.prereqs[weapon]=1
        super().check_reliance(pass_dict)

class Quad_Level_Skill(Skill):
    def __init__(self, name, level, prereqs,cost_per_level=6):
        if level>4:
            raise exc.Skill_Not_Exist('This skill maxes out at level 4.')
        cost=level*cost_per_level
        super().__init__(name,prereqs=prereqs,quantity=level)

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
            raise exc.Prereq_Not_Met
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
    def __init__(self, name, quantity,prereqs):
        self.flags=['can_instruct']
        super().__init__(name, quantity=quantity,prereqs=prereqs)

class Assassin_Eligibility_Skill(Skill):
    def __init__(self, name):
        self.flags=['can_assassinate']
        super().__init__(name)
    
class Fortification_Skill(Skill):
    def __init__(self, name, cost, quantity, prereqs):
        self.flags=['can_fortify']
        super().__init__(name, cost, quantity=quantity, prereqs=prereqs)

class Field_Repair_Skill(Skill):
    def __init__(self, name, prereqs):
        self.prereqs=prereqs
        self.flags=['can_field_repair']
        super().__init__(name, prereqs=prereqs)

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
                raise exc.Memory_Flaw_Already_Added
        except KeyError:
            pass
    
    def remove(self):
        session['skills_added']['memory_flaws']-=1
        session.modifed=True
        super().remove()