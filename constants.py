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
    "skills_added":{},

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