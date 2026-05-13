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

WEAPON_PROFICIENCIES = {
    "Short Weapons": {
    "Max": 1,
    "Cost": 1
    },

    "One-Handed Weapons": {
    "Max": 1,
    "Cost": 2,
    "Prereq": {
        "Short Weapons": 1
    }
    },

    "Two-Handed Weapons": {
    "Max": 1,
    "Cost": 3,
    "Prereq": {
        "One-Handed Weapons": 1
    }
    },

    "Oversized Weapon Use": {
    "Max": 1,
    "Cost": 2,
    "Prereq": {
        "Two-Handed Weapons": 1
    }
    },

    "Thrown Weapons": {
    "Max": 1,
    "Cost": 2
    },

    "Bow and Arrow": {
    "Max": 1,
    "Cost": 3
    },

    "Two-Weapon Fighting": {
    "Max": 1,
    "Cost": 6
    }}

ARMOR_PROFICIENCIES = {

    "Armor Training: Light": {
    "Max": 1,
    "Cost": 2
    },

    "Armor Training: Heavy": {
    "Max": 1,
    "Cost": 2,
    "Prereq": {
        "Armor Training: Light": 1
    }
    },

    "Shield Use": {
    "Max": 1,
    "Cost": 2
    },

    "Helmet Mastery": {
    "Max": 1,
    "Cost": 2
    }}

GENERAL_COMBAT_SKILLS={
  "Toughness": {
    "Max": 5,
    "Cost": 3
  },

  "Dodge": {
    "Max": None,
    "Cost": 6
  },

  "Willpower": {
    "Max": None,
    "Cost": 6
  },

  "Parry": {
    "Max": None,
    "Cost": 4
  },

  "Guardian": {
    "Max": 1,
    "Cost": 4,
    "Prereq": {
      "Parry": 1
    }
  },

  "Stamina Training": {
    "Max": 1,
    "Cost": 2
  },

  "Great Stamina": {
    "Max": 1,
    "Cost": 4,
    "Prereq": {
      "Stamina Training": 1
    }
  },

  "Great Strike": {
    "Max": None,
    "Cost": 3
  },

  "Tactical Lunge": {
    "Max": 1,
    "Cost": 8,
    "Prereq": {
      "Great Strike": 1,
      "Parry": 1
    }
  },
  "Stun": {
    "Max": None,
    "Cost": 3
  }
}

ARCHERY={
  "Precision": {
    "Max": 1,
    "Cost": 7,
    "Prereq": {
      "Bow and Arrow": 1
    }
  },

  "Master Precision": {
    "Max": 1,
    "Cost": 7,
    "Prereq": {
      "Precision": 1
    }
  },

  "Disarming Shot": {
    "Max": None,
    "Cost": 4,
    "Prereq": {
      "Precision": 1
    }
  },

  "Pinning Shot": {
    "Max": None,
    "Cost": 2,
    "Prereq": {
      "Precision": 1
    }
  },

  "Repelling Shot": {
    "Max": None,
    "Cost": 2,
    "Prereq": {
      "Pinning Shot": 1
    }
  },

  "One Shot, One Kill": {
    "Max": None,
    "Cost": 5,
    "Prereq": {
      "Master Precision": 1,
      "Repelling Shot": 1
    }
  },

  "Volley": {
    "Max": 1,
    "Cost": 10,
    "Prereq": {
      "Master Precision": 1
    }
  },

  "Faster Than the Eye": {
    "Max": 1,
    "Cost": 8,
    "Prereq": {
      "Master Precision": 1,
      "Stealth Attack": 1
    }
  }
}

OFFICER_TRAINING={
  "Sudden Motivation": {
    "Max": None,
    "Cost": 1
  },

  "Inspirational Speech": {
    "Max": None,
    "Cost": 2
  },

  "Defensive Instruction": {
    "Max": None,
    "Cost": 4,
    "Prereq": {
      "Parry": 1
    }
  },

  "Evasive Instruction": {
    "Max": None,
    "Cost": 6,
    "Prereq": {
      "Dodge": 1
    }
  },

  "Offensive Instruction": {
    "Max": None,
    "Cost": 3,
    "Prereq": {
      "Great Strike": 1
    }
  },

  "Military Drill": {
    "Max": 1,
    "Cost": 10,
    "Prereq": {"can_instruct":1}
  },

  "Self-Observation": {
    "Max": 1,
    "Cost": 4,
    "Prereq": {"can_instruct":1}
  }
}

THE_ART_OF_DUELING={
  "Disarm": {
    "Max": None,
    "Cost": 4
  },

  "Feint": {
    "Max": None,
    "Cost": 1
  },

  "Invoke Challenge": {
    "Max": 1,
    "Cost": 5
  },

  "Salute": {
    "Max": 1,
    "Cost": 4
  },

  "Stylish Hat": {
    "Max": 1,
    "Cost": 2,
    "Prereq": {
      "Salute": 1
    }
  },

  "Witty Repartee": {
    "Max": 1,
    "Cost": 7
  },

  "Blade Dance": {
    "Max": None,
    "Cost": 5,
    "Prereq": {
      "Great Strike": 1,
      "Leap": 1
    }
  },

  "Pure Of Heart": {
    "Max": 1,
    "Cost": 3
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
  "Stealth Attack": {
    "Max": 1,
    "Cost": 6,
    "Prereq": {"can_assassinate":1}
  },

  "10-Damage Strike": {
    "Max": None,
    "Cost": 8,
    "Prereq": {"can_assassinate":1}
  },

  "Studied Killer": {
    "Max": 1,
    "Cost": 6,
    "Prereq": {
      "Stealth Attack": 1
    }
  },

  "Twist the Knife": {
    "Max": 1,
    "Cost": 10,
    "Prereq": {
      "Stealth Attack": 1
    }
  },

  "Shin Kick": {
    "Max": None,
    "Cost": 3,
    "Prereq": {
      "Stun": 1
    }
  },

  "Sand in Your Eyes": {
    "Max": None,
    "Cost": 3,
    "Prereq": {
      "Stun": 1
    }
  },

  "Hidden Weapon": {
    "Max": 1,
    "Cost": 3,
    "Prereq": {
      "Short Weapons": 1
    }
  },

  "Leap": {
    "Max": None,
    "Cost": 2
  },

  "Leap Attack": {
    "Max": None,
    "Cost": 3,
    "Prereq": {
      "Leap": 1
    }
  },

  "Deathly Vault": {
    "Max": 1,
    "Cost": 4,
    "Prereq": {
      "Stealth Attack": 1,
      "Leap": 1
    }
  },

  "Rope Use": {
    "Max": 1,
    "Cost": 3
  }
}

THE_HONOURED_PATH_OF_THE_BERSERKER={
  "Battle Rage": {
    "Max": None,
    "Cost": 7
  },

  "Enduring Rage": {
    "Max": 1,
    "Cost": 6
  },

  "Hatred": {
    "Max": 1,
    "Cost": 4,
    "Prereq": {
      "Battle Rage": 1
    }
  },

  "Berserker": {
    "Max": 1,
    "Cost": 10,
    "Prereq": {
      "Hatred": 1
    }
  },

  "Break Limb": {
    "Max": None,
    "Cost": 5
  },

  "Break Shield": {
    "Max": 1,
    "Cost": 5,
    "Prereq": {
      "Break Limb": 1,
      "Two-Handed Weapons": 1
    }
  }
}

MUNDANE_HEALING={
  "Examine Wounds": {
    "Max": 1,
    "Cost": 2
  },

  "Detect Poison": {
    "Max": 1,
    "Cost": 2,
    "Prereq": {
      "Examine Wounds": 1
    }
  },

  "Administer Antidote": {
    "Max": None,
    "Cost": 2,
    "Prereq": {
      "Detect Poison": 1
    }
  },

  "Detect Disease": {
    "Max": 1,
    "Cost": 2,
    "Prereq": {
      "Examine Wounds": 1
    }
  },

  "Apply Pressure": {
    "Max": 1,
    "Cost": 1,
    "Prereq": {
      "Examine Wounds": 1
    }
  },

  "Set Bone": {
    "Max": 1,
    "Cost": 3,
    "Prereq": {
      "Apply Pressure": 1
    }
  },

  "Bandage": {
    "Max": 1,
    "Cost": 4,
    "Prereq": {
      "Set Bone": 1
    }
  },

  "Trauma Patch": {
    "Max": None,
    "Cost": 4,
    "Prereq": {
      "Bandage": 1
    }
  },

  "Surgery": {
    "Max": 1,
    "Cost": 5,
    "Prereq": {
      "Bandage": 1,
      "Lore: Anatomy": 1
    }
  },

  "Battlefield Medicine": {
    "Max": 1,
    "Cost": 2,
    "Prereq": {
      "Surgery": 1
    }
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

THE_BARDIC_ARTS={
  "Commanding Presence": {
    "Max": None,
    "Cost": 3
  },

  "Serenade": {
    "Max": None,
    "Cost": 8,
    "Prereq": {
      "Willpower": 1
    }
  },

  "Dance Lesson": {
    "Max": None,
    "Cost": 8,
    "Prereq": {
      "Dodge": 1
    }
  },

  "True Greatness": {
    "Max": None,
    "Cost": 4
  },

  "Drinking Song": {
    "Max": 1,
    "Cost": 6
  },

  "Meditative Song": {
    "Max": None,
    "Cost": 10,
    "Prereq": {
      "Mana Focus": 3
    }
  },

  "Hymn": {
    "Max": 1,
    "Cost": 2
  },

  "Requiem": {
    "Max": 1,
    "Cost": 3
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
    "Cost": 4
  },

  "Master Disguise": {
    "Max": 1,
    "Cost": 6,
    "Prereq": {
      "Disguise": 1
    }
  },

  "Detect Disguise": {
    "Max": 1,
    "Cost": 4
  },

  "Escape": {
    "Max": None,
    "Cost": 3
  },

  "Poison Resistance": {
    "Max": None,
    "Cost": 2
  },

  "Poison Immunity": {
    "Max": 1,
    "Cost": 4,
    "Prereq": {
      "Poison Resistance": 3
    }
  },
  "Lockpicking": {
    "Max": 1,
    "Cost": 4
  },
  "Gambling": {
    "Max": None,
    "Cost": 2
  },
  "Torture": {
    "Max": None,
    "Cost": 2
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

