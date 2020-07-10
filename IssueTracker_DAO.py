from time import sleep

import pandas as pd
from pandas import ExcelWriter
import IssueTracker_model

import IssueTracker_utils
#you need to provide path for excel file that will be used instead of a database
ISSUE_TRACKER_FILE = ""

def create_record(record):
    try:
        issues_python_form = IssueTracker_utils.get_excel_file(ISSUE_TRACKER_FILE)
        issues_python_form[record.mic] = issues_python_form[record.mic].append(
            {"Data": record.date,
             "Kto zgłosił": record.name,
             "Problem": record.problem,
             "Rozwiązanie": record.solution},
            ignore_index=True)
        writer = ExcelWriter(ISSUE_TRACKER_FILE)
        for key in issues_python_form:
            issues_python_form[key].to_excel(writer, key, index=False)
        writer.save()
    except Exception as e:
        print(e)
        sleep(15)
        create_record(record)


def find_all_for_mic(mic):
    issues_python_form = IssueTracker_utils.get_excel_file(ISSUE_TRACKER_FILE)
    problem_frame = issues_python_form[mic].values
    list_of_records = []
    for i in range(problem_frame.shape[0]):
        record = IssueTracker_model.Record(mic=mic,
                                           date=problem_frame[i, 0],
                                           problem=problem_frame[i, 2],
                                           solution=problem_frame[i, 3],
                                           name=problem_frame[i, 1])
        record.id = i
        list_of_records.append(record)
    return list_of_records


def delete_record(mic, id):
    try:
        issues_python_form = IssueTracker_utils.get_excel_file(ISSUE_TRACKER_FILE)
        delete_row = issues_python_form[mic].index[int(id)]
        issues_python_form[mic] = issues_python_form[mic].drop(delete_row)
        writer = ExcelWriter(ISSUE_TRACKER_FILE)
        for key in issues_python_form:
            issues_python_form[key].to_excel(writer, key, index=False)
        writer.save()
    except Exception as e:
        print(e)
        sleep(15)
        delete_record(mic, id)


def update_record(mic, id, record):
    try:
        issues_python_form = IssueTracker_utils.get_excel_file(ISSUE_TRACKER_FILE)
        update_row = issues_python_form[mic].index[int(id)]
        issues_python_form[mic].loc[update_row] = {record.date,
             record.name,
             record.problem,
             record.solution}
        writer = ExcelWriter(ISSUE_TRACKER_FILE)
        for key in issues_python_form:
            issues_python_form[key].to_excel(writer, key, index=False)
        writer.save()
    except Exception as e:
        print(e)
        sleep(15)
        update_row(mic, id, record)
