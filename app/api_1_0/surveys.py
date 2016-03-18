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


from flask import abort, jsonify, request

from . import api
from app.models.survey import Survey

from ..decorators import requires_auth, get_tokeninfo


@api.route('/survey')
def get_surveys():
    survey = Survey()
    return jsonify(surveys=[ob.serialize() for ob in survey.getAll()])


@api.route('/survey/add', methods=['POST'])
def add_survey():
    survey = Survey()
    content = request.get_json(silent=True)
    if content:
        return jsonify(success=bool(survey.add(content)))
    
    return jsonify(success=bool(False))


@api.route('/survey/get/<string:_id>', methods=['GET'])
def get_survey(_id):
    survey = Survey()
    result = survey.getById(_id)
    if result is not None:
        return jsonify(result.serialize())
    
    return abort(404)


@api.route('/survey/del/<string:_id>', methods=['GET'])
def del_survey(_id):
    survey = Survey()
    return jsonify(success=bool(survey.deleteById(_id)))

