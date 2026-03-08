from functools import reduce
from subject import Subject, Grading
from constant import students_dict, electives, core_subjects
from typing import TypedDict, List, Dict


class StudentDict(TypedDict):
    # student info
    regno: str
    classcode: str
    classno: int
    chname: str
    enname: str


class Term(TypedDict):
    # term info
    scores: List[dict]
    grades: List[dict]
    ratio: float


class Performance(TypedDict):
    # student performance
    score: float  # average score
    grade: float  # average predicted grade


class Student:
    def __init__(self, regno: str):
        self.regno = regno
        self.performances = None

    @property
    def info(self) -> StudentDict:
        return students_dict[self.regno]

    @property
    def subjects(self) -> List[str]:
        return core_subjects + electives[self.regno]

    def getPerformances(self, terms: List[Term]) -> Dict[str, Performance]:
        if self.performances is not None:
            return self.performances
            
        # print(self.regno) # Commented out to reduce I/O noise
        result = {}
        for subj in self.subjects:
            result[subj] = self.getSubjectPerformance(subj, terms)
        
        self.performances = result
        return result

    def getSubjectPerformance(
            self, subject_id: str,
            terms: List[Term]) -> Performance:
        regno = self.regno
        performance: Performance = {"score": 0, "grade": 0}

        def reducer(acc, term):
            subj = Subject(subject_id)
            
            # Skip if student not in this term's report
            if regno not in term["scores"]:
                return acc
                
            # Retrieve score, default to 0 if missing or None
            raw_score = term["scores"][regno].get(subject_id)
            score = raw_score if raw_score is not None else 0.0
            try:
                score = float(score)
            except (ValueError, TypeError):
                score = 0.0
            
            ratio = term["ratio"]
            
            grade = None
            if 'grades' in term.keys() and regno in term["grades"]:
                try:
                    # Retrieve grade, check for None
                    raw_grade = term["grades"][regno].get(subject_id)
                    if raw_grade is not None:
                         try:
                             grade = float(raw_grade)
                         except (ValueError, TypeError):
                             # Grade is present but not numeric (e.g. "ABS"), ignore it
                             grade = None
                except:
                    pass
            
            # Ensure grade is numeric for calculation
            try:
                if grade is None:
                    grade = 0.0
                else:
                    grade = float(grade)
            except (ValueError, TypeError):
                grade = 0.0

            # print(score, ratio, subj.id)
            acc["score"] += score * ratio
            # print(grade, regno)
            acc["grade"] += grade * ratio
            return acc

        return reduce(reducer, terms, performance)


if __name__ == "__main__":
    from constant import (
        f6_report_dict,
        f5_term1_report_dict,
        f5_term2_report_dict,
        f5_term1_grade_dict,
        f5_term2_grade_dict,
        f6_grade_dict
    )

    terms: List[Term] = [
        {"scores": f6_report_dict, "ratio": 0.5, "grades": f6_grade_dict},
        {"scores": f5_term2_report_dict, "ratio": 0.25, "grades": f5_term2_grade_dict},
        {"scores": f5_term1_report_dict, "ratio": 0.25, "grades": f5_term1_grade_dict},
    ]

    sts = Student("1211017")
    print(sts.info)
    print(sts.subjects)

    performances = sts.getPerformances(terms)
    print(performances)
