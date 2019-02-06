import json
from math import floor

from student import Student
from constant import subjectIDs


class Subject_Scores:
    def __init__(self):
        for id in subjectIDs:
            setattr(self, id, list())

    def getScores(self, subject):
        return getattr(self, subject)

    def getPercentile(self, subject, score):
        scores = self.getScores(subject)
        rank = scores.index(score)
        percentile = (rank / len(scores)) * 100
        return floor(percentile)

    def importPerformances(self, performances):
        for subjectKey, performance in performances.items():
            scores = self.getScores(subjectKey)
            scores.append(performance["score"])
            scores.sort(reverse=True)


if __name__ == "__main__":
    subj_stat = Subject_Scores()

    students = ["1214010", "1211017", "1211012", "1433023"]
    for s in students:
        sts = Student(s)
        performances = sts.performances
        subj_stat.importPerformances(performances)

    print(subj_stat.getScores("math"))
    print(subj_stat.getScores("chi"))
    print(subj_stat.getScores("hist"))
    print(subj_stat.getPercentile("math", 127.0))
