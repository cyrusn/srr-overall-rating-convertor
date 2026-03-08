#!/usr/bin/env python3
import sys
import os
import argparse
from typing import List

# Add current directory to path to ensure imports work if run from root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import config FIRST to allow overriding
import config

def parse_args():
    parser = argparse.ArgumentParser(description="SRR Converter v2: Calculate student ratings and push to Google Sheets.")
    
    parser.add_argument(
        "-s", "--spreadsheet-id", "--ssid",
        type=str,
        help="Google Spreadsheet ID (overrides config.py)"
    )
    
    parser.add_argument(
        "-k", "--key-file",
        type=str,
        help="Path to Google Cloud Service Account JSON key file (overrides config.py)"
    )
    
    return parser.parse_args()

def main():
    # Parse args before importing modules that use config/constants
    args = parse_args()
    
    # Override config values if arguments provided
    if args.spreadsheet_id:
        config.SPREADSHEET_ID = args.spreadsheet_id
    if args.key_file:
        config.GOOGLE_KEY_FILE = args.key_file

    # Now import modules that depend on the updated config
    # We delay these imports so 'constant.py' uses the updated config values
    try:
        from student import Student, Term
        from report import Report
        from subject_scores import Subject_Scores
        from constant import (
            students,
            f6_report_dict,
            f5_term1_report_dict,
            f5_term2_report_dict,
            f5_term1_grade_dict,
            f5_term2_grade_dict,
            f6_grade_dict,
        )
    except Exception as e:
        print(f"\nCritical Error during initialization: {e}")
        print("Please check your configuration in v2/config.py or your command line arguments.")
        sys.exit(1)

    if not students:
        print("No students found. Please check your Google Sheets configuration and Spreadsheet ID.")
        return

    terms: List[Term] = [
        {
            "scores": f6_report_dict,
            "ratio": 0.5,
            "grades": f6_grade_dict
        },
        {
            "scores": f5_term2_report_dict,
            "ratio": 0.25,
            "grades": f5_term2_grade_dict
        },
        {
            "scores": f5_term1_report_dict,
            "ratio": 0.25,
            "grades": f5_term1_grade_dict
        },
    ]

    subject_scores = Subject_Scores()
    students_with_performances = list()

    print(f"Processing {len(students)} students...")
    for sts in students:
        student = Student(sts["regno"])
        performances = student.getPerformances(terms)
        subject_scores.importPerformances(performances)
        students_with_performances.append(student)

    print("Generating reports...")
    report = Report(students_with_performances, subject_scores, terms)
    report.writeAll()
    print("All tasks completed successfully.")

if __name__ == "__main__":
    main()
