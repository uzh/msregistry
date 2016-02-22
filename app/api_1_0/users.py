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
from app.models.user import User

from ..decorators import requires_auth


@api.route('/user')
@requires_auth
def get_user():
    user = User(_request_ctx_stack.top.uniqueID)
    return jsonify(user.get().to_json())


@api.route('/user/language', methods=['GET'])
@requires_auth
def get_user_language():
    user = User(_request_ctx_stack.top.uniqueID)
    return jsonify(language=user.getLanguage())


@api.route('/user/language', methods=['POST'])
@requires_auth
def set_user_language():
    user = User(_request_ctx_stack.top.uniqueID)
    return jsonify(language=user.setLanguage(request.json['language']))

