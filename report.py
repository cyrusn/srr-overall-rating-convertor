import json
import csv

from overallRating import OverallRating
from subject_scores import Subject_Scores

with open("./data/public/subjectInfo.json") as f:
    subject_info_dict = json.load(f)

subjectKeys = list(subject_info_dict.keys())
subjectCodes = list([value["code"] for key, value in subject_info_dict.items()])

basicInfoKeys = ["regno", "classno", "classcode", "chname", "enname"]
srr_overall_rating_codes = ["R5", "R4", "R3", "R2", "R1"]
srr_percentile_codes = ["P5", "P4", "P3", "P2", "P1"]

statistic_column = (
    ["subject"] + srr_percentile_codes[::-1] + srr_overall_rating_codes[::-1]
)
jupas_column = basicInfoKeys + subjectCodes


class Report:
    def __init__(self, student_list, subject_scores):
        self.student_list = student_list
        self.subject_scores = subject_scores

    @property
    def students(self):
        result = list()
        for student in self.student_list:
            sts = {}
            for subj in student.subjects:
                subjectPerformances = student.performances[subj]

                score = subjectPerformances["score"]
                level = subjectPerformances["level"]
                percentile = self.subject_scores.getPercentile(subj, score)
                overallRating = OverallRating(subj, level, percentile).result

                sts[subj] = {
                    "level": level,
                    "score": score,
                    "percentile": convertPercentileGrade(percentile),
                    "overallRating": overallRating,
                }
            result.append({**student.info, **sts})
        return result

    def getJUPASReport(self, type):
        if type == "overallRating" or type == "percentile":
            result = []
            for student in self.students:
                sts = dict()
                for key, val in student.items():
                    if key in subjectKeys:
                        code = subject_info_dict[key]["code"]
                        sts[code] = val[type]
                    else:
                        sts[key] = val
                result.append(sts)
            return result

    @property
    def statistic(self):
        statistic = list()
        subjects = dict()
        for key in subjectKeys:
            subjects[key] = list()

        for student in self.students:
            for key, value in student.items():
                if key in subjectKeys:
                    subjects[key].append(value["overallRating"])
                    subjects[key].append(value["percentile"])

        for key, value in subjects.items():
            result = dict()
            for rating in srr_overall_rating_codes + srr_percentile_codes:
                result[rating] = value.count(rating)
            result["subject"] = key
            statistic.append(result)

        return statistic

    def writeJSON(self):
        with open("./report/students.json", "w", encoding="utf8") as f:
            json.dump(self.students, f, indent=2, ensure_ascii=False)

    def writeOverallRatingCSV(self):
        writeCSV(
            "./report/overallRating.csv",
            self.getJUPASReport("overallRating"),
            jupas_column,
        )

    def writePercentileCSV(self):
        writeCSV(
            "./report/percentile.csv", self.getJUPASReport("percentile"), jupas_column
        )

    def writeStatisticCSV(self):
        writeCSV("./report/statistic.csv", self.statistic, statistic_column)

    def writeAll(self):
        self.writeJSON()
        self.writeOverallRatingCSV()
        self.writePercentileCSV()
        self.writeStatisticCSV()


def writeCSV(filename, data, headers):
    with open(filename, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for d in data:
            writer.writerow(d)


def convertPercentileGrade(percentile):
    result = 0
    if percentile <= 10:
        result = 4
    elif percentile <= 25:
        result = 3
    elif percentile <= 50:
        result = 2
    elif percentile <= 75:
        result = 1
    else:
        result = 0

    return srr_percentile_codes[result]