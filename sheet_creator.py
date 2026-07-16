import re
import gspread
from openpyxl.utils import column_index_from_string
import constants
from bloodline_skills import BLOODLINE_SKILLS
import datetime
import json
import twin_maskify as tm

#azzy made a mess in here. fix it idiot

class Outside_Respec_Range(Exception):
    pass

class Layout_Manager:
    def __init__(self):
        self.lengths={
            'X':-5,
            'Y':0,
            'Z':0
        }
        self.sectors={
            'Bloodline':'X',
            'Background':'X',
            'General Skills':'Y',
            'Knowledge':'Y',
            'Magical Arts':'Z',
            'Gathering/Crafting':'Z'
        }

        self.sector_boxes={
            'X':['Bloodline','Background'],
            'Y':['General Skills','Knowledge'],
            'Z':['Magical Arts','Gathering/Crafting']
        }

        self.columns={
            'General Skills':'A',
            'Bloodline':'A',
            'Magical Arts':'A',
            'Background':'E',
            'Knowledge':'E',
            'Gathering/Crafting':'E'
        }
        self.below={
            'Bloodline':'General Skills',
            'General Skills':'Magical Arts',
            'Background':'Knowledge',
            'Knowledge':'Gathering/Crafting'
        }

        self.starting_line={
            'X':9,
            'Y':16,
            'Z':23
        }
    
        self.default_locs={
            'Player:':{'col':'A','row':2},
            'Email:':{'col':'A','row':3},
            'Culture:':{'col':'A','row':4},
            'Religion:':{'col':'A','row':5},
            'Character:':{'col':'E','row':2},
            'Bloodline:':{'col':'E','row':3}
        }

        self.merge_ranges=['B2:D2','B3:D3','B4:D4','B5:D5','F2:H2','F3:H3','E6:F6','A1:H1']

class Character_Sheet:
    def __init__(self,url):
        self.workbook = gc.open_by_url(url)

        pages=['Character','Progression','History','Emergency']

        try:
            self.character = self.workbook.worksheet("Character")
        
        except gspread.WorksheetNotFound:
            self.character = self.workbook.add_worksheet(title="Character", rows=100, cols=20)

        try:
            self.progression = self.workbook.worksheet("Progression")
        
        except gspread.WorksheetNotFound:
            self.progression = self.workbook.add_worksheet(title="Progression", rows=100, cols=20)

        try:
            self.history = self.workbook.worksheet("History")
        
        except gspread.WorksheetNotFound:
            self.history = self.workbook.add_worksheet(title="History", rows=100, cols=20)

        try:
            self.emergency = self.workbook.worksheet("Emergency")
        
        except gspread.WorksheetNotFound:
            self.emergency = self.workbook.add_worksheet(title="Emergency", rows=100, cols=20)

        worksheet_list = self.workbook.worksheets()

        for worksheet in worksheet_list:
            if worksheet.title not in pages:
                self.workbook.del_worksheet(worksheet)

class cell_input:
    def __init__(self,value,col,row):
        self.value=value
        self.coordinate=f'{col}{row}'

class Sheet_Constructor:
    def __init__(self,session):
        self.session=session
        self.boxes={}
        for box in constants.SHEET_BOXES:
            self.boxes[box]={}
        self.layout=Layout_Manager()
        self.cells=[]
        self.progression_cells=[]
        self.formula_cells=[]

        self.formats={
        'skill_box_header':{
            'format':{
                "backgroundColor": {
                    "red": 0.588,
                    "green": 0.588,
                    "blue": 0.588
                    },
                    "horizontalAlignment": "CENTER",
                    "textFormat": {
                        "bold": True
                    }
                },
            'cells':[]
            }
        }
    
    def construct(self,character):
        self.bloodline=character['character_details']['bloodline']
        self.insert_bloodline_stuff()
        self.insert_char_details(character['character_details'])
        self.insert_player_details(character['person_details'])
        self.construct_skill_boxes(character['skills_added'])
        self.construct_progression()
        self.cells.append(gspread.Cell(1,1,'Twin Mask'))
        self.insert_formulas()
        for sector in self.layout.sector_boxes:
            sector_length=0
            sector_start=self.layout.starting_line[sector]
            for box in self.layout.sector_boxes[sector]:
                finish_line=0
                skill_column=self.layout.columns[box]
                cost_column=next_letter(skill_column)
                starting_line=self.layout.starting_line[self.layout.sectors[box]]
                cell=generate_cell(box,skill_column,starting_line)
                self.cells.append(cell)
                try:
                    next_box=self.layout.below[box]
                    next_sector=self.layout.sectors[next_box]
                    next_start=self.layout.starting_line[next_sector]
                except KeyError:
                    pass
                box_length=starting_line
                for index, skill in enumerate(self.boxes[box], start=sector_start+1):
                    skill_box=generate_cell(skill,skill_column,index)
                    cost_box=generate_cell(self.boxes[box][skill],cost_column,index)
                    self.cells.extend([skill_box,cost_box])
                    box_length+=1
                    finish_line=index

                if box_length>sector_length:
                    sector_length=box_length

            if sector_length+2 >= next_start:
                if sector=='Y' or sector=='X':
                    self.layout.starting_line[next_sector]=sector_length+2
    
    def insert_bloodline_stuff(self):
        bloodline=self.session['character_details']['bloodline']
        for i,skill in enumerate(BLOODLINE_SKILLS[bloodline],start=10):
            if skill not in self.session['skills_added']:
                if BLOODLINE_SKILLS[bloodline][skill]['Max'] != 1:
                    skill_input=f'{skill} x0'
                else:
                    skill_input=skill
                cost='N/A'
            else:
                quantity=self.session['skills_added'][skill]
                skill_input=f'{skill} x{quantity}'
                cost=quantity*SKILL_REF[skill]['Cost']

            skill_cell=gspread.Cell(i,1,skill_input)
            cost_cell=gspread.Cell(i,2,cost)
            self.cells.extend([skill_cell,cost_cell])

    def construct_progression(self):
        col='A'
        for cell in constants.PROGRESSION_HEADERS:
            cell_data_1=generate_cell(cell,col,1)
            cell_data_2=generate_cell(constants.PROGRESSION_HEADERS[cell],col,2)
            col=next_letter(col)
            if cell=='CP Earned' and self.bloodline.lower() not in ['human','effendal']:
                cell_data_2.value='20'
            self.progression_cells.extend([cell_data_2,cell_data_1])

    def insert_formulas(self):
        for formula in constants.SHEET_FORMULAS:
            cell1=cell_input(formula,constants.SHEET_FORMULAS[formula]['col'],constants.SHEET_FORMULAS[formula]['row'])
            cell2=cell_input(constants.SHEET_FORMULAS[formula]['formula'],next_letter(constants.SHEET_FORMULAS[formula]['col']),int(constants.SHEET_FORMULAS[formula]['row']))
            self.formula_cells.extend([cell1,cell2])
    
    def insert_player_details(self,player):
        not_on_sheet=['discord','emergency_contact']

        new_dict={}

        for label in player:
            if label not in not_on_sheet:
                new_dict[constants.SHEET_RENAME_MAP[label]]=player[label]

        for detail in new_dict:
            column1=self.layout.default_locs[detail]['col']
            column2=next_letter(column1)
            cell1=generate_cell(detail,column1,int(self.layout.default_locs[detail]['row']))
            cell2=generate_cell(new_dict[detail],column2,int(self.layout.default_locs[detail]['row']))
            self.cells.extend([cell1,cell2])
    
    def insert_char_details(self,character):
        not_on_sheet=['backstory','flaws_added','memory_flaws','points','flaw_points','health points','points']

        new_dict={}

        for label in character:
            if label not in not_on_sheet:
                try:
                    new_dict[constants.SHEET_RENAME_MAP[label]]=character[label]
                except KeyError:
                    continue

        if 'Player:' in new_dict:
            new_dict['Character:']=new_dict['Player:']
            del new_dict['Player:']

        for detail in new_dict:
            column1=self.layout.default_locs[detail]['col']
            column2=next_letter(column1)
            cell1=generate_cell(detail,column1,int(self.layout.default_locs[detail]['row']))
            cell2=generate_cell(new_dict[detail],column2,int(self.layout.default_locs[detail]['row']))
            self.cells.extend([cell1,cell2])
    
    def construct_skill_boxes(self,skills):
        skills[f'Native Lore: {self.session['character_details']['culture']}']=0
        for skill in constants.DEFAULT_SKILLS:
            if skill in skills:
                quantity=skills[skill]
                del skills[skill]
            else:
                if skill=='Mana Focus' or skill=='Toughness':
                    quantity='0'
                else:
                    quantity='N/A'
        
            entry1=self.add_quantity(skill,quantity)
            entry2=self.calculate_spend(skill,quantity)

            self.boxes[SKILL_REF[skill]['sheet_box']][entry1]=entry2
            
        for skill in skills:
            if skill in BLOODLINE_SKILLS[self.session['character_details']['bloodline']]:
                continue
            if skill in constants.FLAGS:
                continue
            entry1=self.add_quantity(skill,skills[skill])
            entry2=self.calculate_spend(skill,skills[skill])

            try:
                self.boxes[SKILL_REF[skill]['sheet_box']][entry1]=entry2
            except KeyError:
                self.boxes['Knowledge'][skill]=entry2

    def add_quantity(self,skill,quantity):
        try:
            if quantity=='N/A':
                skill_entry=skill
            
            elif SKILL_REF[skill]['Max'] != 1:
                skill_entry=f'{skill} x{quantity}'

            else:
                skill_entry=skill
        except KeyError:
            if skill[:6]=='Native':
                skill_entry=skill
            else:
                raise KeyError
        
        return skill_entry
    
    def calculate_spend(self,skill,quantity):
        if quantity=='N/A':
            return 'N/A'
        if quantity=='0':

            return 0
        try:
            skill_cost=SKILL_REF[skill]['Cost']
        except KeyError:
            skill_cost=4
        spend_cost=skill_cost*quantity
        return spend_cost

class Existing_Sheet:
    def __init__(self,skills,char_details,url,per_details):
        self.skills=skills
        self.char_details=char_details
        self.url = url
        self.per_details = per_details

class Templates:
    def __init__(self):
        template_sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1S4jGc7nqan4eHvhuWuqbDKQJlKUd2FEe-g2JgSHsFlg/edit?gid=38564953#gid=38564953')

        self.character = template_sh.worksheet("Character")

def check_respec(session):
    old_session = session['old_session'].copy()
    new_session = session.copy()
    del new_session['old_session']

    if new_session['skills_added'] == old_session['skills_added']:
        skills_changed = False
    else:
        skills_changed = True
    
    if new_session['character_details']['backstory'] == old_session['character_details']['backstory']:
        backstory_changed = False
    else:
        backstory_changed = True
    
    return skills_changed,backstory_changed

def export_respec(session):
    url = session.get('sheet_url')

    skill_status, backstory_status = check_respec(session)

    tracking_row = [session['character_details']['name'],skill_status, backstory_status,
           session['character_details']['culture'],session['character_details']['bloodline'],
           session['character_details']['backstory'],json.dumps(session['skills_added'])]
    
    gsheet = Character_Sheet(url)

    sheet=Sheet_Constructor(session)

    sheet.construct(session)
    
    if skill_status is True:
        try:
            pres_check = gsheet.workbook.worksheet('Pending_Character')
            gsheet.workbook.del_worksheet(pres_check)
        except:
            pass

        templates.character.copy_to(gsheet.workbook.id)

        result = gsheet.workbook.worksheet("Copy of Character")

        result.update_title("Pending_Character")

        gsheet.pending_character = gsheet.workbook.worksheet('Pending_Character')

        gsheet.pending_character.update_cells(sheet.cells)

        for cell in sheet.formula_cells:
            gsheet.pending_character.update_acell(cell.coordinate,cell.value)

        for range in sheet.layout.merge_ranges:
            gsheet.pending_character.merge_cells(range)

        for line in sheet.layout.starting_line:
            sheet.formats['skill_box_header']['cells'].extend([f'A{sheet.layout.starting_line[line]}',f'E{sheet.layout.starting_line[line]}'])
        
        for format in sheet.formats:
            for cell in sheet.formats[format]['cells']:
                gsheet.pending_character.format(cell,sheet.formats[format]['format'])
    
    if backstory_status is True:

        try:
            pres_check = gsheet.workbook.worksheet('Pending_History')
            gsheet.workbook.del_worksheet(pres_check)
        except:
            pass
        
        gsheet.workbook.add_worksheet(title="Pending_History", rows=100, cols=20)

        gsheet.pending_history = gsheet.workbook.worksheet('Pending_History')

        gsheet.pending_history.update_cell(1,1,session['character_details']['backstory'])

def sheet_setup(sheet):
    templates.character.copy_to(sheet.id)

    try:
        worksheet = sheet.worksheet("Character")
        sheet.del_worksheet(worksheet)
    except:
        pass

        result = sheet.worksheet("Copy of Character")

        result.update_title("Character")

def export_char(session):

    url = session.get('sheet_url')

    if url is None:
        sh = gc.create(f'{session['person_details']['name']} ({session['character_details']['name']})')
        sheet_setup(sh)
    else:
        sh = gc.open_by_url(url)

    gsheet = Character_Sheet(sh.url)
    
    sheet=Sheet_Constructor(session)

    sheet.construct(session)

    gsheet.progression.update_cells(sheet.progression_cells) 

    gsheet.character.update_cells(sheet.cells)

    try:
        gsheet.history.update_acell('A1',session['character_details']['backstory'])
    except KeyError:
        session['character_details']['backstory']='He was forced to eat cement when he was 6'
        gsheet.history.update_acell('A1',session['character_details']['backstory'])


    gsheet.emergency.update_acell('A2',session['person_details']['emergency_contact'])

    for cell in sheet.formula_cells:
        gsheet.character.update_acell(cell.coordinate,cell.value)

    for range in sheet.layout.merge_ranges:
        gsheet.character.merge_cells(range)

    for line in sheet.layout.starting_line:
        sheet.formats['skill_box_header']['cells'].extend([f'A{sheet.layout.starting_line[line]}',f'E{sheet.layout.starting_line[line]}'])
    
    for format in sheet.formats:
        for cell in sheet.formats[format]['cells']:
            gsheet.character.format(cell,sheet.formats[format]['format'])

    NPL_sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1ArvwEyaAzGb3XvPSShNeEL_eHHrw2TfV9q4kbrY8Bwg/edit?gid=1599082411#gid=1599082411')
    NPL_records = NPL_sh.worksheet("Demo")

    rows = NPL_records.get_all_values()
    num_rows = len(rows)

    NPL_Rows=construct_NPL_Row(session,sh,num_rows+1)

    try:
        worksheet = NPL_sh.worksheet("Demo")
    
    except gspread.WorksheetNotFound:
        worksheet = NPL_sh.add_worksheet(title="Demo", rows=100, cols=20)
    
    worksheet.update_cells(NPL_Rows)

def construct_NPL_Row(session,sheet,row):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if 'second_culture' in session['character_details']:
        culture=f'{session['character_details']['culture']}/{session['character_details']['second_culture']}'
    else:
        culture=session['character_details']['culture']
    timestamp_cell=gspread.Cell(row,1,timestamp)
    type_cell=gspread.Cell(row,2,'Test Character')
    player_name_cell=gspread.Cell(row,3,session['person_details']['name'])
    gmail_account_cell=gspread.Cell(row,4,session['person_details']['email'])
    character_name_cell=gspread.Cell(row,5,session['character_details']['name'])
    bloodline_name_cell=gspread.Cell(row,6,session['character_details']['bloodline'])
    culture_cell=gspread.Cell(row,7,culture)
    sheet_cell=gspread.Cell(row,8,sheet.url)
    religion_cell=gspread.Cell(row,9,session['character_details']['faith'])
    backstory_cell=gspread.Cell(row,10,session['character_details']['backstory'])
    emergency_cell=gspread.Cell(row,11,'Jenny: 8675309')
    approved_cell=gspread.Cell(row,12,'No')
    sheet_shared_cell=gspread.Cell(row,13,'No')
    discord_cell=gspread.Cell(row,14,session['person_details']['name'])

    if 'second_culture' in session['character_details']:
        dual_culture='True'
    else:
        dual_culture='False'
    dual_flag_cell=gspread.Cell(row,15,dual_culture)

    rows=[timestamp_cell,type_cell,player_name_cell,gmail_account_cell,character_name_cell,
                    bloodline_name_cell,culture_cell,sheet_cell,religion_cell,
                    backstory_cell,emergency_cell,approved_cell,sheet_shared_cell,
                    discord_cell,dual_flag_cell]
    return rows

def check_eligiblity(sheet):
    values_list = sheet.col_values(1)
    if len(values_list)>3:
        raise Outside_Respec_Range

def add_points(sheet,session):
    points_earned = []
    
    list1 = sheet.get_all_values()[1][2:5]

    list2 = sheet.get_all_values()[2][2:5]

    points_earned.extend(list1)
    points_earned.extend(list2)

    if session['character_details']['bloodline'].lower() not in ['human','effendal']:
        points=-20
    else:
        points=-40

    for point in points_earned:
        try:
            points+=int(point)
        except ValueError:
            continue
    
    return points

def parse_sheet(sheet_id,session):
    #some method to get the sheet link

    skills=[]

    url='https://docs.google.com/spreadsheets/d/1pJR1I8vtj53HHl0JtMiVFKyN0yMDMJE771WZ1zRDq6M/edit?gid=223854145#gid=223854145'

    sheet = Character_Sheet(url)

    bloodline = sheet.character.acell('F3').value

    check_eligiblity(sheet.progression)

    if 'bloodline' not in session['character_details']:
        session['character_details']['bloodline']=bloodline
    
    session['points_earned'] = add_points(sheet.progression,session)

    session['character_details']['backstory'] = sheet.history.acell('A1').value

    session.modified=True

    list_of_rows = sheet.character.get_all_values()[9:]

    for row in list_of_rows:
        sides=[row[:2],row[4:6]]

        for side in sides:
            if side[0] in ['','General Skills','Magical Arts','Knowledge','Gathering/Crafting']:
                continue
            if side[1] in ['N/A','0']:
                continue
            if ' x' in side[0]:
                side[0]=side[0][:-3]
            
            skill_cost=SKILL_REF[side[0]]['Cost']
            skill_quant=abs(int(side[1])/skill_cost)
            side[1]=skill_quant
            skill_dets={'skill':side[0],'quantity':side[1]}
            skills.append(skill_dets)

    char_details={'bloodline':sheet.character.acell('F3').value,
                  'incentive_points':sheet.character.acell('G6').value,
                  'name':sheet.character.acell('F2').value,
                  'culture':sheet.character.acell('B4').value,
                  'faith':sheet.character.acell('B5').value,
                  'backstory':sheet.history.acell('A1').value}
    
    per_details={'name':sheet.character.acell('B2').value, 'email':sheet.character.acell('B3').value}

    return Existing_Sheet(skills,char_details,url,per_details)

def extract_character_sheet_skills(sheet):
    legacy_discount = 0
    list_of_rows = sheet.character.get_all_values()[9:]

    notes_index = next(
        (i for i, row in enumerate(list_of_rows) if row[0] == "Notes:"),
        None
    )

    list_of_rows = list_of_rows[:notes_index]

    skills={}

    for row in list_of_rows:
        sides=[row[:2],row[4:6]]

        for side in sides:
            if side[0] in ['','General Skills','Magical Arts','Knowledge','Gathering/Crafting']:
                continue
            if side[1] in ['N/A','0']:
                continue
            if ' x' in side[0]:
                side[0]=side[0][:-3]
            
            if 'Rank' in side[0]:
                match = re.search(r"Rank (\d+)", side[0])
                if match:
                    rank = int(match.group(1))
                    if 'Legacy' in side[0]:
                        side[1] = int(side[1]) + rank
                        legacy_discount += rank
                    match = re.search(r"L(\d+)", side[0])
                    if match:
                        side[1] = str(int(side[1]) + int(match.group(1)))
                        legacy_discount += int(match.group(1))

            if side[0] == 'Oathbound':
                side[0] = 'Oath Bound'
            if side[0][:11] == 'Native Lore':
                continue
            if side[0][:4] != 'Lore':
                side[0] = side[0].split(":", 1)[0]
            
            skill_cost=SKILL_REF[side[0]]['Cost']
            skill_quant=abs(int(side[1])/skill_cost)

            skills[side[0]] = skill_quant

    return skills, legacy_discount

def next_letter(letter):
    return chr(ord(letter) + 1)

def generate_cell(value,col,row):
    row=int(row)
    col=column_index_from_string(col)

    return gspread.Cell(row,col,value)

def extract_character_sheet_character_details(sheet):
    list_of_rows = sheet.character.get_all_values()[:8]
    details={}
    details['bloodline'] = list_of_rows[2][5].lower()
    details['culture'] = list_of_rows[3][1]
    details['faith'] = list_of_rows[6][1]
    details['flaw_points'] = 0
    details['flaws_added'] = []
    details['health points'] = 5
    details['name'] = list_of_rows[1][5]
    details['points'] = list_of_rows[6][2]
    details['incentive_points'] = 0

    return details

def extract_recent_sesh(sheet):
    list_of_rows = sheet.progression.get_all_values()

    total_cp = sheet.character.acell('C7').value

    for row in list_of_rows.copy():
        if row[0] == '':
            list_of_rows.remove(row)
    
    last_event = [list_of_rows[-1][0].split(' ')[1], list_of_rows[-1][1], list_of_rows[-1][2],
                  list_of_rows[-1][3], list_of_rows[-1][4],total_cp]
    
    return last_event

def character_sheet_to_dict(url):
    sheet = Character_Sheet(url)
    
    session={}

    skills, legacy = extract_character_sheet_skills(sheet)
    char_details = extract_character_sheet_character_details(sheet)
    last_event = extract_recent_sesh(sheet)
    total_cp = sheet.character.acell('C7').value

    session['gatherings_skills'] = {}
    session['character_details'] = char_details
    session['skills_added'] = skills
    session['legacy_discount'] = legacy
    session['gatherings_table'] = [last_event,]
    session['gathering'] = last_event[0]
    session['gatherings_skills'][last_event[0]] = skills.copy()
    session['total_cp'] = total_cp

    return session

from app import SKILL_REF

#azzy needs to change this to use a service account

gc = gspread.oauth()

templates=Templates()