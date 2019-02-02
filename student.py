import json
from helper import keyByRegno
from subject import Subject
from functools import reduce

with open("./data/private/students.json") as students_file:
    students_dict = keyByRegno(json.load(students_file))

with open("./data/private/f6_report.json") as f6_report_file:
    f6_report_dict = keyByRegno(json.load(f6_report_file))

with open("./data/private/f5_term1_report.json") as f5_term1_report_file:
    f5_term1_report_dict = keyByRegno(json.load(f5_term1_report_file))

with open("./data/private/f5_term2_report.json") as f5_term2_report_file:
    f5_term2_report_dict = keyByRegno(json.load(f5_term2_report_file))


class Student:
    def __init__(self, regno):
        self.regno = regno

    @property
    def info(self):
        return students_dict[self.regno]

    @property
    def subjects(self):
        # student may drop some electives, so the most accurate subject list
        # should be found in f6 report.
        report = f6_report_dict[self.regno]
        keys = list(report.keys())
        keys.remove("regno")

        return keys

    @property
    def performances(self):
        result = {}
        for subj in self.subjects:
            result[subj] = self.getPerformance(subj)
        return result

    def getPerformance(self, subject):
        regno = self.regno
        terms = [
            {"score": f6_report_dict[regno][subject], "ratio": 0.5},
            {"score": f5_term2_report_dict[regno][subject], "ratio": 0.25},
            {"score": f5_term1_report_dict[regno][subject], "ratio": 0.25},
        ]

        performance = {"score": 0, "level": 0}

        def reducer(acc, term):
            subj = Subject(subject)
            level = subj.toLevel(term["score"])
            acc["score"] += term["score"] * term["ratio"]
            acc["level"] += level * term["ratio"]
            return acc

        return reduce(reducer, terms, performance)


if __name__ == "__main__":
    sts = Student("1211017")
    print(sts.info)
    print(sts.subjects)

    performances = sts.performances
    print(performances)