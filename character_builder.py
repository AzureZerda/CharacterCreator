from flask import session, request
import constants
import skills_db
from skills_db import SKILL_REF
import twin_maskify as tm
from Skills import Construct_Skill
from session_manager import Update_Points
 
 
class Player_Details_Input:
    def __init__(self, input):
        self.name = input['player_name']
        self.email = input['email']
        self.emergency = input['emergency_contact']
        if input['discord'] == '':
            self.discord = 'None'
        else:
            self.discord = input['discord']
 
 
class Character_Details_Input:
    def __init__(self, input):
        self.name = input['name']
        self.culture = input['culture']
        self.bloodline = input['bloodline']
        self.faith = input['faith']
        self.incentive_points = input['incentive_points']
 
 
def insert_char_details(player):
    session['person_details'] = {}
    per_ref = session['person_details']
    per_ref['name'] = player.name
    per_ref['discord'] = player.discord
    per_ref['email'] = player.email
    per_ref['emergency_contact'] = player.emergency
 
 
def create_char(data):
    data = request.get_json()
 
    player = Player_Details_Input(data)
 
    character_ = Character_Details_Input(data)
 
    for cat in session:
        try:
            session[cat] = constants.DEFAULT_SESSION[cat].copy()
        except KeyError:
            continue
 
    if character_.bloodline.lower() == 'newborn dream':
        skills_db.BACKGROUND_FLAWS['Tethered'] = {'Max': 1, 'Cost': -10}
        SKILL_REF['Tethered'] = {'Max': 1, 'Cost': -10}
        session['character_details']['flaws_added'].append('Tethered')
        session.modified = True
        session['skills_added']['Tethered'] = 1
 
    else:
        session['character_details']['flaws_added'] = []
        if 'Tethered' in SKILL_REF:
            del SKILL_REF['Tethered']
 
    insert_char_details(player)
 
    char_ref = session['character_details']
    char_ref['name'] = character_.name
    char_ref['culture'] = character_.culture
    char_ref['bloodline'] = character_.bloodline
    char_ref['faith'] = character_.faith
 
    input = {'skill': f'Native Lore: {data["culture"]}',
             'quantity': 1, 'modifer': 1}
    input = tm.SkillChangeInput(input)
 
    character = tm.Character.from_session(session)
 
    skill = Construct_Skill(input, character)
    tm.add_skill(skill)
 
    if 'second_culture' in data:
        char_ref['second_culture'] = data['second_culture']
        input = {'skill': f'Native Lore: {data["second_culture"]}',
                 'quantity': 1, 'modifer': 1}
        input = tm.SkillChangeInput(input)
        skill = Construct_Skill(input, character)
        tm.add_skill(skill)
    if 'incentive_points' in data:
        char_ref['incentive_points'] = data['incentive_points']
    else:
        char_ref['incentive_points'] = 0
 
    session['character_details']['points'] = Update_Points()