class UnspentPoints(Exception):
    pass

class Too_Many_Points(Exception):
    pass

class MissingBackstory(Exception):
    pass

class ReliantSkills(Exception):
    pass

class Backstory_Is_Link(Exception):
    pass

class Bloodline_Requirement(Exception):
    pass

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

class Prereq_Flag_Raised(Exception):
    pass

class Weapon_Master_Added(Exception):
    pass

class Future_Gat_Dependancy(Exception):
    def __init__(self, gathering, skill):
        self.gat = gathering
        self.skill = skill
        self.message = f'You must remove {skill} from {gathering} first'

class Removal_Not_Allowed_Flag(Exception):
    def __init__(self, flag, skills):
        import constants
        flag_skill = constants.FLAG_MAP[flag]

        if not isinstance(flag_skill,list):
            message = f'You must first remove {flag_skill}'
        else:
            for skill in flag_skill:
                if skill in skills:
                    present_skill = skill

            message = f'You must first remove {present_skill}'

        super().__init__(message)