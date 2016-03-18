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

from ..decorators import requires_auth, get_tokeninfo

from app.main.errors import page_not_found


@api.route('/user')
@requires_auth
def get_user():
    user = User()
    result = user.getByUniqueID(_request_ctx_stack.top.uniqueID)
    if result is not None:
        return jsonify(result.serialize())
    
    return page_not_found('User not found')


@api.route('/user/consent', methods=['GET'])
@requires_auth
def get_user_consent():
    user = User()
    return jsonify(consent=user.getConsentByUniqueID(_request_ctx_stack.top.uniqueID))


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
@get_tokeninfo
def get_user_roles():
    return jsonify(roles=_request_ctx_stack.top.roles)


@api.route('/user/lang')
@requires_auth
@get_tokeninfo
def get_user_lang():
    return jsonify(lang=_request_ctx_stack.top.lang)

