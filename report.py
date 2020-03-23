import json
import csv

from overallRating import OverallRating
from constant import (
    basicInfoKeys,
    srr_overall_rating_codes,
    srr_percentile_codes,
    subjectIDs,
    subjectCodes,
    subject_info_dict,
)


def reversed(lst):
    return lst[::-1]


statistic_column = (
    ["subject"] + reversed(srr_percentile_codes) + reversed(srr_overall_rating_codes)
)

jupas_column = basicInfoKeys + subjectCodes


class Report:
    def __init__(self, students_with_performances, subject_scores, terms):
        self.students_with_performances = students_with_performances
        self.subject_scores = subject_scores
        self.terms = terms

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

        def mapPerformance(student, subject_scores):
            performance = {}
            for subject_id in student.subjects:
                subjectPerformances = student.getPerformances(self.terms)[subject_id]

                score = subjectPerformances["score"]
                grade = subjectPerformances["grade"]
                rank, size = subject_scores.getRank(subject_id, score)
                percentile = subject_scores.getPercentile(subject_id, score)
                overallRating = OverallRating(subject_id, grade, percentile).result

                performance[subject_id] = {
                    "grade": round(grade, 2),
                    "score": round(score, 2),
                    "rank": rank,
                    "size": size,
                    "percentile": convertPercentileGrade(percentile),
                    "overallRating": overallRating,
                }
            return {**student.info, **performance}

        result = list()
        for student in self.students_with_performances:
            student_with_performance = mapPerformance(student, self.subject_scores)
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
        def createSubjectsDict():
            subjects = dict()
            for key in subjectIDs:
                subjects[key] = list()
            return subjects

        def appendOverallRatingAndPercentile(subjects, student):
            for key, value in student.items():
                if key in subjectIDs:
                    subjects[key].append(value["overallRating"])
                    subjects[key].append(value["percentile"])

        def countBy(value, keys):
            result = dict()
            for key in keys:
                result[key] = value.count(key)
            return result

        def countPerformance(performance, subject):
            ratings = srr_overall_rating_codes + srr_percentile_codes
            result = countBy(performance, ratings)
            result["subject"] = subject
            return result

        subjects = createSubjectsDict()
        statistic = list()

        for student in self.students:
            appendOverallRatingAndPercentile(subjects, student)

        for subject, performance in subjects.items():
            result = countPerformance(performance, subject)
            statistic.append(result)

        return statistic

    def writeJSON(self):
        with open("./report/students.json", "w", encoding="utf8") as f:
            json.dump(self.students, f, indent=2, ensure_ascii=False)
            print("Report is generated: student.json")

    def writeOverallRatingCSV(self):
        writeCSV(
            "./report/overallRating.csv",
            self.getJUPASReport("overallRating"),
            jupas_column,
        )
        print("Report is generated: overallRating.csv")

    def writePercentileCSV(self):
        writeCSV(
            "./report/percentile.csv", self.getJUPASReport("percentile"), jupas_column
        )
        print("Report is generated: percentile.csv")

    def writeStatisticCSV(self):
        writeCSV("./report/statistic.csv", self.statistic, statistic_column)
        print("Report is generated: statistic.csv")

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
