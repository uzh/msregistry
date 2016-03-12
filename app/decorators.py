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


import jwt
import base64

from functools import wraps
from flask import request, _request_ctx_stack
from flask.ext.cors import cross_origin
from flask import current_app

from models.user import User
from app.main.errors import authorization_required, internal_server_error,\
    invalid_header, token_expired, invalid_audience, invalid_signature


def requires_auth(f):
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @wraps(f)
    def decorated(*args, **kwargs):
        app = current_app._get_current_object()
        auth = request.headers.get('Authorization', None)
        if not auth:
            return authorization_required('Authorization header is expected')
        
        parts = auth.split()

        if parts[0].lower() != 'bearer':
            return invalid_header('Authorization header must start with Bearer')
        elif len(parts) == 1:
            return invalid_header('Token not found')
        elif len(parts) > 2:
            return invalid_header('Authorization header must be Bearer + \s + token')

        token = parts[1]
        try:
            payload = jwt.decode(
                                 token,
                                 base64.b64decode(app.config['OAUTH_CLIENT_SECRET'].replace("_","/").replace("-","+")),
                                 audience=app.config['OAUTH_CLIENT_ID']
                                 )
        except jwt.ExpiredSignature:
            return token_expired('Token is expired')
        except jwt.InvalidAudienceError:
            return invalid_audience('Incorrect audience')
        except jwt.DecodeError:
            return invalid_signature('Token signature is invalid')
        
        _request_ctx_stack.top.uniqueID = payload['sub']
        
        user = User()
        if user.createIfNotExistsByUniqueID(_request_ctx_stack.top.uniqueID) == False:
            return internal_server_error('An error occurred while adding this user')
        
        user.setLastSeenByUniqueID(_request_ctx_stack.top.uniqueID)
        
        return f(*args, **kwargs)

    return decorated

