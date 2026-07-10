from flask import session
import constants
import twin_maskify as tm
from skills_db import SKILL_REF
from bloodline_skills import BLOODLINE_SKILLS
 
 
def reset_skills():
    for cat in constants.DEFAULT_SESSION:
        if cat == 'character_details':
            continue
        session[cat] = constants.DEFAULT_SESSION[cat].copy()
 
    session['character_details']['flaws_added'] = []
 
    session.modified = True
 
 
def reset_session():
    for cat in constants.DEFAULT_SESSION:
        if cat == 'character_details':
            continue
        session[cat] = constants.DEFAULT_SESSION[cat].copy()
 
    session.modified = True
 
 
def reset_skill_selections():
    session['character_details']['health_points'] = 5
    char_ref = session['character_details']
    char_ref['flaws_added'] = []
    session['skills_added'] = {'Literate': 0, 'Weapon_Master': 0,
                                'can_assassinate': 0, 'can_field_repair': 0, 'can_fortify': 0,
                                'can_instruct': 0, 'can_invent': 0, 'gm_mage': 0, 'has_faith': 0,
                                'is_crafter': 0, 'memory_flaws': 0}
    session.modified = True
 
 
def back_to_the_death_realms_with_you():
    for cat in session:
        try:
            session[cat] = constants.DEFAULT_SESSION[cat].copy()
        except KeyError:
            continue
    session.modified = True
 
 
def inject_bloodline_skills(session, dictionary):
    bloodline = session["character_details"]["bloodline"]
 
    dictionary[f'{bloodline.upper()} ONLY SKILLS'] = BLOODLINE_SKILLS.get(bloodline, {})
 
    return dictionary
 
 
def Update_Points():
    # at some point the base native lore started showing up in here. Fix it azzy
    character = tm.Character.from_session(session)
 
    if session['character_details']['bloodline'].lower() not in constants.FORTY_POINTS:
        base_total = 20
    else:
        base_total = 40
 
    if 'points_earned' in session:
        base_total += session['points_earned']
 
    base_total += int(character.details['incentive_points'])
 
    flaw_points = 0
 
    skills_list = dict(session['skills_added'])
 
    native_skips = 0
 
    for skill in skills_list.copy():
        if skill[:6] == 'Native' and native_skips == 0:
            del skills_list[skill]
            native_skips += 1
 
    if session['character_details']['bloodline'].lower() != 'newborn dream' and 'Tethered' in session['character_details']['flaws_added']:
        session['character_details']['flaws_added'].remove('Tethered')
 
    for flaw in session['character_details']['flaws_added']:
        new_flaw_points = flaw_points + -SKILL_REF[flaw]['Cost']
 
        if new_flaw_points >= 10:
            flaw_points = 10
            break
        elif new_flaw_points < 10:
            flaw_points = new_flaw_points
 
    base_total += flaw_points
 
    if 'Pursuit of Knowledge' in skills_list:
        lore_score = session['flags']['lore_score']
 
        if lore_score >= 12:
            base_total += 12
        elif lore_score == 0:
            pass
        else:
            base_total += lore_score
 
    dict_ref = session['Point_Cats']
    lore_score = dict_ref['lore_score']
 
    if 'Weapon Master' in skills_list:
        for skill in constants.WEAPON_MASTER_SKILLS:
            del skills_list[skill]
 
    for skill, quantity in skills_list.items():
 
        if skill in constants.FLAWS:
            continue
        if skill[:7] == 'Native':
            continue
        try:
            skill_cost = SKILL_REF[skill]['Cost']
        except KeyError:
            if skill[:6] == 'Native':
                skill_cost = 4
            else:
                continue
 
        base_total -= skill_cost * quantity
 
    if 'Pursuit of Knowledge' in skills_list:
        if lore_score >= 12:
            base_total += 12
        else:
            base_total += lore_score
 
    session['character_details']['points'] = base_total
 
    return base_total