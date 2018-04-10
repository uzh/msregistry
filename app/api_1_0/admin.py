# Copyright (C) 2018 University of Zurich.  All rights reserved.
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
__copyright__ = ("Copyright (c) 2018, 2019 S3IT, Zentrale Informatik,"
" University of Zurich")


from functools import wraps

from flask import abort, current_app, jsonify, request
from flask_httpauth import HTTPBasicAuth

from mongoalchemy.exceptions import BadValueException

from . import api
from app.models.survey import Survey

from app import db
from app.exceptions import (
    InvalidAuthentication,
    SurveyNotFound,
    MethodNotAllowed,
    UserNotFound
)
from app import utils


httpbasicauth = HTTPBasicAuth()

# Simple username/password authentication.
@httpbasicauth.get_password
def get_cleartext_password(username):
    if username == current_app.config['AUTH_USER']:
        return current_app.config['ACCESS_KEY']
    # 401 ("Unauthorized") seems the correct status code here: a
    # different user *may* be authenticated here, so retrying makes
    # sense
    raise InvalidAuthentication()

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


@api.route('/admin/survey/user/<string:_uid>', methods=['GET'])
@only_authorized_ip_addresses
@httpbasicauth.login_required
def get_all_surveys_by_user(_uid):
    """
    Get all surveys for a given user
    """
    survey = Survey()
    try:
        return jsonify(surveys=[ob.serialize() for ob in survey.getAllByUniqueID(_uid,
                                                                                 utils.Time.Iso8601ToDatetime(request.args.get('from', None)),
                                                                                 utils.Time.Iso8601ToDatetime(request.args.get('until', None)),
                                                                                 request.args.get('tags').split(',') if request.args.get('tags', None) is not None else None,
                                                                                 utils.json.Json._getJSONBool(request.args.get('ongoing', None)),
                                                                                 )])
    except ValueError as error:
        raise MethodNotAllowed(error.message)
    except BadValueException as error:
        raise MethodNotAllowed(error.message)
    except UserNotFound as error:
        raise UserNotFound(_uid)


## POST operations

@api.route('/admin/survey/<string:_id>', methods=['POST'])
@only_authorized_ip_addresses
@httpbasicauth.login_required
def update_user_survey_by_id(_id):
    """
    Update/replace existing survey by _id
    """
    survey = Survey()
    consent = request.get_json(silent=True, force=True)

    try:
        return jsonify(success=bool(survey.updateByUniqueID(_id,
                                                            consent['survey'],
                                                            consent['tags'],
                                                            consent['ongoing'])))
    except ValueError as error:
        raise MethodNotAllowed(error.message)
    except BadValueException as error:
        raise MethodNotAllowed(error.message)
    except SurveyNotFound as error:
        raise SurveyNotFound(_id)


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
