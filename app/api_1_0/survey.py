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


from flask import jsonify, request, _request_ctx_stack

from . import api
from app.models.role import Role
from app.models.survey import Survey

from app import db

from app.auth.decorators import requires_auth, requires_roles, requires_consent

from app.errors import SurveyNotFound, MethodNotAllowed


@api.route('/user/survey', methods=['GET'])
@requires_auth
def get_survey():
    survey = Survey()
    return jsonify(surveys=[ob.serialize() for ob in survey.getAllByUniqueID(_request_ctx_stack.top.uniqueID)])


@api.route('/user/survey/<string:_id>', methods=['GET'])
@requires_auth
@requires_roles(roles=[Role.patient, Role.relative])
def get_survey_by_id(_id):
    survey = Survey()
    try:
        return jsonify(survey.getByUniqueIDAndID(_request_ctx_stack.top.uniqueID, _id).serialize())
    except:
        raise SurveyNotFound(_id)
    

@api.route('/user/survey', methods=['POST'])
@requires_auth
@requires_roles(roles=[Role.patient, Role.relative])
@requires_consent
def add_survey():
    survey = Survey()
    try:
        return jsonify(success=bool(survey.addByUniqueID(_request_ctx_stack.top.uniqueID, request.get_json(silent=True, force=True))))
    except ValueError as error:
        raise MethodNotAllowed(error.message)
    except db.BadValueException as error:
        raise MethodNotAllowed(error.message)

