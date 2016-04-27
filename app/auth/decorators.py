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

from functools import wraps
from flask import request, _request_ctx_stack
from flask.ext.cors import cross_origin
from flask import current_app

from app.models.role import Role
from app.models.user import User

from app.errors import AuthorizationHeaderIsExpected, AuthorizationHeaderMustStartWithBearer, ConsentInformationNotAccepted
from app.errors import IncorrectAudience, InsufficientRoles, InvalidAlgorithm, OAuthReturnsIncorrectPayload
from app.errors import TokenIsExpired, TokenIsInvalid, TokenNotFound



def requires_auth(f):
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @wraps(f)
    def decorated(*args, **kwargs):
        app = current_app._get_current_object()
        auth = request.headers.get('Authorization', None)
        if not auth:
            raise AuthorizationHeaderIsExpected()
        
        parts = auth.split()

        if parts[0].lower() != 'bearer':
            raise AuthorizationHeaderMustStartWithBearer()
        elif len(parts) == 1:
            raise TokenNotFound()
        elif len(parts) > 2:
            raise AuthorizationHeaderMustStartWithBearer()
        token = parts[1]
        
        try:
            payload = jwt.decode(
                                 token, 
                                 open(app.config['OAUTH_CERTIFICATE'], 'r').read()
                                 )
        except jwt.ExpiredSignature:
            raise TokenIsExpired()
        except jwt.InvalidAudienceError:
            raise IncorrectAudience()
        except jwt.DecodeError:
            raise TokenIsInvalid()
        except jwt.exceptions.InvalidAlgorithmError:
            raise InvalidAlgorithm()
        
        try:
            _request_ctx_stack.top.uniqueID = payload['sub']
        except KeyError:
            raise OAuthReturnsIncorrectPayload()
        
        try:
            _request_ctx_stack.top.roles = payload['context']['role']
        except KeyError:
            raise OAuthReturnsIncorrectPayload()
        
        try:
            _request_ctx_stack.top.lang = payload['context']['lang']
        except KeyError:
            raise OAuthReturnsIncorrectPayload()
        
        user = User()
        user.createIfNotExistsByUniqueID(_request_ctx_stack.top.uniqueID)
        user.setLastSeenByUniqueID(_request_ctx_stack.top.uniqueID)
        
        return f(*args, **kwargs)

    return decorated


def requires_roles(roles=None):
    def decorated(method):
        @wraps(method)
        def f(*args, **kwargs):
            if Role.authorizedRoles(roles, _request_ctx_stack.top.roles) is False:
                raise InsufficientRoles()
            
            return method(*args, **kwargs)
            
        return f

    return decorated


def requires_consent(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = User()
        if user.getUserConsentByUniqueID(_request_ctx_stack.top.uniqueID) is False:
            raise ConsentInformationNotAccepted()
        
        return f(*args, **kwargs)

    return decorated


