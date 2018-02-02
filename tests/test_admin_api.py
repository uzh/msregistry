import unittest
import requests
import json
import urlparse
import yaml

userID = 'd4c74594d841139328695756648b6bd6'
surveyID = '57631e93ec71bc7d2337482e'
username = "datamgr"
password = "3v3n m0r3 s3cr3t"
url_prefix = "http://127.0.0.1:5001/api/v1.0/{0}"
survey = {'survey': {'sectionA': 'ALL REMOVED', 'sectionB': '', 'sectionC': 1}, 'tags': ['layer2'], 'ongoing': True}


def get_response(method,request,payload=None):
    method_to_call = getattr(requests,method)
    return method_to_call(url_prefix.format(request),
                          auth=(username,
                                password),
                          data=payload
                          )

class AdminAPIsTestCase(unittest.TestCase):


    

    def test_addByUniqueID(self):
        r = get_response("get","/admin/survey")
        print r.status_code
        if r.status_code != 200:
            print r.text
        r = get_response("get","/admin/survey/user/{0}".format(userID))
        print r.status_code
        if r.status_code != 200:
            print r.text
        r = get_response("post",
                         "/admin/survey/{0}".format(surveyID),
                         payload=json.dumps(survey))
        print r.status_code
        if r.status_code != 200:
            print r.text
        # r = get_response("delete","/admin/survey/{0}".format(surveyID))

