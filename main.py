from student import Student
from report import Report
from subject_scores import Subject_Scores
from constant import (
    students_list,
    f6_report_dict,
    f5_term1_report_dict,
    f5_term2_report_dict,
    gradings_f5_term1,
    gradings_f5_term2,
    gradings_f6,
)

terms = [
    {"score": f6_report_dict, "ratio": 0.5, "gradings": gradings_f6},
    {"score": f5_term2_report_dict, "ratio": 0.25, "gradings": gradings_f5_term2},
    {"score": f5_term1_report_dict, "ratio": 0.25, "gradings": gradings_f5_term1},
]

subject_scores = Subject_Scores()
student_list = list()

for sts in students_list:
    student = Student(sts["regno"])
    performances = student.getPerformances(terms)
    subject_scores.importPerformances(performances)
    student_list.append(student)

report = Report(student_list, subject_scores, terms)
report.writeAll()
