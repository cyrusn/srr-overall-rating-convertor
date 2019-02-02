import json
import csv

from overallRating import OverallRating
from subject_scores import Subject_Scores
from constant import (
    basicInfoKeys,
    srr_overall_rating_codes,
    srr_percentile_codes,
    subjectIDs,
    subjectCodes,
    subject_info_dict,
)

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

        def addPerformance(student, subject_scores):
            performance = {}
            for subj in student.subjects:
                subjectPerformances = student.performances[subj]

                score = subjectPerformances["score"]
                level = subjectPerformances["level"]
                percentile = subject_scores.getPercentile(subj, score)
                overallRating = OverallRating(subj, level, percentile).result

                performance[subj] = {
                    "level": level,
                    "score": score,
                    "percentile": convertPercentileGrade(percentile),
                    "overallRating": overallRating,
                }
            return {**student.info, **performance}

        result = list()
        for student in self.student_list:
            student_with_performance = addPerformance(student, self.subject_scores)
            result.append(student_with_performance)
        return result

    def getJUPASReport(self, type):
        def validate(type):
            return type == "overallRating" or type == "percentile"

        def mapKeyBySubjectCodeAndMapValueByType(student, type):
            sts = dict()
            for key, val in student.items():
                if key in subjectIDs:
                    code = subject_info_dict[key]["code"]
                    sts[code] = val[type]
                else:
                    sts[key] = val
            return sts

        if validate(type):
            result = []
            for student in self.students:
                sts = mapKeyBySubjectCodeAndMapValueByType(student, type)
                result.append(sts)
            return result

    @property
    def statistic(self):
        def mapSubjectID(subjects):
            for key in subjectIDs:
                subjects[key] = list()

        def appendOverallRatingAndPercentile(subjects, student):
            for key, value in student.items():
                if key in subjectIDs:
                    subjects[key].append(value["overallRating"])
                    subjects[key].append(value["percentile"])

        def countBy(value, keys):
            result = dict()
            for rating in keys:
                result[rating] = value.count(rating)
            return result

        subjects = dict()
        mapSubjectID(subjects)
        for student in self.students:
            appendOverallRatingAndPercentile(subjects, student)

        statistic = list()
        for subject, value in subjects.items():
            keys = srr_overall_rating_codes + srr_percentile_codes
            result = countBy(value, keys)
            result["subject"] = subject
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
