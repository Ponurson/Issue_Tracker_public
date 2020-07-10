# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 13:12:00 2020

@author: Komputorz
"""

import re
import pandas as pd
from xlwt import Workbook


def channel_check(channel):
    channels = [{"id": "C9715SMFB", "name": "zeiss-spinning-disc"},
                {"id": "C97GS33EG", "name": "leica-sp8"},
                {"id": "C9LLCFAC8", "name": "zeisslsm780"},
                {"id": "C9LLTTN48", "name": "af7000"},
                {"id": "C9LPD6A4R", "name": "zeiss_spinning_disc"},
                {"id": "C9M7BUC2F", "name": "zeiss_mp_invivo"},
                {"id": "C9M9EGXT6", "name": "mpphotomanipulation"},
                {"id": "C9M9F0NLU", "name": "leicasp8"},
                {"id": "C9MA9LERY", "name": "sigmavp_3view"},
                {"id": "C9MDT1Z9T", "name": "zeiss800"},
                {"id": "C9N5RGJEA", "name": "andor"},
                {"id": "CCYQL3MQQ", "name": "oldsp5"},
                {"id": "CL9UXRCCQ", "name": "tirf"},
                {"id": "GTH51183E", "name": "sp8"}]
    for i in channels:
        if channel == i['id']:
            return i['name']
    return False


def text_checker(text):
    if ("problem" in text.lower()) and ("rozwiazanie" in text.lower() or "rozwiązanie" in text.lower()):
        return True
    else:
        return False


def user_check(user_id):
#    you can provide names and id for slack users to know who is registering a problem  
    users = [{"id": "", "name": ""},
             {"id": "", "name": ""},
             {"id": "", "name": ""},
             {"id": "", "name": ""},
             {"id": "", "name": ""},
             {"id": "", "name": ""}]
    for i in users:
        if user_id == i['id']:
            return i['name']
    return False

def extract_problem_and_solution_from_text(text):
    message_body_cut_1st_problem = re.sub("problem([:,\-,=,\s,_])+", "", text, count=1, flags=re.IGNORECASE)
    problem_rozwiazanie = re.split("rozwi[a,ą]zanie([:,\-,=,\s,_])+", message_body_cut_1st_problem,
                                   flags=re.IGNORECASE, maxsplit=1)
    if len(problem_rozwiazanie) < 3:
        return problem_rozwiazanie[0], "BRAK"

    return problem_rozwiazanie[0], problem_rozwiazanie[-1]


def identify_microscope(message_content):
    test_string = message_content.lower()
    if "sp8" in test_string:
        return ("Leica_SP8_SMD")
    if "sp5" in test_string or ("dmi" in test_string and "6000" in test_string ):
        return ("Leica_SP5")
    elif "andor" in test_string:
        return ("Andor_DSD2")
    elif "spinning" in test_string or "spining" in test_string:
        return ("Zeiss_Spinning_Disc")
    elif "olympus" in test_string or "olimpus" in test_string:
        return ("Olympus_VS110")
    elif "tirf" in test_string:
        return ("Zeiss_TIRF")
    elif (("photo" in test_string and
           "manipulation" in test_string) or
          ("foto" in test_string and
           "manipulacj" in test_string)):
        return ("Zeiss_MP_PhotoManipulation")
    elif ("invivo" in test_string or
          "in vivo" in test_string or
          "in_vivo" in test_string or
          "in-vivo" in test_string):
        return ("Zeiss_MP_InVivo")
    elif "780" in test_string:
        return ("Zeiss_LSM780")
    elif "airy" in test_string or "800" in test_string:
        return ("Zeiss_LSM800_Airyscan")
    elif ("af" in test_string and
          "7000" in test_string):
        return ("Leica_AF_7000_Live")
    elif ("sigma" in test_string and
        "service" in test_string):
        return ("SEM_Zeiss_SigmaVP_3View_Service")
    elif "sigma" in test_string:
        return ("SEM_Zeiss_SigmaVP_3View")
    else:
        return False


def it_create_excel():
    wb = Workbook()
    ws1 = wb.add_sheet('Leica_SP8_SMD')
    ws2 = wb.add_sheet('Leica_SP5')
    ws1 = wb.add_sheet('Andor_DSD2')
    ws1 = wb.add_sheet('Zeiss_Spinning_Disc')
    ws1 = wb.add_sheet('Olympus_VS110')
    ws1 = wb.add_sheet('Zeiss_TIRF')
    ws1 = wb.add_sheet('Zeiss_MP_PhotoManipulation')
    ws1 = wb.add_sheet('Zeiss_MP_InVivo')
    ws1 = wb.add_sheet('Zeiss_LSM780')
    ws1 = wb.add_sheet('Zeiss_LSM800_Airyscan')
    ws1 = wb.add_sheet('Leica_AF_7000_Live')
    ws1 = wb.add_sheet('SEM_Zeiss_SigmaVP_3View')
    ws1 = wb.add_sheet('SEM_Zeiss_SigmaVP_3View_Service')

    wb.save("Issue_tracker_test.xls")

def get_excel_file(ISSUE_TRACKER_FILE):
    xls = pd.ExcelFile(ISSUE_TRACKER_FILE)
    issues_python_form = {}
    for i in xls.sheet_names:
        pojedynczy_sheet = pd.read_excel(xls, i)
        issues_python_form.update({i: pojedynczy_sheet})
    return issues_python_form