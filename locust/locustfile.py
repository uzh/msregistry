# Copyright (C) 2016 University of Zurich.  All rights reserved.
#
# This file is part of MSRegistry Backend.
#
# MSRegistry Backend is free software: you can redistribute it and/or
# modify it under the terms of the version 3 of the GNU Affero General
# Public License as published by the Free Software Foundation, or any
# other later version.
#
# MSRegistry Backend is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the version
# 3 of the GNU Affero General Public License for more details.
#
# You should have received a copy of the version 3 of the GNU Affero
# General Public License along with MSRegistry Backend.  If not, see 
# <http://www.gnu.org/licenses/>.

__author__ = "Filippo Panessa <filippo.panessa@uzh.ch>"
__copyright__ = ("Copyright (c) 2016 S3IT, Zentrale Informatik,"
" University of Zurich")


from locust import HttpLocust, TaskSet, task

import requests
import json
import random

import yaml
    
authorization_headers = {}
informed_consent = False

def login():
    global authorization_headers
    
    with open("locust.yml", 'r') as ymlfile:
        config = yaml.load(ymlfile)
    
    url = config['AUTH_API_URL']
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    data = {'username': config['USERNAME'], 'password': config['PASSWORD']}
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        authorization_headers = {'authorization': 'Bearer %s' %(response.json()['data']['token'])}


class Diary(TaskSet):
    global authorization_headers, informed_consent
    
    diary_id = None       
    
    @task(10)
    def get_user_diary(self):
        response = self.client.get("/api/v1.0/user/diary", headers=authorization_headers)
        diaries = [survey for survey in response.json()['diaries']]
        self.diary_id  = random.choice(diaries)['id']
    
    @task(1)
    def get_user_diary_by_id(self):
        if self.diary_id is not None:
            self.client.get("/api/v1.0/user/diary/%s" % (self.diary_id), headers=authorization_headers)
    
    @task(1)
    def add_user_diary(self):
        if informed_consent is True:
            data = {"diary": {"any": "value"}}
            self.client.post("/api/v1.0/user/diary", headers=authorization_headers, data=json.dumps(data))
    
    @task(20)
    def update_user_diary_by_id(self):
        if informed_consent is True and self.diary_id is not None:
            data = {"diary": {"any": "value", "other": "whatever"}}
            self.client.post("/api/v1.0/user/diary/%s" % (self.diary_id), headers=authorization_headers, data=json.dumps(data))
    
    @task(5)
    def stop(self):
        self.interrupt()


class Survey(TaskSet):
    global authorization_headers, informed_consent
    
    survey_id = None       
    
    @task(10)
    def get_user_survey(self):
        response = self.client.get("/api/v1.0/user/survey", headers=authorization_headers)
        surveys = [survey for survey in response.json()['surveys']]
        self.survey_id  = random.choice(surveys)['id']
    
    @task(1)
    def get_user_survey_by_id(self):
        if self.survey_id is not None:
            self.client.get("/api/v1.0/user/survey/%s" % (self.survey_id), headers=authorization_headers)
    
    @task(1)
    def add_user_survey(self):
        if informed_consent is True:
            data = {"survey": {"value": "any"}, "tags": ["layer2"], "ongoing": True}
            self.client.post("/api/v1.0/user/survey", headers=authorization_headers, data=json.dumps(data))
    
    @task(20)
    def update_user_survey_by_id(self):
        if informed_consent is True and self.survey_id is not None:
            data = {"survey": {"value": "any", "other": "whatever"}, "tags": ["layer2"], "ongoing": True}
            self.client.post("/api/v1.0/user/survey/%s" % (self.survey_id), headers=authorization_headers, data=json.dumps(data))
    
    @task(5)
    def stop(self):
        self.interrupt()


class UserBehavior(TaskSet):
    tasks = {Diary:20, Survey: 10}
    
    global authorization_headers
    
    def on_start(self):
        login()
    
    @task(1)
    def auth_test(self):
        response = self.client.get("/auth/test", headers=authorization_headers)
        if response.json()['code'] != "authorization_success":
            response.status_code = 401

    @task(4)
    def get_user(self):
        self.client.get("/api/v1.0/user", headers=authorization_headers)

    @task(10)
    def get_user_consent(self):
        global informed_consent
        
        response = self.client.get("/api/v1.0/user/consent", headers=authorization_headers)
        informed_consent = response.json()['accepted']
    
    @task(2)
    def get_user_consent_info(self):
        self.client.get("/api/v1.0/user/consent/info", headers=authorization_headers)
    
    @task(1)
    def set_user_consent(self):
        data = {"physician_contact_permitted": True,
                "data_exchange_cohort": True,
                "medical_record_abstraction": True,
                "sex": "male",
                "signature": "FP",
                "birthdate": "18.09.1974"}
        self.client.post("/api/v1.0/user/consent", headers=authorization_headers, data=json.dumps(data))


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=400
    max_wait=900


