import json

core_subjects = ["chi", "eng", "math", "ls"]
basicInfoKeys = ["regno", "classno", "classcode", "chname", "enname"]
srr_overall_rating_codes = ["R5", "R4", "R3", "R2", "R1"]
srr_percentile_codes = ["P5", "P4", "P3", "P2", "P1"]


def keyByRegno(lst):
    return {item["regno"]: item for item in lst}


with open("./data/public/subjectInfo.json") as f:
    subject_info_dict = json.load(f)

with open("./data/private/students.json") as f:
    students_list = json.load(f)

with open("./data/public/subjectGrading.json") as f:
    gradings_f5_term1 = json.load(f)

with open("./data/public/subjectGrading.json") as f:
    gradings_f5_term2 = json.load(f)

with open("./data/public/subjectGrading.json") as f:
    gradings_f6 = json.load(f)

with open("./data/private/students.json") as students_file:
    students_dict = keyByRegno(json.load(students_file))

with open("./data/private/electives.json") as electives_file:
    electives = json.load(electives_file)

with open("./data/private/f6_report.json") as f6_report_file:
    f6_report_dict = keyByRegno(json.load(f6_report_file))

with open("./data/private/f5_term1_report.json") as f5_term1_report_file:
    f5_term1_report_dict = keyByRegno(json.load(f5_term1_report_file))

with open("./data/private/f5_term2_report.json") as f5_term2_report_file:
    f5_term2_report_dict = keyByRegno(json.load(f5_term2_report_file))

subjectIDs = list(subject_info_dict.keys())
subjectCodes = [value["code"] for key, value in subject_info_dict.items()]
