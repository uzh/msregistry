import unittest
import requests
import json
import urlparse
import yaml


## constants
#
# Keep in sync with the "TESTING" `config.yml` file!
#
USER_ID = 'd4c74594d841139328695756648b6bd6'
SURVEY_ID = '57631e93ec71bc7d2337482e'
USERNAME = "datamgr"
PASSWORD = "3v3n m0r3 s3cr3t"
URL_PREFIX = "http://127.0.0.1:5001/api/v1.0/{0}"
SURVEY = {
    'survey': {
        'sectionA': 'ALL REMOVED',
        'sectionB': '',
        'sectionC': 1
    },
    'tags': ['layer2'],
    'ongoing': True
}


def _do_http(method, request, payload=None):
    method_to_call = getattr(requests, method)
    return method_to_call(
        URL_PREFIX.format(request),
        auth=(USERNAME, PASSWORD),
        data=payload
    )

class AdminAPIsTestCase(unittest.TestCase):

    def test_get_all_surveys(self):
        r = _do_http("get","/admin/survey")
        self.assertEqual(r.status_code, 200)

    def test_get_all_surveys_by_user(self):
        r = _do_http("get","/admin/survey/user/{0}".format(USER_ID))
        self.assertEqual(r.status_code, 200)

    def test_update_survey_by_id(self):
        r = _do_http("post", "/admin/survey/{0}".format(SURVEY_ID),
                     payload=json.dumps(SURVEY))
        self.assertEqual(r.status_code, 200)

    # def test_delete_survey_by_id(self):
    #     r = _do_http("post", "/admin/survey/{0}".format(SURVEY_ID),
    #                  payload=json.dumps(SURVEY))
    #     self.assertEqual(r.status_code, 200)
