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


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class TokenIsExpired(InvalidUsage):
    status_code = 400
    
    def __init__(self):
        InvalidUsage.__init__(self, 
                              message='Token is expired', 
                              payload={'code': 'token_expired'})

class TokenIsInvalid(InvalidUsage):
    status_code = 410

    def __init__(self):
        InvalidUsage.__init__(self, 
                              message='Token signature is invalid', 
                              payload={'code': 'invalid_signature'})

class IncorrectAudience(InvalidUsage):
    status_code = 400
    
    def __init__(self):
        InvalidUsage.__init__(self, 
                              message='Incorrect audience', 
                              payload={'code': 'invalid_audience'})

class InvalidAlgorithm(InvalidUsage):
    status_code = 400
    
    def __init__(self):
        InvalidUsage.__init__(self, 
                              message='Invalid Algorithm', 
                              payload={'code': 'invalid_algorithm'})

class InsufficientRoles(InvalidUsage):
    status_code = 401
    
    def __init__(self):
        InvalidUsage.__init__(self, 
                              message='Insufficient Roles', 
                              payload={'code': 'unauthorized'})

class InvalidHeader(InvalidUsage):
    status_code = 401
    
    def __init__(self):
        InvalidUsage.__init__(self, 
                              message='Invalid Header', 
                              payload={'code': 'invalid_header'})

class TokenNotFound(InvalidUsage):
    status_code = 401
    
    def __init__(self):
        InvalidUsage.__init__(self, 
                              message='Token not found', 
                              payload={'code': 'invalid_header'})
  
class AuthorizationHeaderMustStartWithBearer(InvalidUsage):
    status_code = 401
    
    def __init__(self):
        InvalidUsage.__init__(self, 
                              message='Authorization header must start with Bearer', 
                              payload={'code': 'invalid_header'})

class AuthorizationHeaderIsExpected(InvalidUsage):
    status_code = 403
    
    def __init__(self):
        InvalidUsage.__init__(self, 
                              message='Authorization header is expected', 
                              payload={'code': 'authorization_required'})

class ConsentInformationNotAccepted(InvalidUsage):
    status_code = 403
    
    def __init__(self):
        InvalidUsage.__init__(self, 
                              message='Consent Information not accepted', 
                              payload={'code': 'forbidden'})

class UserNotFound(InvalidUsage):
    status_code = 404
    
    def __init__(self, UniqueID):
        InvalidUsage.__init__(self, 
                              message='Couldn\'t found a User with UniqueID={}'.format(UniqueID), 
                              payload={'code': 'not_found'})

class DiaryNotFound(InvalidUsage):
    status_code = 404
    
    def __init__(self, _id):
        InvalidUsage.__init__(self, 
                              message='Couldn\'t found a Diary with id={}'.format(_id), 
                              payload={'code': 'not_found'})

class SurveyNotFound(InvalidUsage):
    status_code = 404
    
    def __init__(self, _id):
        InvalidUsage.__init__(self, 
                              message='Couldn\'t found a Survey with id={}'.format(_id), 
                              payload={'code': 'not_found'})

class MethodNotAllowed(InvalidUsage):
    status_code = 405
    
    def __init__(self, message):
        InvalidUsage.__init__(self, 
                              message=message, 
                              payload={'code': 'method_not_allowed'})

class OAuthReturnsIncorrectPayload(InvalidUsage):
    status_code = 500
    
    def __init__(self):
        InvalidUsage.__init__(self, 
                              message='OAuth Server returns incorrect payload', 
                              payload={'code': 'oauth_server_error'})


