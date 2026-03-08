import json
import csv
import os

from overallRating import OverallRating
from constant import (
    report_location,
    basicInfoKeys,
    srr_overall_rating_codes,
    srr_percentile_codes,
    subjectIDs,
    subjectCodes,
    subject_info_dict,
    gs
)


def sortFunc(sts):
    classcode = sts["classcode"]
    classno = sts["classno"]
    return f"{classcode}{classno:02}"


def reversed(lst):
    return lst[::-1]


statistic_column = (
    ["subject"]
    + reversed(srr_percentile_codes)
    + reversed(srr_overall_rating_codes)
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
                subjectPerformances = student.getPerformances(self.terms)[
                    subject_id]

                score = subjectPerformances["score"]
                grade = subjectPerformances["grade"]
                rank, size = subject_scores.getRank(subject_id, score)
                percentile = subject_scores.getPercentile(subject_id, score)
                overallRating = OverallRating(
                    subject_id, grade, percentile).result

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
            student_with_performance = mapPerformance(
                student, self.subject_scores)
            result.append(student_with_performance)
        return result

    def getJUPASReport(self, type):
        def validate(type):
            return type == "overallRating" or type == "percentile"

        def mapKeyBySubjectCodeAndMapValueByType(student, type):
            sts = dict()
            for key, val in student.items():
                if key in subjectIDs:
                    if isinstance(val, dict):
                         code = subject_info_dict[key]["code"]
                         sts[code] = val.get(type, '')
                    # If not dict, skip (it's raw data or empty)
                else:
                    sts[key] = val
            return sts

        if validate(type):
            result = []
            for student in self.students:
                sts = mapKeyBySubjectCodeAndMapValueByType(student, type)
                result.append(sts)
            result.sort(key=sortFunc)
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
                    if isinstance(value, dict):
                        subjects[key].append(value.get("overallRating", ""))
                        subjects[key].append(value.get("percentile", ""))
                    # else skip

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
        if not os.path.exists(report_location):
            os.makedirs(report_location)
        with open(
            f"{report_location}/students.json", "w", encoding="utf8"
        ) as f:
            json.dump(self.students, f, indent=2, ensure_ascii=False)
            print("Report is generated: student.json")

    def writeOverallRatingCSV(self):
        writeCSV(
            f"{report_location}/overallRating.csv",
            self.getJUPASReport("overallRating"),
            jupas_column,
        )
        print("Report is generated: overallRating.csv")

    def writePercentileCSV(self):
        writeCSV(
            f"{report_location}/percentile.csv",
            self.getJUPASReport("percentile"),
            jupas_column,
        )
        print("Report is generated: percentile.csv")

    def writeStatisticCSV(self):
        writeCSV(f"{report_location}/statistic.csv",
                 self.statistic, statistic_column)
        print("Report is generated: statistic.csv")

    def writeToGoogleSheets(self):
        if not gs or not gs.service or not gs.spreadsheet_id:
            print("Warning: Google Sheets not configured. Skipping write.")
            return

        def dicts_to_rows(dicts, headers):
            rows = [headers]
            for d in dicts:
                rows.append([d.get(h, "") for h in headers])
            return rows

        # Output Students
        sheet_students = os.getenv("SHEET_OUTPUT_STUDENTS", "OutputStudents")
        
        # Exact headers as requested: regno classcode classno chname enname + 17 subjects
        headers = [
            'regno', 'classcode', 'classno', 'chname', 'enname',
            'chi', 'eng', 'math', 'csd', 'bio', 'bafs', 'chem', 'chist', 
            'econ', 'geog', 'hist', 'ict', 'phy', 'ths', 'va', 'hmsc', 'm2'
        ]
        
        # Prepare rows
        output_rows = []
        for s in self.students:
            row = {}
            # Basic Info
            row['regno'] = s.get('regno', '')
            row['classcode'] = s.get('classcode', '')
            row['classno'] = s.get('classno', '')
            row['chname'] = s.get('chname', '')
            row['enname'] = s.get('enname', '')
            
            # Subject Data (Overall Rating)
            # Subject IDs in the system (chi, eng, etc.) match the requested shortcodes
            for sub_id in headers[5:]: # Subject columns start after enname
                if sub_id in s:
                    perf = s[sub_id]
                    if isinstance(perf, dict):
                        row[sub_id] = perf.get('overallRating', '')
                    else:
                        row[sub_id] = ''
                else:
                    row[sub_id] = ''
            
            output_rows.append(row)

        gs.create_sheet_if_missing(sheet_students)
        gs.clear_data(f"{sheet_students}!A1:ZZ1000")
        gs.update_data(f"{sheet_students}!A1", dicts_to_rows(output_rows, headers))
        print(f"Report is written to Google Sheet: {sheet_students}")

        # Overall Rating
        sheet_overall = os.getenv("SHEET_OUTPUT_OVERALL_RATING", "OutputOverallRating")
        overall_data = self.getJUPASReport("overallRating")
        gs.create_sheet_if_missing(sheet_overall)
        gs.clear_data(f"{sheet_overall}!A1:Z1000")
        gs.update_data(f"{sheet_overall}!A1", dicts_to_rows(overall_data, jupas_column))
        print(f"Report is written to Google Sheet: {sheet_overall}")

        # Percentile
        sheet_percentile = os.getenv("SHEET_OUTPUT_PERCENTILE", "OutputPercentile")
        percentile_data = self.getJUPASReport("percentile")
        gs.create_sheet_if_missing(sheet_percentile)
        gs.clear_data(f"{sheet_percentile}!A1:Z1000")
        gs.update_data(f"{sheet_percentile}!A1", dicts_to_rows(percentile_data, jupas_column))
        print(f"Report is written to Google Sheet: {sheet_percentile}")

        # Statistic
        sheet_statistic = os.getenv("SHEET_OUTPUT_STATISTIC", "OutputStatistic")
        statistic_data = self.statistic
        gs.create_sheet_if_missing(sheet_statistic)
        gs.clear_data(f"{sheet_statistic}!A1:Z1000")
        gs.update_data(f"{sheet_statistic}!A1", dicts_to_rows(statistic_data, statistic_column))
        print(f"Report is written to Google Sheet: {sheet_statistic}")

    def writeAll(self):
        # Still write locally if paths exist
        try:
            self.writeJSON()
            self.writeOverallRatingCSV()
            self.writePercentileCSV()
            self.writeStatisticCSV()
        except Exception as e:
            print(f"Notice: Local file writing skipped or failed: {e}")
            
        # Write to Google Sheets
        self.writeToGoogleSheets()


def writeCSV(filename, data, headers):
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    with open(filename, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for d in data:
            writer.writerow(d)
