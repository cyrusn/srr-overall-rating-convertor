from functools import reduce

from subject import Subject, Grading
from constant import students_dict, electives, core_subjects

from typing import TypedDict, List, Dict


class StudentDict(TypedDict):
    regno: str
    classcode: str
    classno: int
    chname: str
    enname: str


class Term(TypedDict):
    score: List[dict]
    ratio: float
    gradings: List[Grading]


class Performance(TypedDict):
    score: float  # average score
    grade: float  # average predicted grade


class Student:
    def __init__(self, regno: str):
        self.regno = regno

    @property
    def info(self) -> StudentDict:
        return students_dict[self.regno]

    @property
    def subjects(self) -> List[str]:
        return core_subjects + electives[self.regno]

    def getPerformances(self, terms: List[Term]) -> Dict[str, Performance]:
        result = {}
        for subj in self.subjects:
            result[subj] = self.getSubjectPerformance(subj, terms)
        return result

    def getSubjectPerformance(self, subject_id: str, terms: List[Term]) -> Performance:
        regno = self.regno
        performance: Performance = {"score": 0, "grade": 0}

        def reducer(acc, term):
            subj = Subject(subject_id)
            score = term["score"][regno][subject_id]
            gradings = term["gradings"]
            ratio = term["ratio"]
            grade = subj.scoreToGrade(score, gradings)
            acc["score"] += score * ratio
            acc["grade"] += grade * ratio
            return acc

        return reduce(reducer, terms, performance)


if __name__ == "__main__":
    from constant import (
        f6_report_dict,
        f5_term1_report_dict,
        f5_term2_report_dict,
        gradings_f5_term1,
        gradings_f5_term2,
        gradings_f6,
    )

    terms: List[Term] = [
        {"score": f6_report_dict, "ratio": 0.5, "gradings": gradings_f6},
        {"score": f5_term2_report_dict, "ratio": 0.25, "gradings": gradings_f5_term2},
        {"score": f5_term1_report_dict, "ratio": 0.25, "gradings": gradings_f5_term1},
    ]

    sts = Student("1211017")
    print(sts.info)
    print(sts.subjects)

    performances = sts.getPerformances(terms)
    print(performances)
