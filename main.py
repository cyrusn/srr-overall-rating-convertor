from student import Student
from report import Report
from subject_scores import Subject_Scores
from constant import students_list

subject_scores = Subject_Scores()
student_list = list()

for sts in students_list:
    student = Student(sts["regno"])
    performances = student.performances
    subject_scores.importPerformances(performances)
    student_list.append(student)

report = Report(student_list, subject_scores)
report.writeAll()
