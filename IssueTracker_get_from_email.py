# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 13:47:30 2020

IssueTracker_get_from_email

@author: Komputorz
"""

import imaplib
import email
from datetime import datetime
from time import sleep

import IssueTracker_model
import IssueTracker_utils
from IssueTracker_DAO import create_record
from IssueTracker_utils import identify_microscope


def it_get_from_email():
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
#        you need to provide email adress and password
        mail.login('', '')
        # mail read
        mail.select('Inbox')

        result, data = mail.search(None, '(SUBJECT "problem" UNSEEN)')

        problemy_z_kilku_wiadomosci = []
        for num in data[0].split():
            rv, data = mail.fetch(num, '(RFC822)')
            if rv != 'OK':
                print("ERROR getting message", num)

            message_total = email.message_from_bytes(data[0][1])
            try:
                message_title = email.header.decode_header(message_total['Subject'])[0][0].decode('utf8')
            except:
                message_title = email.header.decode_header(message_total['Subject'])[0][0]
            message_from = message_total["From"]
            date_tuple = email.utils.parsedate_tz(message_total['Date'])
            message_date = datetime.now()

            if date_tuple:
                message_date = datetime.fromtimestamp(
                    email.utils.mktime_tz(date_tuple))

            for part in message_total.walk():
                if part.get_content_type() == 'text/plain':
                    message_body = str(part.get_payload(decode=True).decode('utf-8')).replace("\\r\\n", " ")

            microscope_name = identify_microscope(message_title)
            if microscope_name == False:
                microscope_name = identify_microscope(message_body)
                if microscope_name == False:
                    print("nie można rozpoznać mikroskopu")
                    microscope_name = "nie można rozpoznać mikroskopu"
            problem, solution = IssueTracker_utils.extract_problem_and_solution_from_text(message_body)
            record = IssueTracker_model.Record(microscope_name, message_date, problem, solution, message_from)
            problemy_z_kilku_wiadomosci.append(record)
        mail.logout()
        return (problemy_z_kilku_wiadomosci)
    except Exception as e:
        print(e)
        sleep(15)
        it_get_from_email()


def main():
    while True:
        problemy_lista = it_get_from_email()
        for i in problemy_lista:
            create_record(i)
        sleep(15)


if __name__ == "__main__":
    main()





