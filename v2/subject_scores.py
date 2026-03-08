from math import floor

from student import Student, Term, Performance
from constant import subjectIDs

from typing import Dict, List, Tuple


class Subject_Scores:
    def __init__(self):
        for id in subjectIDs:
            setattr(self, id, list())

    def getScores(self, subject_id: str) -> List[float]:
        return getattr(self, subject_id)

    def getRank(self, subject_id: str, score: float) -> Tuple[int, int]:
        """
        getRank return the tuple of the ranking and the total
        number of students of subject.
        """
        scores: List[float] = self.getScores(subject_id)
        scores.sort(reverse=True)
        rank = scores.index(score)
        return (rank, len(scores))

    def getPercentile(self, subject_id: str, score: float) -> float:
        (rank, size) = self.getRank(subject_id, score)
        percentile = (rank / size) * 100
        return floor(percentile)

    def importPerformances(self, performances: Dict[str, Performance]):
        #  import student's performance of each subjects
        for subject_id, performance in performances.items():
            scores: List[float] = self.getScores(subject_id)
            scores.append(performance["score"])


if __name__ == "__main__":
    from constant import (
        f6_report_dict,
        f5_term1_report_dict,
        f5_term2_report_dict,
        f5_term1_grade_dict,
        f5_term2_grade_dict,
        f6_grade_dict,
    )

    subj_stat = Subject_Scores()
    terms: List[Term] = [
        {"scores": f5_term1_report_dict, "ratio": 0.25, "grades": f5_term1_grade_dict},
        {"scores": f5_term2_report_dict, "ratio": 0.25, "grades": f5_term2_grade_dict},
        {"scores": f6_report_dict, "ratio": 0.5, "grades": f6_grade_dict},
    ]

    students = ["1214010", "1211017", "1211012", "1433023"]

    for s in students:
        sts = Student(s)
        performances = sts.getPerformances(terms)
        subj_stat.importPerformances(performances)

    print(subj_stat.getScores("math"))
    print(subj_stat.getScores("chi"))
    print(subj_stat.getScores("hist"))
    print(subj_stat.getPercentile("math", 127.0))
    print(subj_stat.getPercentile("math", 246.25))
