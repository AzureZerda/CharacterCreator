BACKGROUND_FEATURES={
'Magical Aptitude':{
'Max':1,
'Cost':4,
'desc':'Required to learn and use magic'
},
'Prophetic Dreamer':{
'Max':1,
'Cost':4,
'desc':'After 30 minutes of role-play, you may report to NPC camp and tell an available story staff member that you have used PROPHETIC DREAMER and would like to know about the single greatest threat or incursion likely to enter the gamespace in the next 3 hours. You may ask ONE yes-or-no question about the threat or incursion you have just learned of.'
},
'Nobility':{
'Max':1,
'Cost':6,
'desc':'You may wear 3 pins of status. You should seek out an OOC resource on the “Rules of Society” to understand how nobility fits within the game world and any privileges or responsibilities you have as a result.'
},
'Military Experience':{
'Max':None,
'Cost':4,
'desc':'You may call “Bid: Military Experience (Nation)” and ask a question to a Twin Mask Story Staff member to potentially get extra information or detail on a situation.'
},
'Bardic Knowledge':{
'Max':1,
'Cost':4,
'desc':'You may call “Bid: Bardic Knowledge” and ask a question to a Twin Mask Story Staff member to potentially gain extra information about a situation.'
}
}

BACKGROUND_FLAWS={
'Sovereign Zeal':{
'Max':1,
'Cost':-2,
'desc':'Whenever you physically hear an insult to your nation/culture (that is, any nation/culture for which you have NATIVE LORE), you must verbally answer and challenge that insult. If you choose not to do this, you lose access to all skills or spells beyond the ones in the “Weapon Proficiencies” and “Armor Proficiencies” sections for 30 minutes.'
},

'Religious Zeal':{
'Max':1,
'Cost':-2,
'desc':'Whenever you physically hear an insult to your religion (that is, the religion printed on your character sheet), you must verbally answer and challenge that insult. If you choose not to do this, you lose access to all skills or spells beyond the ones in the “Weapon Proficiencies” and “Armor Proficiencies” sections for 30 minutes.'
},

'Corrupted':{
'Max':1,
'Cost':-6,
'desc':'You begin the game with +1 Corruption. This notably increases the likelihood of your character permanently dying.'
},

'Frail':{
'Max':None,
'Cost':-3,
'desc':'You begin the game with a permanent -1 maximum Health Points (HP) for every rank in this flaw.'
},

'Clouded Memory':{
'Max':1,
'Cost':-2,
'desc':'You start the game with only a very rudimentary backstory. (It still must include mention that your character died.) Over the course of one year of real time, you should work with your NPL to fill out your character’s “Backstory” tab on the character sheet as you learn more about the world of Twin Mask.'
},

'Fractured Memory':{
'Max':1,
'Cost':-4,
'desc':'You have holes in your memory that can never be filled. These holes can be defined in the “Backstory” tab on your character sheet as missing sections, or left purely to role-play, at your option. No spell, ability, or amount of role-play can ever recover these memories. Twin Mask Story Staff may fill in the holes with information about the world, but this will still not recover the memories; you will simply have learned anew about events from your past.'
},

'Fading Memory':{
'Max':1,
'Cost':-4,
'desc':'You start with a fully fleshed-out backstory, but over the course of one year in real time you must role-play the process of forgetting that entire backstory, culminating in remembering nothing about your past. No spell, ability, or amount of role-play can ever recover these memories. You may learn about events from your past, but these are not memories; you will simply have learned anew about events you have now forgotten.'
},

'Illiterate':{
'Max':1,
'Cost':-4,
'desc':'You must role-play being unable to read written text in-game. You are also incapable of writing, which will greatly complicate your ability to use the postal system and certain Influence actions. Spellcasting via scrolls is still possible if you have the appropriate LORE and MAGIC skills.'
},

'Oathbound':{
'Max':1,
'Cost':-6,
'desc':'Whenever you give a formal oath within the world of Twin Mask, you are bound to keep it. Failure to do so gives +1 Corruption per broken oath (reported to NPC camp). Magical compulsion prevents penalty if resisted appropriately.'
}
}

WEAPON_PROFICIENCIES={
    "Short Weapons":{
        "Max":1,
        "Cost":1,
        "desc":"You may wield and use weapons up to 24 inches in length."
    },

    "One-Handed Weapons":{
        "Max":1,
        "Cost":2,
        "Prereq":{
            "Short Weapons":1
        },
        "desc":"You may wield and use weapons up to 48 inches in length."
    },

    "Two-Handed Weapons":{
        "Max":1,
        "Cost":3,
        "Prereq":{
            "One-Handed Weapons":1
        },
        "desc":"You may wield and use weapons of any length, as long as they are wielded in two hands."
    },

    "Oversized Weapon Use":{
        "Max":1,
        "Cost":2,
        "Prereq":{
            "Two-Handed Weapons":1
        },
        "desc":"You may wield and use weapons of any length in one hand."
    },

    "Thrown Weapons":{
        "Max":1,
        "Cost":2,
        "desc":"You may wield and use thrown weapons."
    },

    "Bow and Arrow":{
        "Max":1,
        "Cost":3,
        "desc":"You may wield and use a bow."
    },

    "Two-Weapon Fighting":{
        "Max":1,
        "Cost":6,
        "desc":"You may wield and use two weapons at once. You must have the required skills to use each of those weapons—this skill does not confer the ability to use weapons by itself."
    }
}

ARMOR_PROFICIENCIES={
    "Armor Training: Light":{
        "Max":1,
        "Cost":2,
        "desc":"You may wear and benefit from light armor, providing a base armor value of 7 points when worn."
    },

    "Armor Training: Heavy":{
        "Max":1,
        "Cost":2,
        "Prereq":{
            "Armor Training: Light":1
        },
        "desc":"You may wear and benefit from heavy armor, providing a base armor value of 15 points when worn."
    },

    "Shield Use":{
        "Max":1,
        "Cost":2,
        "desc":"You may wear and benefit from a single shield with no dimension longer than the distance from the wielder’s navel to the ground, or you can wear and benefit from a buckler-sized shield, as explained above."
    },

    "Helmet Mastery":{
        "Max":1,
        "Cost":2,
        "desc":"You may call “No Effect” to Stuns while wearing a helmet."
    }
}

GENERAL_COMBAT_SKILLS={
  "Toughness":{
    "Max":5,
    "Cost":3,
    "desc":"Increases your Health Points (HP) by 1. This skill may be taken no more than 5 times."
  },

  "Dodge":{
    "Max":None,
    "Cost":6,
    "desc":"You may call “Dodge” to prevent an effect that physically strikes you, including weapons, spell packets, thrown weapons, and touch attacks."
  },

  "Willpower":{
    "Max":None,
    "Cost":6,
    "desc":"You may call “Willpower” to prevent any effect that does not physically touch you, such as a call delivered by voice, gesture, gaze, ward, or ingested potion."
  },

  "Parry":{
    "Max":None,
    "Cost":4,
    "desc":"You may call “Parry” to negate the effect of an attack delivered by a melee weapon."
  },

  "Guardian":{
    "Max":1,
    "Cost":4,
    "Prereq":{
      "Parry":1
    },
    "desc":"You may expend a use of PARRY and call “Guard Parry” to negate the effect of a melee attack or deathblow against someone else within arm’s reach. If you Guard Parry a deathblow, that target will be immune to deathblows for 3 seconds."
  },

  "Stamina Training":{
    "Max":1,
    "Cost":2,
    "desc":"Reduces the duration of the “Weakness” effect on you by one minute, down to 2 minutes."
  },

  "Great Stamina":{
    "Max":1,
    "Cost":4,
    "Prereq":{
      "Stamina Training":1
    },
    "desc":"Reduces the duration of the “Weakness” effect by an additional minute, down to 1 minute."
  },

  "Great Strike":{
    "Max":None,
    "Cost":3,
    "desc":"You may add +2 damage to a weapon attack. Only one Great Strike effect may apply to any particular weapon attack."
  },

  "Tactical Lunge":{
    "Max":1,
    "Cost":8,
    "Prereq":{
      "Great Strike":1,
      "Parry":1
    },
    "desc":"Within 3 seconds of performing a Great Strike, you may call “Parry” without expending a use of the PARRY skill to negate the effect of an attack delivered by a melee weapon. This ability may not be used more than once every 30 seconds."
  },

  "Stun":{
    "Max":None,
    "Cost":3,
    "desc":"You may call “Stun” instead of damage when you make an attack with a weapon."
  }
}

ARCHERY={
  "Precision":{
    "Max":1,
    "Cost":7,
    "Prereq":{
      "Bow and Arrow":1
    },
    "desc":"You deal +2 damage with every attack you make using a bow."
  },

  "Master Precision":{
    "Max":1,
    "Cost":7,
    "Prereq":{
      "Precision":1
    },
    "desc":"You treat every attack you make with a bow as a Great Strike."
  },

  "Disarming Shot":{
    "Max":None,
    "Cost":4,
    "Prereq":{
      "Precision":1
    },
    "desc":"You may call “Disarm” instead of damage when attacking with a bow."
  },

  "Pinning Shot":{
    "Max":None,
    "Cost":2,
    "Prereq":{
      "Precision":1
    },
    "desc":"You may call “Bind” instead of damage when attacking with a bow."
  },

  "Repelling Shot":{
    "Max":None,
    "Cost":2,
    "Prereq":{
      "Pinning Shot":1
    },
    "desc":"You may call “Repel” instead of damage when attacking with a bow."
  },

  "One Shot, One Kill":{
    "Max":None,
    "Cost":5,
    "Prereq":{
      "Master Precision":1,
      "Repelling Shot":1
    },
    "desc":"You may call “Lesser Death” instead of damage when attacking with a bow."
  },

  "Volley":{
    "Max":1,
    "Cost":10,
    "Prereq":{
      "Master Precision":1
    },
    "desc":"You may call “Loose!” “Volley!” or “Fire!” in a group of three or more archers within arm’s reach of each other. If all archers in that group shoot simultaneously, they call “10” rather than their normal damage."
  },

  "Faster Than the Eye":{
    "Max":1,
    "Cost":8,
    "Prereq":{
      "Master Precision":1,
      "Stealth Attack":1
    },
    "desc":"You may call “Stealth” for every attack you make with a bow."
  }
}

OFFICER_TRAINING={
  "Sudden Motivation":{
    "Max":None,
    "Cost":1,
    "desc":"You may role-play 3 seconds of verbal motivation while in physical contact with another character and call “Remove Weakness.”"
  },

  "Inspirational Speech":{
    "Max":None,
    "Cost":2,
    "desc":"You may role-play 30 seconds of delivering a motivational speech and call “By My Voice: Remove Weakness.”"
  },

  "Defensive Instruction":{
    "Max":None,
    "Cost":4,
    "Prereq":{
      "Parry":1
    },
    "desc":"You may role-play 30 seconds of defensive combat instruction with another character and call “Bestow Parry.” You must explain that this bestowed effect lasts for 30 minutes or until used."
  },

  "Evasive Instruction":{
    "Max":None,
    "Cost":6,
    "Prereq":{
      "Dodge":1
    },
    "desc":"You may role-play 30 seconds of evasive combat instruction with another character and call “Bestow Dodge.” You must explain that this bestowed effect lasts for 30 minutes or until used."
  },

  "Offensive Instruction":{
    "Max":None,
    "Cost":3,
    "Prereq":{
      "Great Strike":1
    },
    "desc":"You may role-play 30 seconds of offensive combat instruction with another character and call “Bestow Great Strike.” You must explain that this bestowed effect lasts for 30 minutes or until used."
  },

  "Military Drill":{
    "Max":1,
    "Cost":10,
    "Prereq":{"can_instruct":1},
    "desc":"You may role-play thirty minutes of combat instruction with a group and call “Bestow Parry,” “Bestow Dodge,” and/or “Bestow Great Strike,” based on which INSTRUCTION skills you possess. You must explain that these bestowed effects last for the entire Twin Mask event and return with rest."
  },

  "Self-Observation":{
    "Max":1,
    "Cost":4,
    "Prereq":{"can_instruct":1},
    "desc":"You receive the benefits of your own DEFENSIVE INSTRUCTION, EVASIVE INSTRUCTION, OFFENSIVE INSTRUCTION, and MILITARY DRILL."
  }
}

THE_ART_OF_DUELING={
  "Disarm":{
    "Max":None,
    "Cost":4,
    "desc":"You may call “Disarm” instead of damage when making a melee attack with a SHORT or ONE-HANDED weapon if your other hand is completely empty. You may call this effect even if you strike a weapon or shield."
  },

  "Feint":{
    "Max":None,
    "Cost":1,
    "desc":"You may call “Feint” to regain use of an expended melee weapon or touch attack when an opponent uses PARRY OR DODGE to counter you, as long as you are wielding a SHORT or ONE-HANDED weapon and have your other hand completely empty."
  },

  "Invoke Challenge":{
    "Max":1,
    "Cost":5,
    "desc":"You may clearly and verbally challenge a character, or group of characters, to a duel. If they clearly and verbally accept your challenge, you may use all your “Returns with Rest” skills, but not items, as if you had just completed a rest. Simply attacking you does NOT count as accepting your challenge. If any participants in the duel attack, or are attacked, by non-participants, all “Returns with Rest” skills that came back due to this skill immediately go on cooldown."
  },

  "Salute":{
    "Max":1,
    "Cost":4,
    "desc":"You may call “Bestow Self 3 Armor” after a 3-second salute or flourish with your weapon. The armor lasts until used or until there are no nearby enemies for at least 30 seconds."
  },

  "Stylish Hat":{
    "Max":1,
    "Cost":2,
    "Prereq":{
      "Salute":1
    },
    "desc":"You may call “Bestow Self 5 Armor” when you perform the SALUTE skill if you are wearing an impressive piece of headgear."
  },

  "Witty Repartee":{
    "Max":1,
    "Cost":7,
    "desc":"You may spend 3 seconds making a clever quip or insult, after which your next melee weapon attack within 30 seconds functions as a Great Strike."
  },

  "Blade Dance":{
    "Max":None,
    "Cost":5,
    "Prereq":{
      "Great Strike":1,
      "Leap":1
    },
    "desc":"Within 3 seconds of performing a Great Strike, you may call “Leap” without expending a use of the LEAP skill and take 3 steps in any one direction, immune to DODGE-able attacks. This ability may not be used more than once every 30 seconds."
  },

  "Pure Of Heart":{
    "Max":1,
    "Cost":3,
    "desc":"You may use this skill as if it were a WILLPOWER while you wear your token of devotion prominently."
  }
}

THE_SCHOOL_OF_SUFFERING={
  "Armored Forearms":{
    "Max":1,
    "Cost":6,
    "desc":"Non-touch attacks other than BREAK LIMB that strike your forearms and hands count as though they have hit a shield."
  },

  "Armored Shins":{
    "Max":1,
    "Cost":9,
    "Prereq":{
      "Armored Forearms":1
    },
    "desc":"Non-touch attacks other than BREAK LIMB that strike your shins and feet count as though they have hit a shield."
  },

  "Slow Bleeding":{
    "Max":1,
    "Cost":3,
    "desc":"Your bleedout timer increases by 3 minutes permanently."
  },

  "Meditative Stillness":{
    "Max":1,
    "Cost":2,
    "Prereq":{
      "Slow Bleeding":1
    },
    "desc":"You may answer “Dead” whenever an effect attempts to detect whether you are living."
  },

  "Slow Death":{
    "Max":1,
    "Cost":3,
    "Prereq":{
      "Meditative Stillness":1
    },
    "desc":"Your death count increases by 3 minutes permanently."
  },

  "Torture Resistance":{
    "Max":None,
    "Cost":3,
    "desc":"You may call “Resist” when a character calls “Torture” against you. This skill may be used in Weakness and Bleedout."
  },

  "Torture Immunity":{
    "Max":1,
    "Cost":4,
    "Prereq":{
      "Torture Resistance":3
    },
    "desc":"You may call “No Effect” when a character calls “Torture” against you as often as you wish. This skill may be used in Weakness and Bleedout."
  }
}

THE_ASSASSINS_ARTS={
  "Stealth Attack":{
    "Max":1,
    "Cost":6,
    "Prereq":{"can_assassinate":1},
    "desc":"You may call “Stealth” in addition to the normal attack call when you land an attack with a Short or Thrown Weapon, or a bow, against a target’s back. This bypasses their armor to damage their Health Points directly, and prevents them from countering with Dodge, Parry, or Willpower."
  },

  "10-Damage Strike":{
    "Max":None,
    "Cost":8,
    "Prereq":{"can_assassinate":1},
    "desc":"You may call “10” for an attack with a Short Weapon, Thrown Weapon, or bow."
  },

  "Studied Killer":{
    "Max":1,
    "Cost":6,
    "Prereq":{"Stealth Attack":1},
    "desc":"You may spend 30 uninterrupted seconds within arm’s reach of another character and call “Stealth” for your next melee attack against them, regardless of where the attack lands."
  },

  "Twist the Knife":{
    "Max":1,
    "Cost":10,
    "Prereq":{"Stealth Attack":1},
    "desc":"Every melee STEALTH ATTACK that you make with a SHORT WEAPON functions as a Great Strike."
  },

  "Shin Kick":{
    "Max":None,
    "Cost":3,
    "Prereq":{"Stun":1},
    "desc":"You may make a touch attack against a character that is not actively hostile and call “Stun.”"
  },

  "Sand in Your Eyes":{
    "Max":None,
    "Cost":3,
    "Prereq":{"Stun":1},
    "desc":"You may throw a packet and call “Stun.”"
  },

  "Hidden Weapon":{
    "Max":1,
    "Cost":3,
    "Prereq":{"Short Weapons":1},
    "desc":"You may tie a white ribbon around a SHORT WEAPON and make a reasonable effort to hide it. Other characters must role-play as though it does not exist until you reveal it or it is found via magic."
  },

  "Leap":{
    "Max":None,
    "Cost":2,
    "desc":"You may raise your hands above your head, call “Leap,” and take 3 steps in any direction, during which time you are Airborne and cannot be affected by anything that could be countered by the DODGE skill. You must land with at least 3 limbs touching the ground before you can move again."
  },

  "Leap Attack":{
    "Max":None,
    "Cost":3,
    "Prereq":{"Leap":1},
    "desc":"You may make a single melee weapon attack during the 3 steps you take as part of LEAP."
  },

  "Deathly Vault":{
    "Max":1,
    "Cost":4,
    "Prereq":{"Stealth Attack":1,"Leap":1},
    "desc":"Within 30 seconds of performing a deathblow on a target you personally put into bleedout, you may call “Leap” without expending a use of the LEAP skill and take three steps in any one direction, during which time you may not be affected by any attacks that could be countered by a DODGE. This ability may not be used more than once every 30 seconds."
  },

  "Rope Use":{
    "Max":1,
    "Cost":3,
    "desc":"You may role-play binding a character with a rope phys-rep for 3 seconds while explaining how ROPE USE works. They may not escape these bindings without a use of ESCAPE, or a bladed weapon wielded by themselves or others."
  }
}

THE_HONOURED_PATH_OF_THE_BERSERKER={
  "Battle Rage":{
    "Max":None,
    "Cost":7,
    "desc":"You may call “Rage” and start a 10-second timer during which all weapon attacks function as Great Strikes."
  },

  "Enduring Rage":{
    "Max":1,
    "Cost":6,
    "desc":"You must speak for 3 seconds to a character you have put into bleedout, perform a deathblow, and then may call, “Heal Self 2.” This skill does not work if you did not perform the attack that put the character into bleedout."
  },

  "Hatred":{
    "Max":1,
    "Cost":4,
    "Prereq":{
      "Battle Rage":1
    },
    "desc":"You must role-play a moment of rage and motivation, after which you may call “Remove Weakness, Rage!” and immediately begin an available use of your BATTLE RAGE skill. If you have no available uses of BATTLE RAGE, this skill cannot be used."
  },

  "Berserker":{
    "Max":1,
    "Cost":10,
    "Prereq":{
      "Hatred":1
    },
    "desc":"Once per game, you may call “Berserker!” within 30 seconds of entering bleedout and enter a Berserk state. You heal to your current maximum HP, and all your strikes function as Great Strikes for the duration of the Berserk effect. When your Berserk effect ends, you immediately drop to 0 HP and enter Bleedout."
  },

  "Break Limb":{
    "Max":None,
    "Cost":5,
    "desc":"You may call “Break Arm” or “Break Leg” instead of weapon damage."
  },

  "Break Shield":{
    "Max":1,
    "Cost":5,
    "Prereq":{
      "Break Limb":1,
      "Two-Handed Weapons":1
    },
    "desc":"You may expend a use of BREAK LIMB and call “Break Shield” while wielding a TWO-HANDED WEAPON in both hands and striking a shield."
  }
}

MUNDANE_HEALING={
  "Examine Wounds":{
    "Max":1,
    "Cost":2,
    "desc":"You may call “Examine Wounds” within 3 feet of another character. They must tell you if they are living, bleeding out, or dead—and if they are not bleeding out or dead, they should also tell you exactly how damaged they are, in numerical terms. (For instance, “I am missing 4 HP.”)"
  },

  "Detect Poison":{
    "Max":1,
    "Cost":2,
    "Prereq":{"Examine Wounds":1},
    "desc":"You may call “Detect Poison” whenever you are within arm’s reach (roughly 3 feet) of a chosen person. They must tell you if they are suffering from a Poison."
  },

  "Administer Antidote":{
    "Max":None,
    "Cost":2,
    "Prereq":{"Detect Poison":1},
    "desc":"You should role-play the process of treating a person’s Poisoned condition, then call “Remove Poison” to prevent them from dying."
  },

  "Detect Disease":{
    "Max":1,
    "Cost":2,
    "Prereq":{"Examine Wounds":1},
    "desc":"You have the ability to call “detect disease” whenever you are within arm’s reach (roughly 3 feet) of a chosen person. They must tell you if they have any diseases—but they cannot tell you the specific effects of any diseases they may be suffering from."
  },

  "Apply Pressure":{
    "Max":1,
    "Cost":1,
    "Prereq":{"Examine Wounds":1},
    "desc":"With this skill, you have the ability to call “slow bleeding” whenever you are touching a person who is in bleedout. As long as you maintain physical contact with them, you can halt their bleedout count—but you can only use APPLY PRESSURE in this way for up to 3 minutes."
  },

  "Set Bone":{
    "Max":1,
    "Cost":3,
    "Prereq":{"Apply Pressure":1},
    "desc":"You may call “set bone” whenever you are touching a person who has a broken limb. You should role-play the process of wrenching the limb into place, and the subject should role-play an enormous amount of pain."
  },

  "Bandage":{
    "Max":1,
    "Cost":4,
    "Prereq":{"Set Bone":1},
    "desc":"You have the ability to tie a strip of cloth around a person, then call “heal 1” to restore 1 of their Health Points. You can do this as often as you want if you have enough bandages, but you may only use this skill once every 30 seconds, regardless of how many different people you are bandaging."
  },

  "Trauma Patch":{
    "Max":None,
    "Cost":4,
    "Prereq":{"Bandage":1},
    "desc":"you should follow the normal procedure for using a BANDAGE (explained above), but also use role-playing and/or props to suggest that this is an extraordinary effort, then call “Heal 4” to restore the person you are bandaging."
  },

  "Surgery":{
    "Max":1,
    "Cost":5,
    "Prereq":{"Bandage":1,"Lore: Anatomy":1},
    "desc":"To use this skill, you must have props representing a doctor’s implements, such as (for example) a needle and thread, a sharp knife, and a magnifying glass. The amount of time required to perform a given surgery can vary by its complexity (ask a Twin Mask Staff member for details)… but, absent a Staff member’s guidance, it will take 3 minutes of intensive role-playing."
  },

  "Battlefield Medicine":{
    "Max":1,
    "Cost":2,
    "Prereq":{"Surgery":1},
    "desc":"your use of the SURGERY skill to heal others speeds up dramatically, taking only 2 minutes."
  }
}

RELIGIOUS_WORSHIP={
    "Prayer":{
        "Max":1,
        "Cost":4,
        "Prereq":{
            "has_faith":1
        },
        "desc":"Once per game, you may spend 30 minutes participating in a religious rite led by a priest of your faith and then choose one of the available benefits of that rite based on priest rank and number of attendees."
    },
    "Secondary Prayer":{
        "Max":1,
        "Cost":4,
        "Prereq":{
            "Priesthood":2
        },
        "desc":"You may perform PRAYER twice per game instead of once."
    },
    "Tertiary Prayer":{
        "Max":1,
        "Cost":4,
        "Prereq":{
            "Priesthood":4
        },
        "desc":"You may perform PRAYER three times per game."
    },
    "Priesthood":{
        "Max":4,
        "Cost":6,
        "desc":"You may use any known RITE MASTERY skills to perform religious rites for your faith at your level. See the Divine Magic section of Chapter 4."
    },
    "Rite Mastery":{
        "Max":1,
        "Cost":4,
        "Prereq":{"Prayer":1},
        "desc":"Choose one of the 10 non-Universal rites in the Divine Magic section of Chapter 4. You may perform this rite using PRIESTHOOD with 30 minutes of role-play at a Shrine to your faith. You choose a new rite from the 10 available every time you take this skill."
    },
    "Repentance":{
        "Max":1,
        "Cost":2,
        "desc":"If you have +1 Corruption as a result of evil actions performed during gameplay, you receive -1 Corruption. If you ever gain +1 Corruption from performing evil actions while you have this skill, you instead gain +2 Corruption."
    }
}

BARDIC_ARTS={
  "Commanding Presence":{
    "Max":None,
    "Cost":3,
    "desc":"You may call “By My Voice: Stun” after role-playing 3 seconds of trying to get people to quiet down. This may not be used in combat."
  },

  "Serenade":{
    "Max":None,
    "Cost":8,
    "Prereq":{"Willpower":1},
    "desc":"You may perform a 3-minute bardic talent in front of an audience of at least 4 characters, then call “Bestow Willpower” on one of those characters and yourself. You must explain that this Willpower lasts for the entire game and Returns with Rest."
  },

  "Dance Lesson":{
    "Max":None,
    "Cost":8,
    "Prereq":{"Dodge":1},
    "desc":"You must dance to music with another character for 3 minutes, then you may call “Bestow Dodge” on that character and yourself. You must explain that this Dodge lasts for the entire game and Returns with Rest."
  },

  "True Greatness":{
    "Max":None,
    "Cost":4,
    "desc":"You may perform a 3-minute bardic talent in front of at least 3 characters. For 3 hours afterward, you may call “Remove Weakness” on yourself whenever you receive a verbal compliment."
  },

  "Drinking Song":{
    "Max":1,
    "Cost":6,
    "desc":"You may perform a 3-minute bardic talent in front of at least 3 characters. For 3 minutes afterward, the first applicable COOKING skill item you consume will have its numerical values doubled."
  },

  "Meditative Song":{
    "Max":None,
    "Cost":10,
    "Prereq":{"Mana Focus":3},
    "desc":"You may perform a 3-minute bardic talent and call “Restore 3 Mana” on yourself. This may not be used more than once every 30 minutes."
  },

  "Hymn":{
    "Max":1,
    "Cost":2,
    "desc":"You may perform a 3-minute bardic talent in front of at least 3 characters during the first 3 minutes of a PRAYER—dedicated to a god of your faith—and reduce the duration of the PRAYER from 30 minutes to 20 minutes."
  },

  "Requiem":{
    "Max":1,
    "Cost":3,
    "desc":"You may perform a 3-minute bardic talent in front of at least 3 characters during a funeral or wake to allow the spirit of the dead character in question to hear everything said beyond that point in the ceremony."
  }
}

MAGICAL_ARTS={
    "Mana Focus":{
        "Max":None,
        "Cost":1,
        "Prereq":{"Magical Aptitude":1},
        "desc":"You increase your maximum mana by 1."
    },

    "Alchemy":{
        "Max":4,
        "Cost":6,
        'desc':"You can cast Alchemy spells up to the level you choose"
    },

    "Channeling":{
        "Max":4,
        "Cost":6,
        'desc':"You can cast Channeling spells up to the level you choose"
    },

    "Divination":{
        "Max":4,
        "Cost":6,
        'desc':"You can cast Divination spells up to the level you choose"
    },

    "Sorcery":{
        "Max":4,
        "Cost":6,
        'desc':"You can cast Sorcery spells up to the level you choose"
    },

    "Warding":{
        "Max":4,
        "Cost":6,
        'desc':"You can cast Warding spells up to the level you choose"
    },

    "Weapon Casting":{
        "Max":1,
        "Cost":8,
        "Prereq":{"Magical Aptitude":1},
        "desc":"You may deliver a packet spell via a melee or ranged weapon. You must follow all requirements and make the call exactly as you would when delivering it by packet, with the exception that you may add the “Stealth” modifier if you meet all the requirements."
    },

    "Elemental Flourish":{
        "Max":1,
        "Cost":4,
        "Prereq":{"Sorcery":1,"Great Strike":1},
        "desc":"Whenever you perform a GREAT STRIKE, you may add Fire, Ice, Acid, or Lightning to that attack in addition to its normal damage."
    },

    "Armored Casting":{
        "Max":1,
        "Cost":6,
        "Prereq":{"Magical Aptitude":1},
        "desc":"You may ignore restrictions from armor and shields when casting spells."
    },

    "Combat Mimic":{
        "Max":None,
        "Cost":4,
        "Prereq":{"Weapon Casting":1},
        "desc":"You may repeat the call of a non-Greater melee weapon attack targeted at you within the last 3 seconds."
    },

    "Internal Reserves":{
        "Max":1,
        "Cost":4,
        "Prereq":{"Mana Focus":10},
        "desc":"You may meditate for 30 seconds, then call “Restore 10 mana.” You reduce your maximum HP by 1 for the remainder of the weekend."
    },

    "Arcane Tutelage":{
        "Max":1,
        "Cost":10,
        "Prereq":{"gm_mage":1,"Research":1},
        "desc":"You may perform a 30-minute presentation on magic, then call “Bestow 10 mana.” You must explain to everyone present that this mana works like maximum mana and returns with sunrise/sunset, just like mana on their character sheet."
    },

    "Arcane Observation":{
        "Max":1,
        "Cost":4,
        "Prereq":{"Arcane Tutelage":1},
        "desc":"You receive the benefit of your own Arcane Tutelage."
    },

    "Spellwright":{
        "Max":1,
        "Cost":2,
        "Prereq":{"gm_mage":1,"Research":1},
        "desc":"You may pitch and invent new spells using the rules for Researching New Spells"
    }
}

SKULLDUGGERY={
"Disguise": {
"Max": 1,
"Cost": 4,
"desc":"You may don a disguise and attempt to appear unrecognizable as your character without changing your race. If asked OOC by other characters if you are your PC, you may answer “yes” or “no” at your option. You may answer this way both IC and OOC."
},

"Master Disguise": {
"Max": 1,
"Cost": 6,
"Prereq": {
"Disguise": 1
},
"desc":"You may don a disguise and attempt to appear unrecognizable as your character with the ability to change your race. If asked OOC by other characters if you are your PC, you may answer “yes” or “no” at your option. You may answer this way both IC and OOC."
},

"Detect Disguise": {
"Max": 1,
"Cost": 4,
"desc":"You must spend 3 uninterrupted minutes within arm’s reach of a character, then may call “Detect Disguise.” They must answer truthfully whether they are in disguise. Special—the EFFENDAL SENSES skill reduces the time to 2 uninterrupted minutes."
},

"Escape": {
"Max": None,
"Cost": 3,
"desc":"You may call “Escape” and remove yourself from any effect that physically restricts your movement, like ROPE USE, Bind, shackles, or SUPERNATURAL STRENGTH."
},

"Poison Resistance": {
"Max": None,
"Cost": 2,
"desc":"You may call “Resist” and prevent or end all Poison effects currently affecting you, regardless of time remaining."
},

"Poison Immunity": {
"Max": 1,
"Cost": 4,
"Prereq": {
"Poison Resistance": 3
},
"desc":"You may call “No Effect” to prevent any Poison effects from affecting you."
},

"Lockpicking": {
"Max": 1,
"Cost": 4,
"desc":"You may spend 3 minutes role-playing picking a lock with a tagged lockpick prop to open an Apprentice-level lock."
},

"Gambling": {
"Max": None,
"Cost": 2,
"desc":"You may call “Gambling” and re-draw one hand of cards or re-roll one set of dice. You must take the new result no matter the outcome."
},

"Torture": {
"Max": None,
"Cost": 2,
"desc":"You spend 3 minutes role-playing torturing a character, then may call “Torture” and ask one yes-or-no question. The target must answer truthfully unless they resist."
}
}

KNOWLEDGE={
    "Research":{
        "Max":1,
        "Cost":6,
        "Prereq":{"Literate":0},
        "desc":"Once per game, you may spend 30 minutes role-playing researching a specific topic with at least 2 research assistants. You then bring your character sheet (with the signatures of your research assistants on the back) and your Library building tag or tagged Research Object to Logistics. You then fill out either an Open-Ended Research Form for your topic, or have a Staff member on duty sign off on an active research tag."
    },

    "Alchemical Examination":{
        "Max":1,
        "Cost":3,
        "Prereq":{"Lore: Alchemy":1},
        "desc":"You may spend 30 seconds role-playing studying an object, then ask a nearby Twin Mask Story Staff member what you learned about the object in question using ALCHEMICAL EXAMINATION."
    }
}

GATHERING={
    "Academic Standing":{
        "Max":4,
        "Cost":4,
        'desc':'At check-in, you receive an amount of Academic Standing cards equal to the rank you choose'
    },
    "Economic Standing":{
        "Max":4,
        "Cost":4,
        'desc':'At check-in, you receive an amount of Economic Standing cards equal to the rank you choose'
    },
    "Military Standing":{
        "Max":4,
        "Cost":4,
        'desc':'At check-in, you receive an amount of Military Standing cards equal to the rank you choose'
    },
    "Political Standing":{
        "Max":4,
        "Cost":4,
        'desc':'At check-in, you receive an amount of Political Standing cards equal to the rank you choose'
    },
    "Underworld Standing":{
        "Max":4,
        "Cost":4,
        'desc':'At check-in, you receive an amount of Underworld Standing cards equal to the rank you choose'
    },
    "Mining":{
        "Max":4,
        "Cost":4,
        'desc':'At check-in, you get an amount of points in the MINING tree equal to the rank you choose'
    },
    "Herbalism":{
        "Max":4,
        "Cost":4,
        'desc':'At check-in, you get an amount of points in the HERBALISM tree equal to the rank you choose'
    },
    "Woodcutting":{
        "Max":4,
        "Cost":4,
        'desc':'At check-in, you get an amount of points in the WOODCUTTING tree equal to the rank you choose'
    },
    "Hunting":{
        "Max":4,
        "Cost":4,
        'desc':'At check-in, you get an amount of points in the HUNTING tree equal to the rank you choose'
    },
    "Mercantile":{
        "Max":4,
        "Cost":4,
        'desc':'At check-in, you get an amount of points in the MERCANTILE tree equal to the rank you choose'
    },
    "Black Market":{
        "Max":4,
        "Cost":4,
        'desc':'At check-in, you get an amount of points in the BLACK MARKET tree equal to the rank you choose'
    }
}

CRAFTING_SKILLS={
"Fortify Armor":{
"Max":1,
"Cost":3,
"Prereq":{"can_fortify":1},
"desc":"You may spend 3 minutes at a Worktable (Light) or a Forge (Heavy) role-playing reinforcing a set of armor, then call “Bestow 2 Armor” (Light) or “Bestow 4 Armor” (Heavy). You should explain that this bestowed armor lasts the entire weekend and is restored with rest or FIELD REPAIR."
},

"Field Repair":{
"Max":None,
"Cost":2,
"Prereq":{"can_field_repair":1},
"desc":"You may spend 30 seconds role-playing repairing a set of armor or a shield that you have the relevant crafting skill for, then call “Restore Armor” or “Restore Shield.”"
},

"Repair Shield":{
"Max":1,
"Cost":3,
"Prereq":{"Shieldsmithing":1},
"desc":"You may spend 3 minutes at a Forge roleplaying the process of repairing a shield, then call Restore Shield."
},

"Recipe Scribing":{
"Max":1,
"Cost":2,
"Prereq":{"Scroll Scribing":1},
"desc":"You may use SCROLL SCRIBING to copy craft recipes (but not rituals). The cost is 1 Feather + 1 Paper per level of the recipe. You must bring the recipe, Laboratory tag, and ingredients to Logistics, just as you do with a scroll."
},

"New Edition":{
"Max":1,
"Cost":3,
"Prereq":{"Scroll Scribing":1},
"desc":"You may use SCROLL SCRIBING to make a replacement copy of a damaged, non-stolen scroll for a single blood ink, regardless of level. You must bring (and surrender) the damaged scroll to Logistics along with the Laboratory tag and ingredients, just like making a new scroll."
},

"Grand Feast":{
"Max":1,
"Cost":10,
"Prereq":{"Cooking":4},
"desc":"You spend 30+ minutes role-playing hosting a feast for any number of people. You and up to 2 other cooks you choose may cook any number of dishes from the COOKING tree as part of the feast. You should explain that any food cooked AND consumed during the event by a participant that is there for the full 30 minutes gains the benefit of DRINKING SONG. See the COOKING skill for which dishes DRINKING SONG applies to."
},

"Reconstruct":{
"Max":1,
"Cost":1,
"Prereq":{"is_crafter":1},
"desc":"You may remake a crafting item with the exact same, rulebook-legal properties listed on the original tag with one fewer listed ingredient of your choice per rank of the original item."
},

"Inventor":{
"Max":1,
"Cost":2,
"Prereq":{"can_invent":1,"Research":1},
"desc":"You may pitch and invent new craft recipes using the rules for Researching New Craft Items"
}
}

LORE={}

APPROVED_LORES=["Alchemy","Celestials","The Blood Cauldon","War of Wine","Rules of Society","Blood Magic","Demons","The Celestine Faith","Purges","Nature","Channeling","Fae","Church of Chorus","The First Crusade","Anatomy","Divination","Dragons","Demon Faiths","The War of Radiance","Medicine","Dream Magic","Undead","Dragon Worship","The Second Crusade","Knighthood","Necromancy","The Lady of the Mists","The War of Giants","Sorcery","the Nameless Faith","Summoning","Old Ways","Warding","Trahazi Zodiac","Ritual Magic"]
for starting_lore in APPROVED_LORES:
    LORE[f'Lore: {starting_lore}']={'Max':1,'Cost':4,'desc':f'You may call “Bid Lore: {starting_lore}” and ask a question of a nearby Twin Mask Story Staff member. This question may be as simple as, “Do I know anything about this?” or as specific as you like.'}

CRAFTING_CIRCLES = {
    "Blacksmithing": {"Max": 4, "Cost": 6, "desc":"You may spend 30 minutes at a Forge role-playing crafting an item from the Blacksmithing chart or a craft recipe with a total Skill Level of your chosen level, then take your building tag and ingredients to Logistics."},
    "Weaponsmithing": {"Max": 4, "Cost": 6, "desc":"You may spend 30 minutes at a Forge role-playing crafting an item from the Weaponsmithing chart or a craft recipe with a total Skill Level of your chosen level, then take your building tag and ingredients to Logistics."},
    "Armorsmithing": {"Max": 4, "Cost": 6, "desc":"You may spend 30 minutes at a Forge role-playing crafting an item from the Armorsmithing chart or a craft recipe with a total Skill Level of your chosen level, then take your building tag and ingredients to Logistics."},
    "Shieldsmithing": {"Max": 4, "Cost": 6, "desc":"You may spend 30 minutes at a Forge role-playing crafting an item from the Shieldsmithing chart or a craft recipe with a total Skill Level of your chosen level, then take your building tag and ingredients to Logistics."},
    "Locksmithing": {"Max": 4, "Cost": 6, "desc":"You may spend 30 minutes at a Work Table role-playing crafting an item from the Locksmithing chart or a craft recipe with a total Skill Level of your chosen level, then take your building tag and ingredients to Logistics."},
    "Enchanting": {"Max": 4, "Cost": 6, "desc":"You may spend 30 minutes at a Work Table role-playing crafting an item from the Enchanting chart or a craft recipe with a total Skill Level of your chosen level, then take your building tag and ingredients to Logistics."},
    "Scroll Scribing": {"Max": 4, "Cost": 6, "desc":"You may spend 30 minutes at a Laboratory role-playing copying any spell scroll or Scribing craft recipe up to the level you choose, then take your building tag and ingredients to Logistics."},
    "Artificing": {"Max": 4, "Cost": 6, "desc":"You may spend 30 minutes at a Laboratory role-playing crafting an item from the Artificing chart or a craft recipe with a total Skill Level of your chosen level, then take your building tag and ingredients to Logistics."},
    "Cooking": {"Max": 4, "Cost": 6, "desc":"You may spend 3 minutes at a Kitchen role-playing to cook a dish from the Cooking chart or a craft recipe with a total Skill Level up to your chosen level."},
    "Stable Alchemy": {"Max": 4, "Cost": 6, "desc":"You may spend 30 minutes at a Laboratory role-playing crafting a potion from an Alchemy scroll up to the level you choose you are attuned to (or an attuned craft recipe), then take your building tag and ingredients to Logistics."},
    "Tailoring": {"Max": 4, "Cost": 6, "desc":"You may spend 30 minutes at a Worktable role-playing crafting an item from the Tailoring chart or a craft recipe with a total Skill Level of your chosen level, then take your building tag and ingredients to Logistics."},
    "Fletching": {"Max": 4, "Cost": 6, "desc":"You may spend 30 minutes at a Worktable role-playing crafting an item from the Fletching chart or a craft recipe with a total Skill Level of your chosen level, then take your building tag and ingredients to Logistics."},
    "Engineering": {"Max": 4, "Cost": 6, "desc":"You may spend 30 minutes at a location role-playing crafting an item from the Engineering chart or a craft recipe with a total Skill Level of your chosen level, then take your ingredients to Logistics."}
}

