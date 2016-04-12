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
from pprint import _id

__author__ = "Filippo Panessa <filippo.panessa@uzh.ch>"
__copyright__ = ("Copyright (c) 2016 S3IT, Zentrale Informatik,"
" University of Zurich")


from flask import jsonify, request, _request_ctx_stack

from . import api
from app.models.role import Role
from app.models.diary import Diary

from app import db

from app.auth.decorators import requires_auth, requires_roles, requires_consent

from app.errors import DiaryNotFound, MethodNotAllowed


@api.route('/user/diary', methods=['GET'])
@requires_auth
@requires_roles(roles=[Role.patient, Role.relative])
def get_user_diary():
    diary = Diary()
    return jsonify(diaries=[ob.serialize() for ob in diary.getAllByUniqueID(_request_ctx_stack.top.uniqueID,
                                                                            request.args.get('from', None),
                                                                            request.args.get('until', None))])


@api.route('/user/diary/<string:_id>', methods=['GET'])
@requires_auth
@requires_roles(roles=[Role.patient, Role.relative])
def get_user_diary_by_id(_id):
    diary = Diary()
    try:
        return jsonify(diary.getByUniqueIDAndID(_request_ctx_stack.top.uniqueID, _id).serialize())
    except:
        raise DiaryNotFound(_id)


@api.route('/user/diary', methods=['POST'])
@requires_auth
@requires_roles(roles=[Role.patient, Role.relative])
@requires_consent
def add_diary():
    diary = Diary()
    try:
        return jsonify(success=bool(diary.addByUniqueID(_request_ctx_stack.top.uniqueID, request.get_json(silent=True, force=True))))
    except ValueError as error:
        raise MethodNotAllowed(error.message)
    except db.BadValueException as error:
        raise MethodNotAllowed(error.message)


@api.route('/user/diary/<string:_id>', methods=['POST'])
@requires_auth
@requires_roles(roles=[Role.patient, Role.relative])
def post_user_diary_by_id(_id):
    diary = Diary()
    try:
        diary.getByUniqueIDAndID(_request_ctx_stack.top.uniqueID, _id).serialize()
    except:
        raise DiaryNotFound(_id)
    
    try:
        return jsonify(success=bool(diary.updateByUniqueIDAndID(_request_ctx_stack.top.uniqueID, _id, request.get_json(silent=True, force=True))))
    except ValueError as error:
        raise MethodNotAllowed(error.message)
    except db.BadValueException as error:
        raise MethodNotAllowed(error.message)


