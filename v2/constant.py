import json
import ast
from google_sheets import GoogleSheet
from config import *


# Original constants
report_location = "report_output"
core_subjects = ["chi", "eng", "math", "csd"]
basicInfoKeys = ["regno", "classno", "classcode", "chname", "enname"]
srr_overall_rating_codes = ["R5", "R4", "R3", "R2", "R1"]
srr_percentile_codes = ["P5", "P4", "P3", "P2", "P1"]

def keyByRegno(lst):
    return {int(item["regno"]): item for item in lst if item.get("regno")}

def createStudentElectiveDict(lst):
    excluded_keys = core_subjects + [
        "regno",
        "classcode",
        "classno",
        "chname",
        "enname",
        "ename",
        "cname",
        "schoolYear",
        "classlevel"
    ]

    def get_keys(d, excluded_keys):
        # Only include keys that are subjects and have a non-empty value (0 is allowed)
        keys = []
        for key, val in d.items():
            if key in subjectIDs and key not in excluded_keys and val is not None and val != "":
                keys.append(key)
        return keys

    return {
        int(item["regno"]): [key for key in get_keys(item, excluded_keys)] 
        for item in lst if item.get("regno")
    }

# Initialize Google Sheets
gs = GoogleSheet()

# Sheet Names are imported from config.py

# Data loading
if gs.spreadsheet_id and gs.service:
    print(f"Loading data from Google Spreadsheet: {gs.spreadsheet_id}")
    
    # Subject Info
    subject_info_raw = gs.get_sheet_data(SHEET_SUBJECT_INFO)
    # Ensure we only take rows with a valid ID
    subject_info_dict = {item.pop('id'): item for item in subject_info_raw if item.get('id')}
    
    subjectIDs = list(subject_info_dict.keys())
    subjectCodes = [value["code"] for key, value in subject_info_dict.items()]
    
    # Students - Now using F6Report as the primary source for student basic info
    students = gs.get_sheet_data(SHEET_F6_REPORT)
    for s in students:
        if 'regno' in s and s['regno'] is not None: s['regno'] = int(s['regno'])
        if 'classno' in s and s['classno'] is not None: s['classno'] = int(s['classno'])
    students_dict = keyByRegno(students)
    
    # Reports
    def process_report(rows):
        cleaned_rows = []
        for r in rows:
            new_row = {}
            if 'regno' in r and r['regno'] is not None:
                new_row['regno'] = int(r['regno'])
            
            for key, val in r.items():
                if key == 'regno': continue
                
                # strict filtering: only include if not None and not empty string
                if val is not None and val != "":
                    if key not in basicInfoKeys:
                        try:
                            # Try to convert to float, but if 0, treat as data (score 0 is possible?)
                            # User said "empty do not mean get zero". So 0 is data. Empty is not.
                            new_row[key] = float(val)
                        except:
                            # keep as string if not float (e.g. grades like 5*)
                            new_row[key] = val
                    else:
                        new_row[key] = val
            cleaned_rows.append(new_row)
        return cleaned_rows

    f6_report_json = process_report(gs.get_sheet_data(SHEET_F6_REPORT))
    f6_report_dict = keyByRegno(f6_report_json)
    electives = createStudentElectiveDict(f6_report_json)
    
    f5_term1_report_json = process_report(gs.get_sheet_data(SHEET_F5_T1_REPORT))
    f5_term1_report_dict = keyByRegno(f5_term1_report_json)

    f5_term1_grade_json = process_report(gs.get_sheet_data(SHEET_F5_T1_GRADE))
    f5_term1_grade_dict = keyByRegno(f5_term1_grade_json)
    
    f5_term2_report_json = process_report(gs.get_sheet_data(SHEET_F5_T2_REPORT))
    f5_term2_report_dict = keyByRegno(f5_term2_report_json)
    
    f5_term2_grade_json = process_report(gs.get_sheet_data(SHEET_F5_T2_GRADE))
    f5_term2_grade_dict = keyByRegno(f5_term2_grade_json)
    
    f6_grade_json = process_report(gs.get_sheet_data(SHEET_F6_GRADE))
    f6_grade_dict = keyByRegno(f6_grade_json)
    
else:
    print("Warning: Google Sheets not configured or failed to initialize.")
    subject_info_dict = {}
    students = []
    students_dict = {}
    f6_report_dict = {}
    electives = {}
    f5_term1_report_dict = {}
    f5_term1_grade_dict = {}
    f5_term2_report_dict = {}
    f5_term2_grade_dict = {}
    f6_grade_dict = {}
    subjectIDs = []
    subjectCodes = []
