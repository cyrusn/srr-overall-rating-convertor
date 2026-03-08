import json
import os
import sys
from dotenv import load_dotenv
from google_sheets import GoogleSheet

# Add parent directory to path to find google_sheets.py
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Import from config.py in parent dir
try:
    from config import (
        SPREADSHEET_ID,
        SHEET_STUDENTS, SHEET_SUBJECT_INFO,
        SHEET_F6_REPORT, SHEET_F5_T1_REPORT, SHEET_F5_T2_REPORT, SHEET_F5_T2_GRADE, SHEET_F6_GRADE
    )
except ImportError:
    print("Error importing config.py. Ensure script is run with correct PYTHONPATH.")
    sys.exit(1)

gs = GoogleSheet()

# User requested fixed column order for report/student data
FIXED_HEADERS = [
    'regno', 'classcode', 'classno', 'chname', 'enname',
    'chi', 'eng', 'math', 'csd', 'bio', 'bafs', 'chem', 'chist', 
    'econ', 'geog', 'hist', 'ict', 'phy', 'ths', 'va', 'hmsc', 'm2'
]

def upload_json_to_sheet(json_path, sheet_name, transform_func=None):
    if not os.path.exists(json_path):
        print(f"Skipping {sheet_name}: File not found at {json_path}")
        return

    print(f"Reading {json_path}...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if transform_func:
        data = transform_func(data)

    if not data:
        print(f"Skipping {sheet_name}: No data found.")
        return

    if isinstance(data, dict):
        # Convert dict to list of dicts if needed (should be handled by transform_func usually)
        pass

    # Extract headers
    if isinstance(data, list) and len(data) > 0:
        # Collect ALL unique keys from ALL items
        all_keys = set()
        for item in data:
            all_keys.update(item.keys())
        
        # Determine final headers: FIXED_HEADERS first, then remaining keys sorted alphabetically
        final_headers = []
        
        # Add fixed headers if they exist in the data (or force them?)
        # User said "make all data... have same format... headers look like below"
        # So we force the FIXED_HEADERS order.
        # But if a fixed header is NOT in data, should we add it as empty column?
        # User implies standardized format, so yes, safer to include them.
        # However, for SubjectInfo or Grading sheets, these headers don't apply.
        # We should detect if this sheet is a "Report/Student" type sheet.
        # Heuristic: if data has 'regno', apply FIXED_HEADERS logic.
        
        is_student_data = any('regno' in item for item in data)
        
        if is_student_data:
            # Add all FIXED_HEADERS
            final_headers.extend(FIXED_HEADERS)
            
            # Add any other keys found in data (e.g. schoolYear, classlevel)
            other_keys = sorted([k for k in all_keys if k not in FIXED_HEADERS])
            final_headers.extend(other_keys)
        else:
            # For non-student sheets (e.g. SubjectInfo), just sort keys or use default
            # Keep simple sort or original logic if needed. 
            # Default to sorted list of all keys
            final_headers = sorted(list(all_keys))
            
        headers = final_headers
    else:
        print(f"Skipping {sheet_name}: Data format not supported (must be list of dicts).")
        return

    # Prepare rows
    rows = [headers]
    for item in data:
        row = []
        for h in headers:
            val = item.get(h, "")
            if isinstance(val, (list, dict)):
                val = str(val) # Convert complex types to string representation
            row.append(val)
        rows.append(row)

    print(f"Uploading to {sheet_name} ({len(data)} rows)...")
    gs.create_sheet_if_missing(sheet_name)
    gs.clear_data(f"{sheet_name}!A1:Z10000")
    gs.update_data(f"{sheet_name}!A1", rows)
    print(f"Uploaded {sheet_name}.")

# Transformations
def transform_subject_info(data):
    # Data is dict: { "chi": { "code": "...", "subject": "..." }, ... }
    # Convert to list: [ { "id": "chi", "code": "...", "subject": "..." }, ... ]
    result = []
    for key, val in data.items():
        item = {"id": key}
        item.update(val)
        result.append(item)
    return result

def transform_students(data):
    return data # Already list of dicts

def transform_report(data):
    return data # Already list of dicts

# Execution
if __name__ == "__main__":
    print(f"Starting upload to Spreadsheet: {SPREADSHEET_ID}")

    # Check connection and permissions
    try:
        gs.service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        print("Successfully connected to the spreadsheet.")
    except Exception as e:
        print(f"Error connecting to spreadsheet: {e}")
        if "403" in str(e):
            print("\n!!! PERMISSION DENIED !!!")
            print(f"Please share the spreadsheet with this service account email as Editor:\n")
            # Extract email from key file if possible, or just print a generic message
            try:
                with open("../v2/.env.key.json", "r") as f:
                    key_data = json.load(f)
                    print(f"  {key_data.get('client_email', 'UNKNOWN_EMAIL')}\n")
            except:
                print("  (Check .env.key.json for client_email)\n")
        sys.exit(1)

    # Public Data
    upload_json_to_sheet(os.path.join(V1_DATA_PUBLIC, "subjectInfo.json"), SHEET_SUBJECT_INFO, transform_subject_info)

    # Private Data
    upload_json_to_sheet(os.path.join(V1_DATA_PRIVATE, "students.json"), SHEET_STUDENTS, transform_students)
    upload_json_to_sheet(os.path.join(V1_DATA_PRIVATE, "f6_report.json"), SHEET_F6_REPORT, transform_report)
    upload_json_to_sheet(os.path.join(V1_DATA_PRIVATE, "f5_first_report.json"), SHEET_F5_T1_REPORT, transform_report)
    upload_json_to_sheet(os.path.join(V1_DATA_PRIVATE, "f5_second_report.json"), SHEET_F5_T2_REPORT, transform_report)
    upload_json_to_sheet(os.path.join(V1_DATA_PRIVATE, "f5_term2_grade_report.json"), SHEET_F5_T2_GRADE, transform_report)
    upload_json_to_sheet(os.path.join(V1_DATA_PRIVATE, "f6_grade_report.json"), SHEET_F6_GRADE, transform_report)

    print("Upload complete.")
