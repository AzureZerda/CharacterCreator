#azzy made a mess in here. fix it idiot

import gspread
from openpyxl.utils import column_index_from_string
import constants
from bloodline_skills import BLOODLINE_SKILLS
import datetime

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

def next_letter(letter):
    return chr(ord(letter) + 1)

def generate_cell(value,col,row):
    row=int(row)
    col=column_index_from_string(col)

    return gspread.Cell(row,col,value)

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
        not_on_sheet=['discord',]

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

def export_char(session):

    template_sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1S4jGc7nqan4eHvhuWuqbDKQJlKUd2FEe-g2JgSHsFlg/edit?gid=38564953#gid=38564953')

    template = template_sh.worksheet("Character")

    #sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1kOFjkm8D9JxEUL-i5zz3PlUelE_3B8nGUB1meIEYZN8/edit?gid=1580168798#gid=1580168798')

    #sh = gc.create('DUAL_TEST')
    sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1q71A6Yt6spkFtRbojMFi_fwN35eaXQ-cvM41IobujLc/edit?gid=269478616#gid=269478616')

    template.copy_to(sh.id)

    try:
        worksheet = sh.worksheet("Character")
        sh.del_worksheet(worksheet)
    except:
        pass

    result= sh.worksheet("Copy of Character")

    result.update_title("Character")

    try:
        worksheet = sh.worksheet("Character")
    
    except gspread.WorksheetNotFound:
        worksheet = sh.add_worksheet(title="Character", rows=100, cols=20)

    try:
        worksheet1 = sh.worksheet("Progression")
    
    except gspread.WorksheetNotFound:
        worksheet1 = sh.add_worksheet(title="Progression", rows=100, cols=20)
    
    sheet=Sheet_Constructor(session)

    sheet.construct(session)

    worksheet.update_cells(sheet.cells)

    worksheet1.update_cells(sheet.progression_cells)

    for cell in sheet.formula_cells:
        worksheet.update_acell(cell.coordinate,cell.value)

    for range in sheet.layout.merge_ranges:
        worksheet.merge_cells(range)

    for line in sheet.layout.starting_line:
        sheet.formats['skill_box_header']['cells'].extend([f'A{sheet.layout.starting_line[line]}',f'E{sheet.layout.starting_line[line]}'])
    
    for format in sheet.formats:
        for cell in sheet.formats[format]['cells']:
            worksheet.format(cell,sheet.formats[format]['format'])

    NPL_Rows=construct_NPL_Row(session,sh)

    #NPL_sh = gc.create('NPL_DEMO_1')
    NPL_sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1ArvwEyaAzGb3XvPSShNeEL_eHHrw2TfV9q4kbrY8Bwg/edit?gid=1599082411#gid=1599082411')

    try:
        worksheet = NPL_sh.worksheet("Demo")
    
    except gspread.WorksheetNotFound:
        worksheet = NPL_sh.add_worksheet(title="Demo", rows=100, cols=20)
    
    worksheet.update_cells(NPL_Rows)

def construct_NPL_Row(session,sheet):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row=3
    if 'second_culture' in session['character_details']:
        culture=f'{session['character_details']['culture']}/{session['character_details']['second_culture']}'
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


from app import SKILL_REF
#azzy needs to change this to use a service account
#gc = gspread.oauth()