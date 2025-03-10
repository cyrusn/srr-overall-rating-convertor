from typing import List

from student import Student, Term
from report import Report
from subject_scores import Subject_Scores
from constant import (
    students,
    f6_report_dict,
    f5_term1_report_dict,
    f5_term2_report_dict,
    f5_term2_grade_dict,
    f6_grade_dict,
    gradings_f5_term1,
    gradings_f5_term2,
    gradings_f6,
)

terms: List[Term] = [
    {
        "scores": f6_report_dict,
        "ratio": 0.5,
        "gradings": gradings_f6,
        "grades": f6_grade_dict
    },
    {
        "scores": f5_term2_report_dict,
        "ratio": 0.25,
        "gradings": gradings_f5_term2,
        "grades": f5_term2_grade_dict
    },
    {
        "scores": f5_term1_report_dict,
        "ratio": 0.25,
        "gradings": gradings_f5_term1
    },
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
