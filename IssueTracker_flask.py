# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 14:31:28 2020

@author: Komputorz
"""
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
import ssl as ssl_lib
import certifi
import IssueTracker_DAO
import pandas as pd
import IssueTracker_model
import IssueTracker_utils
from datetime import datetime
from flask import request
from flask import jsonify
from flask_cors import CORS, cross_origin

#you need to provide credentials to use slack
slack_token = ""
slack_secret = ""

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
slack_events_adapter = SlackEventAdapter(slack_secret, "/slack/events", app)

slack_web_client = WebClient(token=slack_token)

onboarding_tutorials_sent = {}
user_handler_list = []

@slack_events_adapter.on("message")
def message(payload):
    event = payload.get("event", {})

    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")
    mic = IssueTracker_utils.identify_microscope(text)
#    bot id is neccessary
    if event.get('bot_id') == '':
        return

    if IssueTracker_utils.channel_check(channel_id) != False:
        if IssueTracker_utils.text_checker(text):
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            author = IssueTracker_utils.user_check(user_id)
            mic = IssueTracker_utils.identify_microscope(IssueTracker_utils.channel_check(channel_id))
            problem, solution = IssueTracker_utils.extract_problem_and_solution_from_text(text)
            record = IssueTracker_model.Record(mic, date, problem, solution, author)
            IssueTracker_DAO.create_record(record)
            slack_web_client.reactions_add(channel=channel_id, timestamp=event.get('ts'), name="thumbsup")
        return
    for i in range(len(user_handler_list)):
        if user_handler_list[i].user_id == user_id:
            try:
                line = user_handler_list[i].mic_array[int(text) - 1]
                out = line[0].strftime("%m/%d/%Y, %H:%M:%S") + '\n\n' + line[1] + '\n\nProblem: ' + line[2].replace(
                    "\n", " ") + '\nRozwiązanie: ' + line[3].replace("\n", " ")
                message = {"channel": channel_id,
                           "username": "IssueTracker",
                           "text": out}
                response = slack_web_client.chat_postMessage(**message)
                return
            except Exception as e:
                print(e)

    if mic != False:
        try:
            if IssueTracker_utils.text_checker(text):
                date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                author = IssueTracker_utils.user_check(user_id)
                problem, solution = IssueTracker_utils.extract_problem_and_solution_from_text(text)
                record = IssueTracker_model.Record(mic, date, problem, solution, author)
                IssueTracker_DAO.create_record(record)
                slack_web_client.reactions_add(channel=channel_id, timestamp=event.get('ts'), name="thumbsup")
                return
#            you need to provide path for excel file that will be used instead of a database
            issue_tracker_file = ""
            xls = pd.ExcelFile(issue_tracker_file)
            issues_python_form = {}
            for i in xls.sheet_names:
                pojedynczy_sheet = pd.read_excel(xls, i)
                issues_python_form.update({i: pojedynczy_sheet})
            problem_frame = issues_python_form[mic].values

            user_handler_exists = False
            for i in range(len(user_handler_list)):
                if user_handler_list[i].user_id == user_id:
                    user_handler_list[i].mic_array = problem_frame
                    user_handler_exists = True
            if not user_handler_exists:
                user_handler_list.append(User_Handler(user_id, problem_frame))

            out = ""
            for i in range(problem_frame.shape[0]):
                out += (str(i + 1) + ". " + problem_frame[i, 2]).replace("\n", " ") + "\n"
            message = {"channel": channel_id,
                       "username": "IssueTracker",
                       "text": out}
            response = slack_web_client.chat_postMessage(**message)
        except Exception as e:
            print(e)
            print(text)
            message = {"channel": channel_id,
                       "username": "IssueTracker",
                       "text": "wystąpił problem z odpowiedzią"}
            response = slack_web_client.chat_postMessage(**message)


class User_Handler:

    def __init__(self, user_id, mic_array):
        self.user_id = user_id
        self.mic_array = mic_array


@app.route("/IssueTracker/<mic>", methods=["GET"])
@cross_origin()
def printIssues(mic):
    print(request.headers.get('Host'))
    return jsonify(
        [ob.__dict__ for ob in IssueTracker_DAO.find_all_for_mic(IssueTracker_utils.identify_microscope(mic))])


@app.route("/IssueTracker/<mic>", methods=['POST'])
@cross_origin()
def createIssue(mic):
    data = request.json
    print(data)
    mic = IssueTracker_utils.identify_microscope(mic)
    record = IssueTracker_model.Record(mic=mic,
                                       date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                       problem=data["problem"],
                                       solution=data["solution"],
                                       name=data["name"])
    IssueTracker_DAO.create_record(record)
    return "success"


@app.route("/IssueTracker/<mic>/<id>", methods=['DELETE'])
@cross_origin()
def delete_issue(mic, id):
    mic = IssueTracker_utils.identify_microscope(mic)
    IssueTracker_DAO.delete_record(mic, id)
    return "success"


@app.route("/IssueTracker/<mic>/<id>", methods=['PUT'])
@cross_origin()
def update_issue(mic, id):
    mic = IssueTracker_utils.identify_microscope(mic)
    data = request.json
    record = IssueTracker_model.Record(mic=mic,
                                       date=data["date"],
                                       problem=data["problem"],
                                       solution=data["solution"],
                                       name=data["name"])
    IssueTracker_DAO.update_record(mic, id, record)
    return "success"


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    app.run(port=3000)
