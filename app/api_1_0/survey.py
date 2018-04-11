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


from flask import jsonify, request
from flask import _app_ctx_stack as stack

from . import api
from app.models.role import Role
from app.models.survey import Survey

from app import db

from app.auth.decorators import requires_auth, requires_roles, requires_consent

from app.exceptions import SurveyNotFound, MethodNotAllowed

from jsonschema import validate, ValidationError

from app import inputs
from app import utils

@api.route('/user/survey', methods=['GET'])
@requires_auth
def get_survey():
    survey = Survey()
    try:
        return jsonify(surveys=[ob.serialize() for ob in survey.getAllByUniqueID(stack.top.uniqueID,
                                                                                 utils.Time.Iso8601ToDatetime(request.args.get('from', None)),
                                                                                 utils.Time.Iso8601ToDatetime(request.args.get('until', None)),
                                                                                 request.args.get('tags').split(',') if request.args.get('tags', None) is not None else None,
                                                                                 utils.json.Json._getJSONBool(request.args.get('ongoing', None)),
                                                                                 )])
    except ValueError as error:
        raise MethodNotAllowed(error.message)
    except db.BadValueException as error:
        raise MethodNotAllowed(error.message)


@api.route('/user/survey/<string:_id>', methods=['GET'])
@requires_auth
@requires_roles(roles=[Role.patient, Role.relative])
def get_survey_by_id(_id):
    survey = Survey()
    try:
        return jsonify(survey.getByUniqueIDAndID(stack.top.uniqueID, _id).serialize())
    except:
        raise SurveyNotFound(_id)


@api.route('/user/survey', methods=['POST'])
@requires_auth
@requires_roles(roles=[Role.patient, Role.relative])
@requires_consent
def add_survey():
    survey = Survey()
    consent = request.get_json(silent=True, force=True)
    
    try:
        validate(consent, inputs.survey)
    except ValidationError as error:
        raise MethodNotAllowed(error.message)
    
    try:
        return jsonify(success=bool(survey.addByUniqueID(stack.top.uniqueID, 
                                                         consent['survey'],
                                                         consent['tags'],
                                                         consent['ongoing'])))
    except ValueError as error:
        raise MethodNotAllowed(error.message)
    except db.BadValueException as error:
        raise MethodNotAllowed(error.message)


@api.route('/user/survey/<string:_id>', methods=['POST'])
@requires_auth
@requires_roles(roles=[Role.patient, Role.relative])
@requires_consent
def update_survey_by_id(_id):
    survey = Survey()
    consent = request.get_json(silent=True, force=True)
    
    try:
        survey.getByUniqueIDAndID(stack.top.uniqueID, _id).serialize()
    except:
        raise SurveyNotFound(_id)
    
    try:
        validate(consent, inputs.survey)
    except ValidationError as error:
        raise MethodNotAllowed(error.message)
    
    try:
        return jsonify(success=bool(survey.updateByUniqueIDAndID(stack.top.uniqueID, _id, 
                                                                 consent['survey'],
                                                                 consent['tags'],
                                                                 consent['ongoing'])))
    except ValueError as error:
        raise MethodNotAllowed(error.message)
    except db.BadValueException as error:
        raise MethodNotAllowed(error.message)


