import json
from helper import keyByRegno
from student import Student
from subject import Subject
from report import Report
from subject_scores import Subject_Scores

with open("./data/private/students.json") as f:
    students_list = json.load(f)

subject_scores = Subject_Scores()
student_list = list()

for sts in students_list:
    student = Student(sts["regno"])
    performances = student.performances
    subject_scores.importPerformances(performances)
    student_list.append(student)

report = Report(student_list, subject_scores)
report.writeAll()

