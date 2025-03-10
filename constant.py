import json

private_data_location = "./data/private/2024"
public_data_location = "./data/public"
report_location = "./report/2024"

core_subjects = ["chi", "eng", "math", "csd"]
basicInfoKeys = ["regno", "classno", "classcode", "chname", "enname"]
srr_overall_rating_codes = ["R5", "R4", "R3", "R2", "R1"]
srr_percentile_codes = ["P5", "P4", "P3", "P2", "P1"]


def keyByRegno(lst):
    return {item["regno"]: item for item in lst}


def createStudentElectiveDict(lst):
    excluded_keys = core_subjects + [
        "regno",
        "classcode",
        "classno",
        "chname",
        "enname",
    ]

    def get_keys(d, excluded_keys):
        return [key for key in d.keys() if key not in excluded_keys]

    return {
        item["regno"]: [key for key in get_keys(item, excluded_keys)] for item in lst
    }


with open(f"{public_data_location}/subjectInfo.json") as f:
    subject_info_dict = json.load(f)

with open(f"{public_data_location}/subjectGrading.json") as f:
    gradings_f5_term1 = json.load(f)

with open(f"{public_data_location}/subjectGrading.json") as f:
    gradings_f5_term2 = json.load(f)

with open(f"{public_data_location}/subjectGrading_f6.json") as f:
    gradings_f6 = json.load(f)

with open(f"{private_data_location}/students.json") as f:
    students = json.load(f)

with open(f"{private_data_location}/students.json") as students_file:
    students_dict = keyByRegno(json.load(students_file))

with open(f"{private_data_location}/f6_report.json") as f6_report_file:
    f6_report_json = json.load(f6_report_file)
    f6_report_dict = keyByRegno(f6_report_json)
    electives = createStudentElectiveDict(f6_report_json)

with open(f"{private_data_location}/f5_first_report.json") as f5_term1_report_file:
    f5_term1_report_dict = keyByRegno(json.load(f5_term1_report_file))

with open(f"{private_data_location}/f5_second_report.json") as f5_term2_report_file:
    f5_term2_report_dict = keyByRegno(json.load(f5_term2_report_file))

with open(f"{private_data_location}/f5_term2_grade_report.json") as f5_term2_grade_report:
    f5_term2_grade_dict = keyByRegno(json.load(f5_term2_grade_report))

with open(f"{private_data_location}/f6_grade_report.json") as f6_grade_report:
    f6_grade_dict = keyByRegno(json.load(f6_grade_report))

subjectIDs = list(subject_info_dict.keys())
subjectCodes = [value["code"] for key, value in subject_info_dict.items()]
