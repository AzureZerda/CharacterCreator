import re
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
    cost_ref={}
    CP_Spent = 0

    # at some point the base native lore started showing up in here. Fix it azzy
    
    character = tm.Character.from_session(session)
 
    if session['character_type'] != 'character_plan':
        if session['character_details']['bloodline'].lower() not in constants.FORTY_POINTS:
            base_total = 20
        else:
            base_total = 40
    
        if 'points_earned' in session:
            base_total += session['points_earned']
    
        base_total += int(character.details['incentive_points'])
    else:
        if 'char_points' not in session['character_details']:
            session['character_details']['base_points'] = int(session['character_details']['points'])
        base_total = int(session['character_details']['base_points'])
        session['character_details']['char_points'] = int(session['character_details']['points'])
 
    skills_list = dict(session['skills_added'])
 
    native_skips = 0
 
    if session['character_details']['bloodline'].lower() != 'newborn dream' and 'Tethered' in session['character_details']['flaws_added']:
        session['character_details']['flaws_added'].remove('Tethered')

    if 'Pursuit of Knowledge' in skills_list:
        lore_elims = 3
    else:
        lore_elims = 0
 
    if 'Weapon Master' in skills_list:
        for skill in constants.WEAPON_MASTER_SKILLS:
            del skills_list[skill]
    
    for skill, quantity in skills_list.items():
        audit_printout = ''
        audit_printout += f'Before processing {skill}, the total CP is {base_total}. '
        if 'Legacy' in skill:
            discount = quantity
        else:
            match = re.search(r"L\d+", skill)
            if match:
                discount = skill[-2]
            else:
                discount = 0
 
        try:
            skill_cost = SKILL_REF[skill.split(' (',1)[0]]['Cost']
        except KeyError:
            if skill[:2] == 'R.' or skill[:4] == 'Lore':
                if lore_elims > 0:
                    skill_cost = 0
                    lore_elims -= 1
                else:
                    skill_cost = 4
            elif skill[:6] == 'Native':
                if native_skips==0:
                    skill_cost=0
                    native_skips += 1
                else:
                    skill_cost = 4
                    quantity= 1
            else:
                continue

        audit_printout += f'the cost of {skill} is {(skill_cost * int(quantity))-int(discount)}. '
        
        base_total -= (skill_cost * int(quantity))-int(discount)

        CP_Spent += (skill_cost * int(quantity))-int(discount)

        cost_ref[skill] = (skill_cost * int(quantity))-int(discount)

        audit_printout += f'After accounting for cost of {skill}, there are now {base_total} points\n'


    session['character_details']['points'] = base_total
    session['cost_ref'] = cost_ref

    return base_total