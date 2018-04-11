# Copyright (C) 2018 University of Zurich.  All rights reserved.
#
"""
Implementation of the 'admin' API for the MS-Registry backend.

The 'admin' API allows limited modification of entities in the
database.
"""
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

__author__ = "Sergio Maffioletti <sergio.maffioletti@uzh.ch>"
__copyright__ = "Copyright (c) 2018 University of Zurich"


from datetime import datetime
from functools import wraps
import json
from syslog import *

from flask import abort, current_app, jsonify, request
from flask_httpauth import HTTPBasicAuth

from mongoalchemy.exceptions import BadValueException

from app.exceptions import (
    InvalidAuthentication,
    SurveyNotFound,
    MethodNotAllowed,
    UserNotFound
)
from app.models.survey import Survey
from app import utils

from . import api


httpbasicauth = HTTPBasicAuth()  # pylint: disable=invalid-name

# Simple username/password authentication.
@httpbasicauth.get_password
def get_cleartext_password(username):  # pylint: disable=missing-docstring
    if username == current_app.config['AUTH_USER']:
        return current_app.config['ACCESS_KEY']
    # 401 ("Unauthorized") seems the correct status code here: a
    # different user *may* be authenticated here, so retrying makes
    # sense
    raise InvalidAuthentication()

# pylint: disable=missing-docstring,invalid-name
def only_authorized_ip_addresses(fn):
    @wraps(fn)
    def with_auth_ip(*args, **kwargs):
        if request:
            if request.remote_addr not in current_app.config['AUTH_IP']:
                current_app.logger.warning(
                    "IP address {0} not allowed to access admin API.",
                    request.remote_addr)
                # 403 ("Forbidden") is the correct status code here
                # according to the HTTP spec ("Authorization will not
                # help and the request SHOULD NOT be repeated.")
                # Also, do not bother to return a properly formatted
                # JSON message for REST API consumption -- if somebody
                # is attempting unauthorized access, the last thing we
                # want to do is give 'em hints at how to properly do
                # their requests...
                abort(403)
        else:
            current_app.warning(
                "No request context, cannot check IP authorization!")
        return fn(*args, **kwargs)
    return with_auth_ip

class _AuditLog(object):
    _facility = {
        'KERN': LOG_KERN,
        'USER': LOG_USER,
        'MAIL': LOG_MAIL,
        'DAEMON': LOG_DAEMON,
        'AUTH': LOG_AUTH,
        'LPR': LOG_LPR,
        'NEWS': LOG_NEWS,
        'UUCP': LOG_UUCP,
        'CRON': LOG_CRON,
        'SYSLOG': LOG_SYSLOG,
        'AUTHPRIV': LOG_AUTH,
        'LOCAL0': LOG_LOCAL0,
        'LOCAL1': LOG_LOCAL1,
        'LOCAL2': LOG_LOCAL2,
        'LOCAL3': LOG_LOCAL3,
        'LOCAL4': LOG_LOCAL4,
        'LOCAL5': LOG_LOCAL5,
        'LOCAL6': LOG_LOCAL6,
        'LOCAL7': LOG_LOCAL7,
    }
    def __init__(self):
        self._syslog = None
    def __call__(self, msg):
        if self._syslog is None:
            openlog(
                ident=current_app.config.get(
                    'MONGOALCHEMY_DATABASE', 'msregistry-api'),
                logoption=(LOG_PID|LOG_CONS|LOG_NDELAY),
                facility=self._facility[
                    current_app.config.get(
                        'AUDIT_LOG_FACILITY', 'authpriv').upper()]
            )
        syslog(msg)

_audit_log = _AuditLog()

def add_to_audit_log(action, **data):
    data['action'] = action
    data['timestamp'] = datetime.now().isoformat()
    data['from'] = request.remote_addr
    _audit_log(json.dumps(data))


# Admin endpoints for Survey management

## GET operations

@api.route('/admin/survey', methods=['GET'])
@only_authorized_ip_addresses
@httpbasicauth.login_required
def get_all_surveys():
    """
    Get all surveys for all users.
    """
    survey = Survey()
    try:
        return jsonify(surveys=[ob.serialize() for ob in survey.getAll()])
    except ValueError as error:
        raise MethodNotAllowed(error.message)
    except BadValueException as error:
        raise MethodNotAllowed(error.message)
    finally:
        add_to_audit_log('get_all_surveys')


@api.route('/admin/survey/user/<string:_uid>', methods=['GET'])
@only_authorized_ip_addresses
@httpbasicauth.login_required
def get_all_surveys_by_user(_uid):
    """
    Get all surveys for a given user
    """
    survey = Survey()
    try:
        return jsonify(
            surveys=[
                ob.serialize()
                for ob in survey.getAllByUniqueID(
                    _uid,
                    utils.Time.Iso8601ToDatetime(request.args.get('from', None)),
                    utils.Time.Iso8601ToDatetime(request.args.get('until', None)),
                    (request.args.get('tags').split(',')
                     if request.args.get('tags', None) is not None
                     else None),
                    utils.json.Json._getJSONBool(request.args.get('ongoing', None)))])
    except ValueError as error:
        raise MethodNotAllowed(error.message)
    except BadValueException as error:
        raise MethodNotAllowed(error.message)
    except UserNotFound as error:
        raise UserNotFound(_uid)
    finally:
        add_to_audit_log('get_all_surveys_by_user', user_id=_uid)


## POST operations

@api.route('/admin/survey/<string:_id>', methods=['POST'])
@only_authorized_ip_addresses
@httpbasicauth.login_required
def update_user_survey_by_id(_id):
    """
    Update/replace existing survey by _id
    """
    survey = Survey()
    content = request.get_json(silent=True, force=True)
    try:
        return jsonify(
            success=bool(
                survey.updateByUniqueID(
                    _id,
                    content['survey'],
                    content['tags'],
                    content['ongoing'])))
    except ValueError as error:
        raise MethodNotAllowed(error.message)
    except BadValueException as error:
        raise MethodNotAllowed(error.message)
    except SurveyNotFound as error:
        raise SurveyNotFound(_id)
    finally:
        add_to_audit_log(
            'update_user_survey_by_id',
            survey_id=_id,
            replacement=content,
        )

## DELETE operations

@api.route('/admin/survey/<string:_id>', methods=['DELETE'])
@only_authorized_ip_addresses
@httpbasicauth.login_required
def delete_survey_by_id(_id):
    """
    Delete existing survey by _id
    """
    survey = Survey()
    try:
        return jsonify(success=bool(survey.deleteByUniqueID(_id)))
    except ValueError as error:
        raise MethodNotAllowed(error.message)
    except BadValueException as error:
        raise MethodNotAllowed(error.message)
    except SurveyNotFound as error:
        raise SurveyNotFound(_id)
    finally:
        add_to_audit_log(
            'delete_survey_by_id',
            survey_id=_id,
        )
