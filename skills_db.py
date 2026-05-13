BACKGROUND_FEATURES={
    'Magical Aptitude':{
        'Max':1,
        'Cost':4,
        'desc':'Required to learn and use magic'
    },
    'Prophetic Dreamer':{
        'Max':1,
        'Cost':4,
        'desc':'Dreams reveal future threats and events'
    },
    'Nobility':{
        'Max':1,
        'Cost':6,
        'desc':'High social status with privileges, responsibilities'
    },
    'Military Experience':{
        'Max':None,
        'Cost':4,
        'desc':'Recall military knowledge for situational insight'
    },
    'Bardic Knowledge':{
        'Max':1,
        'Cost':4,
        'desc':'Wide knowledge of lore, legends, customs'
    }
}

BACKGROUND_FLAWS={
    "Sovereign Zeal": {"Max": 1, "Cost": -2},
    "Religious Zeal": {"Max": 1, "Cost": -2},
    "Corrupted": {"Max": 1, "Cost": -6},
    "Frail": {"Max": None, "Cost": -3},

    "Clouded Memory": {
        "Max": 1,
        "Cost": -2,
        'Prereq':{
          'memory_flaws':0}
    },

    "Fractured Memory": {
        "Max": 1,
        "Cost": -4,
        'Prereq':{
          'memory_flaws':0}
    },

    "Fading Memory": {
        "Max": 1,
        "Cost": -4,
        'Prereq':{
          'memory_flaws':0}
    },
    "Illiterate": {"Max": 1, "Cost": -4, 'Prereq':{'Literate':0}},
    'Oathbound':{'Max':1, 'Cost': -6}}

WEAPON_PROFICIENCIES={
    "Short Weapons":{
        "Max":1,
        "Cost":1,
        "desc":"Use melee weapons up to 24 inches"
    },

    "One-Handed Weapons":{
        "Max":1,
        "Cost":2,
        "Prereq":{
            "Short Weapons":1
        },
        "desc":"Use melee weapons up to 48 inches"
    },

    "Two-Handed Weapons":{
        "Max":1,
        "Cost":3,
        "Prereq":{
            "One-Handed Weapons":1
        },
        "desc":"Use longer weapons requiring two hands"
    },

    "Oversized Weapon Use":{
        "Max":1,
        "Cost":2,
        "Prereq":{
            "Two-Handed Weapons":1
        },
        "desc":"Use two-handed weapons in one hand"
    },

    "Thrown Weapons":{
        "Max":1,
        "Cost":2,
        "desc":"Use and throw approved ranged weapons"
    },

    "Bow and Arrow":{
        "Max":1,
        "Cost":3,
        "desc":"Use bows safely in ranged combat"
    },

    "Two-Weapon Fighting":{
        "Max":1,
        "Cost":6,
        "desc":"Wield two weapons simultaneously in combat"
    }
}

ARMOR_PROFICIENCIES={
    "Armor Training: Light":{
        "Max":1,
        "Cost":2,
        "desc":"Wear light armor with moderate protection"
    },

    "Armor Training: Heavy":{
        "Max":1,
        "Cost":2,
        "Prereq":{
            "Armor Training: Light":1
        },
        "desc":"Wear heavy armor with high protection"
    },

    "Shield Use":{
        "Max":1,
        "Cost":2,
        "desc":"Use shields to block and defend"
    },

    "Helmet Mastery":{
        "Max":1,
        "Cost":2,
        "desc":"Immune to stun effects while helmeted"
    }
}

GENERAL_COMBAT_SKILLS={
  "Toughness":{
    "Max":5,
    "Cost":3,
    "desc":"Increase maximum health points permanently"
  },

  "Dodge":{
    "Max":None,
    "Cost":6,
    "desc":"Evade physical attacks completely once"
  },

  "Willpower":{
    "Max":None,
    "Cost":6,
    "desc":"Resist mental or non-physical effects"
  },

  "Parry":{
    "Max":None,
    "Cost":4,
    "desc":"Block melee attacks using weapon"
  },

  "Guardian":{
    "Max":1,
    "Cost":4,
    "Prereq":{
      "Parry":1
    },
    "desc":"Protect allies by redirecting melee attacks"
  },

  "Stamina Training":{
    "Max":1,
    "Cost":2,
    "desc":"Reduce duration of weakness effects"
  },

  "Great Stamina":{
    "Max":1,
    "Cost":4,
    "Prereq":{
      "Stamina Training":1
    },
    "desc":"Greatly reduce weakness duration further"
  },

  "Great Strike":{
    "Max":None,
    "Cost":3,
    "desc":"Increase weapon damage by two"
  },

  "Tactical Lunge":{
    "Max":1,
    "Cost":8,
    "Prereq":{
      "Great Strike":1,
      "Parry":1
    },
    "desc":"Parry after powerful offensive strike"
  },

  "Stun":{
    "Max":None,
    "Cost":3,
    "desc":"Replace damage with stunning attack"
  }
}

ARCHERY={
  "Precision":{
    "Max":1,
    "Cost":7,
    "Prereq":{
      "Bow and Arrow":1
    },
    "desc":"Increase bow damage through accuracy"
  },

  "Master Precision":{
    "Max":1,
    "Cost":7,
    "Prereq":{
      "Precision":1
    },
    "desc":"All bow attacks count as Great Strikes"
  },

  "Disarming Shot":{
    "Max":None,
    "Cost":4,
    "Prereq":{
      "Precision":1
    },
    "desc":"Bow attacks can disarm enemies"
  },

  "Pinning Shot":{
    "Max":None,
    "Cost":2,
    "Prereq":{
      "Precision":1
    },
    "desc":"Bow attacks immobilize target briefly"
  },

  "Repelling Shot":{
    "Max":None,
    "Cost":2,
    "Prereq":{
      "Pinning Shot":1
    },
    "desc":"Bow attacks push enemies backward"
  },

  "One Shot, One Kill":{
    "Max":None,
    "Cost":5,
    "Prereq":{
      "Master Precision":1,
      "Repelling Shot":1
    },
    "desc":"Bow attacks can inflict Lesser Death"
  },

  "Volley":{
    "Max":1,
    "Cost":10,
    "Prereq":{
      "Master Precision":1
    },
    "desc":"Coordinated archers deal maximum damage"
  },

  "Faster Than the Eye":{
    "Max":1,
    "Cost":8,
    "Prereq":{
      "Master Precision":1,
      "Stealth Attack":1
    },
    "desc":"Stealth bow attacks bypass defenses"
  }
}

OFFICER_TRAINING={
  "Sudden Motivation":{
    "Max":None,
    "Cost":1,
    "desc":"Quick touch removes ally weakness"
  },

  "Inspirational Speech":{
    "Max":None,
    "Cost":2,
    "desc":"Voice speech removes group weakness"
  },

  "Defensive Instruction":{
    "Max":None,
    "Cost":4,
    "Prereq":{
      "Parry":1
    },
    "desc":"Teach ally additional Parry use"
  },

  "Evasive Instruction":{
    "Max":None,
    "Cost":6,
    "Prereq":{
      "Dodge":1
    },
    "desc":"Teach ally additional Dodge use"
  },

  "Offensive Instruction":{
    "Max":None,
    "Cost":3,
    "Prereq":{
      "Great Strike":1
    },
    "desc":"Teach ally additional Great Strike"
  },

  "Military Drill":{
    "Max":1,
    "Cost":10,
    "Prereq":{"can_instruct":1},
    "desc":"Group training grants long-term combat skills"
  },

  "Self-Observation":{
    "Max":1,
    "Cost":4,
    "Prereq":{"can_instruct":1},
    "desc":"Gain benefits from your own instruction"
  }
}

THE_ART_OF_DUELING={
  "Disarm":{
    "Max":None,
    "Cost":4,
    "desc":"Disarm enemy weapons or shields on hit"
  },

  "Feint":{
    "Max":None,
    "Cost":1,
    "desc":"Recover expended attack when opponent defends"
  },

  "Invoke Challenge":{
    "Max":1,
    "Cost":5,
    "desc":"Initiate duel granting rested skill use"
  },

  "Salute":{
    "Max":1,
    "Cost":4,
    "desc":"Gain temporary armor through combat flourish"
  },

  "Stylish Hat":{
    "Max":1,
    "Cost":2,
    "Prereq":{
      "Salute":1
    },
    "desc":"Improve salute armor with stylish headgear"
  },

  "Witty Repartee":{
    "Max":1,
    "Cost":7,
    "desc":"Boost next attack with clever banter"
  },

  "Blade Dance":{
    "Max":None,
    "Cost":5,
    "Prereq":{
      "Great Strike":1,
      "Leap":1
    },
    "desc":"Leap after empowered melee strikes"
  },

  "Pure Of Heart":{
    "Max":1,
    "Cost":3,
    "desc":"Gain willpower through devotion and favor"
  }
}

THE_SCHOOL_OF_SUFFERING={
  "Armored Forearms": {
    "Max": 1,
    "Cost": 6
  },

  "Armored Shins": {
    "Max": 1,
    "Cost": 9,
    "Prereq": {
      "Armored Forearms": 1
    }
  },

  "Slow Bleeding": {
    "Max": 1,
    "Cost": 3
  },

  "Meditative Stillness": {
    "Max": 1,
    "Cost": 2,
    "Prereq": {
      "Slow Bleeding": 1
    }
  },

  "Slow Death": {
    "Max": 1,
    "Cost": 3,
    "Prereq": {
      "Meditative Stillness": 1
    }
  },

  "Torture Resistance": {
    "Max": None,
    "Cost": 3
  },

  "Torture Immunity": {
    "Max": 1,
    "Cost": 4,
    "Prereq": {
      "Torture Resistance": 3
    }
  }
}

THE_ASSASSINS_ARTS={
  "Stealth Attack":{
    "Max":1,
    "Cost":6,
    "Prereq":{"can_assassinate":1},
    "desc":"Deliver attacks while remaining undetected"
  },

  "10-Damage Strike":{
    "Max":None,
    "Cost":8,
    "Prereq":{"can_assassinate":1},
    "desc":"Single attack deals maximum damage"
  },

  "Studied Killer":{
    "Max":1,
    "Cost":6,
    "Prereq":{"Stealth Attack":1},
    "desc":"Improve effectiveness of stealth attacks"
  },

  "Twist the Knife":{
    "Max":1,
    "Cost":10,
    "Prereq":{"Stealth Attack":1},
    "desc":"Increase damage after stealth strikes"
  },

  "Shin Kick":{
    "Max":None,
    "Cost":3,
    "Prereq":{"Stun":1},
    "desc":"Deliver stun through low attack"
  },

  "Sand in Your Eyes":{
    "Max":None,
    "Cost":3,
    "Prereq":{"Stun":1},
    "desc":"Blind or impair enemy vision briefly"
  },

  "Hidden Weapon":{
    "Max":1,
    "Cost":3,
    "Prereq":{"Short Weapons":1},
    "desc":"Conceal and draw hidden weapons quickly"
  },

  "Leap":{
    "Max":None,
    "Cost":2,
    "desc":"Quick movement burst over distance"
  },

  "Leap Attack":{
    "Max":None,
    "Cost":3,
    "Prereq":{"Leap":1},
    "desc":"Attack while performing a leap"
  },

  "Deathly Vault":{
    "Max":1,
    "Cost":4,
    "Prereq":{"Stealth Attack":1,"Leap":1},
    "desc":"Combine stealth attack with vertical mobility"
  },

  "Rope Use":{
    "Max":1,
    "Cost":3,
    "desc":"Use ropes for traversal and control"
  }
}

THE_HONOURED_PATH_OF_THE_BERSERKER={
  "Battle Rage":{
    "Max":None,
    "Cost":7,
    "desc":"Enter rage state boosting attack power"
  },

  "Enduring Rage":{
    "Max":1,
    "Cost":6,
    "desc":"Heal after executing enemy deathblow"
  },

  "Hatred":{
    "Max":1,
    "Cost":4,
    "Prereq":{
      "Battle Rage":1
    },
    "desc":"Remove weakness and trigger rage"
  },

  "Berserker":{
    "Max":1,
    "Cost":10,
    "Prereq":{
      "Hatred":1
    },
    "desc":"Heal fully and enter berserk frenzy"
  },

  "Break Limb":{
    "Max":None,
    "Cost":5,
    "desc":"Injure enemy limbs with focused strikes"
  },

  "Break Shield":{
    "Max":1,
    "Cost":5,
    "Prereq":{
      "Break Limb":1,
      "Two-Handed Weapons":1
    },
    "desc":"Destroy enemy shields with heavy strikes"
  }
}

MUNDANE_HEALING={
  "Examine Wounds":{
    "Max":1,
    "Cost":2,
    "desc":"Identify target health and injury status"
  },

  "Detect Poison":{
    "Max":1,
    "Cost":2,
    "Prereq":{"Examine Wounds":1},
    "desc":"Detect whether target is poisoned"
  },

  "Administer Antidote":{
    "Max":None,
    "Cost":2,
    "Prereq":{"Detect Poison":1},
    "desc":"Remove poison through medical treatment"
  },

  "Detect Disease":{
    "Max":1,
    "Cost":2,
    "Prereq":{"Examine Wounds":1},
    "desc":"Detect whether target has disease"
  },

  "Apply Pressure":{
    "Max":1,
    "Cost":1,
    "Prereq":{"Examine Wounds":1},
    "desc":"Pause bleedout through direct pressure"
  },

  "Set Bone":{
    "Max":1,
    "Cost":3,
    "Prereq":{"Apply Pressure":1},
    "desc":"Reset broken limbs with painful correction"
  },

  "Bandage":{
    "Max":1,
    "Cost":4,
    "Prereq":{"Set Bone":1},
    "desc":"Heal minor wounds using bandages"
  },

  "Trauma Patch":{
    "Max":None,
    "Cost":4,
    "Prereq":{"Bandage":1},
    "desc":"Rapid healing using advanced bandaging"
  },

  "Surgery":{
    "Max":1,
    "Cost":5,
    "Prereq":{"Bandage":1,"Lore: Anatomy":1},
    "desc":"Perform complex medical and surgical procedures"
  },

  "Battlefield Medicine":{
    "Max":1,
    "Cost":2,
    "Prereq":{"Surgery":1},
    "desc":"Speed up surgical healing in combat"
  }
}

RELIGIOUS_WORSHIP={
    "Prayer":{
        "Max":1,
        "Cost":4,
        'Prereq':{
            'has_faith':1
        }
    },
    "Secondary Prayer":{
        "Max":1,
        "Cost":4,
        "Prereq":{
            "Priesthood":2
        }
    },
    "Tertiary Prayer":{
        "Max":1,
        "Cost":4,
        "Prereq":{
            "Priesthood":4
        }
    },
    "Priesthood":{
        "Max":4,
        "Cost":6
    },
    "Rite Mastery":{
        "Max":1,
        "Cost":4,
        "Prereq":{"Prayer":1}
    },
    "Repentance":{
        "Max":1,
        "Cost":2
    }
}

BARDIC_ARTS={
  "Commanding Presence": {
    "Max": None,
    "Cost": 3,
    "Desc": "Voice stun outside of combat"
  },

  "Serenade": {
    "Max": None,
    "Cost": 8,
    "Prereq": {"Willpower": 1},
    "Desc": "Grants shared Willpower via performance"
  },

  "Dance Lesson": {
    "Max": None,
    "Cost": 8,
    "Prereq": {"Dodge": 1},
    "Desc": "Dance grants shared Dodge ability"
  },

  "True Greatness": {
    "Max": None,
    "Cost": 4,
    "Desc": "Compliments remove Weakness temporarily"
  },

  "Drinking Song": {
    "Max": 1,
    "Cost": 6,
    "Desc": "Boosts first food effect potency"
  },

  "Meditative Song": {
    "Max": None,
    "Cost": 10,
    "Prereq": {"Mana Focus": 3},
    "Desc": "Restores mana through musical performance"
  },

  "Hymn": {
    "Max": 1,
    "Cost": 2,
    "Desc": "Shortens prayer time during rites"
  },

  "Requiem": {
    "Max": 1,
    "Cost": 3,
    "Desc": "Allows dead to hear funeral"
  }
}

MAGICAL_ARTS={
    "Mana Focus":{
        "Max":None,
        "Cost":1,
        "Prereq":{"Magical Aptitude":1}
    },
    "Alchemy":{
        "Max":4,
        "Cost":6
    },
    "Channeling":{
        "Max":4,
        "Cost":6
    },
    "Divination":{
        "Max":4,
        "Cost":6
    },
    "Sorcery":{
        "Max":4,
        "Cost":6
    },
    "Warding":{
        "Max":4,
        "Cost":6
    },
    "Weapon Casting":{
        "Max":1,
        "Cost":8,
        "Prereq":{"Magical Aptitude":1}
    },
    "Elemental Flourish":{
        "Max":1,
        "Cost":4,
        "Prereq":{"Sorcery":1,"Great Strike":1}
    },
    "Armored Casting":{
        "Max":1,
        "Cost":6,
        "Prereq":{"Magical Aptitude":1}
    },
    "Combat Mimic":{
        "Max":None,
        "Cost":4,
        "Prereq":{"Weapon Casting":1}
    },
    "Internal Reserves":{
        "Max":1,
        "Cost":4,
        "Prereq":{"Mana Focus":10}
    },
    "Arcane Tutelage":{
        "Max":1,
        "Cost":10,
        "Prereq":{"gm_mage":1,"Research":1}
    },
    "Arcane Observation":{
        "Max":1,
        "Cost":4,
        "Prereq":{"Arcane Tutelage":1}
    },
    "Spellwright":{
        "Max":1,
        "Cost":2,
        "Prereq":{"gm_mage":1,"Research":1}
    }
}

SKULLDUGGERY={
"Disguise": {
"Max": 1,
"Cost": 4,
"Desc": "Deceptive identity concealment with lying allowed"
},

"Master Disguise": {
"Max": 1,
"Cost": 6,
"Prereq": {
"Disguise": 1
},
"Desc": "Cross-bloodline disguise including race alteration"
},

"Detect Disguise": {
"Max": 1,
"Cost": 4,
"Desc": "Reveal hidden disguises after close observation"
},

"Escape": {
"Max": None,
"Cost": 3,
"Desc": "Instantly break free from restraints"
},

"Poison Resistance": {
"Max": None,
"Cost": 2,
"Desc": "End or resist poison effects"
},

"Poison Immunity": {
"Max": 1,
"Cost": 4,
"Prereq": {
"Poison Resistance": 3
},
"Desc": "Complete immunity against all poisons"
},

"Lockpicking": {
"Max": 1,
"Cost": 4,
"Desc": "Open locked objects using tools"
},

"Gambling": {
"Max": None,
"Cost": 2,
"Desc": "Re-roll dice or redraw cards"
},

"Torture": {
"Max": None,
"Cost": 2,
"Desc": "Extract truthful answers through pain"
}
}

KNOWLEDGE={
    "Lore":{
        "Max":1,
        "Cost":4
    },
    "Research":{
        "Max":1,
        "Cost":6,
        "Prereq":{"Literate":0}
    },
    "Alchemical Examination":{
        "Max":1,
        "Cost":3,
        "Prereq":{"Lore: Alchemy":1}
    }
}

GATHERING={
    "Academic Standing":{
        "Max":4,
        "Cost":4
    },
    "Economic Standing":{
        "Max":4,
        "Cost":4
    },
    "Military Standing":{
        "Max":4,
        "Cost":4
    },
    "Political Standing":{
        "Max":4,
        "Cost":4
    },
    "Underworld Standing":{
        "Max":4,
        "Cost":4
    },
    "Mining":{
        "Max":4,
        "Cost":4
    },
    "Herbalism":{
        "Max":4,
        "Cost":4
    },
    "Woodcutting":{
        "Max":4,
        "Cost":4
    },
    "Hunting":{
        "Max":4,
        "Cost":4
    },
    "Mercantile":{
        "Max":4,
        "Cost":4
    },
    "Black Market":{
        "Max":4,
        "Cost":4
    }
}

CRAFTING_SKILLS={
    "Fortify Armor":{
        "Max":1,
        "Cost":3,
        "Prereqs":{"can_fortify":1}
    },
    "Field Repair":{
        "Max":None,
        "Cost":2,
        "Prereq":{"can_field_repair":1}
    },
    "Repair Shield":{
        "Max":1,
        "Cost":3,
        "Prereq":{"Shieldsmithing":1}
    },
    "Recipe Scribing":{
        "Max":1,
        "Cost":2,
        "Prereq":{"Scroll Scribing":1}
    },
    "New Edition":{
        "Max":1,
        "Cost":3,
        "Prereq":{"Scroll Scribing":1}
    },
    "Grand Feast":{
        "Max":1,
        "Cost":10,
        "Prereq":{"Cooking":4}
    },
    "Reconstruct":{
        "Max":1,
        "Cost":1,
        "Prereq":{"is_crafter":1}
    },
    "Inventor":{
        "Max":1,
        "Cost":2,
        "Prereq":{"can_invent":1,"Research":1}
    }
}

LORE={
    "Lore: Alchemy": {"Max": 1, "Cost": 4},
    "Lore: Celestials": {"Max": 1, "Cost": 4},
    "Lore: Church of Chorus": {"Max": 1, "Cost": 4},
    "Lore: War of Wine": {"Max": 1, "Cost": 4},
    "Lore: Rules of Society": {"Max": 1, "Cost": 4},

    "Lore: Blood Magic": {"Max": 1, "Cost": 4},
    "Lore: Amalgamation": {"Max": 1, "Cost": 4},
    "Lore: Demons": {"Max": 1, "Cost": 4},
    "Lore: Old Ways": {"Max": 1, "Cost": 4},
    "Lore: Purges": {"Max": 1, "Cost": 4},
    "Lore: Nature": {"Max": 1, "Cost": 4},

    "Lore: Channeling": {"Max": 1, "Cost": 4},
    "Lore: Fae": {"Max": 1, "Cost": 4},
    "Lore: Dragon Worship": {"Max": 1, "Cost": 4},
    "Lore: The First Crusade": {"Max": 1, "Cost": 4},
    "Lore: Anatomy": {"Max": 1, "Cost": 4},

    "Lore: Divination": {"Max": 1, "Cost": 4},
    "Lore: Dragons": {"Max": 1, "Cost": 4},
    "Lore: The Celestine Faith": {"Max": 1, "Cost": 4},
    "Lore: The War Of Radiance": {"Max": 1, "Cost": 4},
    "Lore: Medicine": {"Max": 1, "Cost": 4},

    "Lore: Dream": {"Max": 1, "Cost": 4},
    "Lore: Undead": {"Max": 1, "Cost": 4},
    "Lore: The Lady of the Mists": {"Max": 1, "Cost": 4},
    "Lore: The Second Crusade": {"Max": 1, "Cost": 4},

    "Lore: Necromancy": {"Max": 1, "Cost": 4},
    "Lore: The Nameless Faith": {"Max": 1, "Cost": 4},
    "Lore: The War of Giants": {"Max": 1, "Cost": 4},

    "Lore: Sorcery": {"Max": 1, "Cost": 4},
    "Lore: Trahazi Zodiac": {"Max": 1, "Cost": 4},

    "Lore: Summoning": {"Max": 1, "Cost": 4},
    "Lore: The Blood Cauldron": {"Max": 1, "Cost": 4},

    "Lore: Warding": {"Max": 1, "Cost": 4},
    "Lore: Demon Faiths": {"Max": 1, "Cost": 4},

    "Lore: Rituals": {"Max": 1, "Cost": 4},
    "Lore: Dace": {"Max": 1, "Cost": 4}
}

CRAFTING_CIRCLES = {
    "Blacksmithing": {"Max": 4, "Cost": 6},
    "Weaponsmithing": {"Max": 4, "Cost": 6},
    "Armorsmithing": {"Max": 4, "Cost": 6},
    "Shieldsmithing": {"Max": 4, "Cost": 6},
    "Locksmithing": {"Max": 4, "Cost": 6},
    "Enchanting": {"Max": 4, "Cost": 6},
    "Scroll Scribing": {"Max": 4, "Cost": 6},
    "Artificing": {"Max": 4, "Cost": 6},
    "Cooking": {"Max": 4, "Cost": 6},
    "Stable Alchemy": {"Max": 4, "Cost": 6},
    "Tailoring": {"Max": 4, "Cost": 6},
    "Fletching": {"Max": 4, "Cost": 6},
    "Engineering": {"Max": 4, "Cost": 6}
}

