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
import json
import urllib, urllib2

from functools import wraps
from flask import request, _request_ctx_stack
from flask.ext.cors import cross_origin
from flask import current_app

from app.models.role import Role
from app.models.user import User
from app.exceptions import InvalidApiUsage


def requires_auth(f):
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @wraps(f)
    def decorated(*args, **kwargs):
        app = current_app._get_current_object()
        auth = request.headers.get('Authorization', None)
        if not auth:
            raise InvalidApiUsage('Authorization header is expected', status_code=403, 
                                  payload={'code': 'authorization_required'})
        
        parts = auth.split()

        if parts[0].lower() != 'bearer':
            raise InvalidApiUsage('Authorization header must start with Bearer', status_code=401, 
                                  payload={'code': 'invalid_header'})
        elif len(parts) == 1:
            raise InvalidApiUsage('Token not found', status_code=401, 
                                  payload={'code': 'invalid_header'})
        elif len(parts) > 2:
            raise InvalidApiUsage('Authorization header must be Bearer + \s + token', status_code=401, 
                                  payload={'code': 'invalid_header'})
        token = parts[1]
        _request_ctx_stack.top.token = token
         
        try:
            payload = jwt.decode(
                                 token,
                                 base64.b64decode(app.config['OAUTH_CLIENT_SECRET'].replace("_","/").replace("-","+")),
                                 audience=app.config['OAUTH_CLIENT_ID']
                                 )
        except jwt.ExpiredSignature:
            raise InvalidApiUsage('Token is expired', status_code=400, 
                                  payload={'code': 'token_expired'})
        except jwt.InvalidAudienceError:
            raise InvalidApiUsage('Incorrect audience', status_code=400, 
                                  payload={'code': 'invalid_audience'})
        except jwt.DecodeError:
            raise InvalidApiUsage('Token signature is invalid', status_code=400, 
                                  payload={'code': 'invalid_signature'})
        
        _request_ctx_stack.top.uniqueID = payload['sub']
        
        user = User()
        if user.createIfNotExistsByUniqueID(_request_ctx_stack.top.uniqueID) == False:
            raise InvalidApiUsage('An error occurred while adding this user', status_code=500, 
                                  payload={'code': 'internal_server_error'})
        
        user.setLastSeenByUniqueID(_request_ctx_stack.top.uniqueID)
        
        return f(*args, **kwargs)

    return decorated


def requires_roles(roles=None):
    def decorated(method):
        @wraps(method)
        def f(*args, **kwargs):
            url = current_app.config['URL_TOKENINFO']
            
            values = {'id_token' : _request_ctx_stack.top.token }
            headers = { 'Accept' : 'application/json',
                        'Authorization' : 'Bearer %s' % _request_ctx_stack.top.token }
            
            data = urllib.urlencode(values)
            request = urllib2.Request(url, data, headers)
            
            json_data = urllib2.urlopen(request).read()
            json_object = json.loads(json_data)
            
            if 'app_metadata' in json_object and 'roles' in json_object:
                _request_ctx_stack.top.roles = json_object['app_metadata']['roles']
            else:
                _request_ctx_stack.top.roles = []
            
            if 'app_metadata' in json_object and 'lang' in json_object:
                _request_ctx_stack.top.lang = json_object['app_metadata']['lang']
            else:
                _request_ctx_stack.top.lang = current_app.config['DEFAULT_LANG']
            
            if Role.authorizedRoles(roles, _request_ctx_stack.top.roles) is False:
                raise InvalidApiUsage('Insufficient Roles', status_code=401, 
                                      payload={'code': 'unauthorized'})
            
            return method(*args, **kwargs)
            
        return f

    return decorated


def requires_consent(f):
    @cross_origin(headers=['Content-Type', 'Authorization'])
    @wraps(f)
    def decorated(*args, **kwargs):
        user = User()
        if user.getConsentByUniqueID(_request_ctx_stack.top.uniqueID) is False:
            raise InvalidApiUsage('Consent Information not accepted', status_code=401, 
                                  payload={'code': 'unauthorized'})
        
        return f(*args, **kwargs)

    return decorated

