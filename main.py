from typing import List

from student import Student, Term
from report import Report
from subject_scores import Subject_Scores
from constant import (
    students,
    f6_report_dict,
    f5_term1_report_dict,
    f5_term2_report_dict,
    gradings_f5_term1,
    gradings_f5_term2,
    gradings_f6,
)

terms: List[Term] = [
    {"score": f6_report_dict, "ratio": 0.2, "gradings": gradings_f6},
    {"score": f5_term2_report_dict, "ratio": 0.4, "gradings": gradings_f5_term2},
    {"score": f5_term1_report_dict, "ratio": 0.4, "gradings": gradings_f5_term1},
]

subject_scores = Subject_Scores()
students_with_performances = list()

for sts in students:
    student = Student(sts["regno"])
    performances = student.getPerformances(terms)
    subject_scores.importPerformances(performances)
    students_with_performances.append(student)

report = Report(students_with_performances, subject_scores, terms)
report.writeAll()
