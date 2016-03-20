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


from flask import abort, jsonify, request, _request_ctx_stack

from . import api
from app.models.user import User

from ..decorators import requires_auth, requires_roles


@api.route('/user')
@requires_auth
def get_user():
    user = User()
    result = user.getByUniqueID(_request_ctx_stack.top.uniqueID)
    if result is not None:
        return jsonify(result.serialize())
    
    return abort(404)


@api.route('/user/consent', methods=['GET'])
@requires_auth
def get_user_consent():
    user = User()
    result = user.getConsentByUniqueID(_request_ctx_stack.top.uniqueID)
    if result is not None:
        return jsonify(consent=result)
    
    return abort(404)


@api.route('/user/consent', methods=['POST'])
@requires_auth
def set_user_consent():
    user = User()
    content = request.get_json(silent=True)
    if content and 'consent' in content:
        return jsonify(success=bool(user.setConsentByUniqueID(content['consent'],
                                                              _request_ctx_stack.top.uniqueID)))
        
    return jsonify(success=bool(False))


@api.route('/user/roles')
@requires_auth
@requires_roles(roles=None)
def get_user_roles():
    return jsonify(roles=_request_ctx_stack.top.roles)


@api.route('/user/lang')
@requires_auth
@requires_roles(roles=None)
def get_user_lang():
    return jsonify(lang=_request_ctx_stack.top.lang)

