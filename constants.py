FLAGS={
    'gm_mage':[],
    'is_crafter':['Anything from CRAFTING CIRCLES except cooking'],
    'can_invent':['Anything from CRAFTING CIRCLES at level 4'],
    'can_instruct':['Offensive Instruction', 'Evasive Instruction', 'Defensive Instruction'],
    'can_assassinate':['Short Weapons', 'Thrown Weapons', 'Bow and Arrow'],
    'Literate':[],
    'has_faith':[],
    'memory_flaws':[],
    'can_field_repair':['Fortify Armor','Repair Shield'],
    'can_fortify':['Armorsmithing x1', 'Tailoring x1'],
    'Weapon_Master':[]
    }

DEFAULT_SESSION={
    "skills_added":{'Literate': 0, 'Weapon_Master': 0, 'can_assassinate': 0, 'can_field_repair': 0, 'can_fortify': 0, 'can_instruct': 0, 'can_invent': 0, 'gm_mage': 0, 'has_faith': 0, 'is_crafter': 0, 'memory_flaws': 0},

    'character_details':{
        'points':40,
        'flaw_points':0,
        'memory_flaws':0,
        'health points':5,
        'flaws_added':[]
    },
    'flags':{
        'points_warning_given':False,
        'lore_score':0,
        'memory_flaws':0},
        
    'Point_Cats':{
        'lore_score':0
    }
}

FORTY_POINTS=['human','effendal']

FLAWS=['Sovereign Zeal','Religious Zeal','Religious Zeal','Corrupted','Frail',
           'Clouded Memory','Fractured Memory','Fading Memory','Illiterate','Oathbound',
           'Tethered']

for flag in FLAGS:
    DEFAULT_SESSION['skills_added'][flag]=0

WEAPON_MASTER_SKILLS=['Bow and Arrow', 'One-Handed Weapons', 'Oversized Weapon Use', 'Short Weapons', 'Thrown Weapons', 'Two-Handed Weapons']

SHEET_BOXES=['Bloodline','Background','General Skills','Knowledge','Magical Arts','Gathering/Crafting']

DEFAULT_SKILLS=['Toughness','Mana Focus','Parry','Dodge','Willpower']

SHEET_RENAME_MAP={
    'bloodline':'Bloodline:',
    'culture':'Culture:',
    'faith':'Religion:',
    'name':'Character:',
    'name':'Player:',
    'email':'Email:'
}

SHEET_FORMULAS={
    'Total CP:':{'formula':'=SUM(Progression!C2:E1000)','col':'B','row':'7'},
    'Spent CP:':{'formula':'=SUM(B10:B)+SUM(F10:F)','col':'B','row':'8'},
    'Corruption:':{'formula':'=SUM(Progression!I2:I1000)','col':'E','row':'4'},
    'HP:':{'formula':'=(B17/3)+5','col':'G','row':'4'},
    'Mana:':{'formula':'=B18','col':'G','row':'5'},
    'CP Left:':{'formula':'=C7-C8','col':'F','row':'8'},
    'Incentive Points Left:':{'formula':'=SUM(Progression!H2:H1000)','col':'F','row':'6'}
}

PROGRESSION_HEADERS={'CP Credit Reason':'Characer Creation','Date Earned':'','CP Earned':40,
                     'IP to CP':'','Food Tag':'',
                     'Incentive Points and Taint':'Death (Character Creation)','Date Earned':'',
                     'IP Earned':'','Corruption Earned':'1','Staff Initials':''}