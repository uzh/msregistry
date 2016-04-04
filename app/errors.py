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


from werkzeug.exceptions import HTTPException, NotFound


class TokenIsExpired(HTTPException):
    code = 400
    
    def __init__(self):
        self.message = 'Token is expired'
        self.error = 'token_expired'

class TokenIsInvalid(HTTPException):
    code = 400
    
    def __init__(self):
        self.message = 'Token signature is invalid'
        self.error = 'invalid_signature'

class IncorrectAudience(HTTPException):
    code = 400
    
    def __init__(self):
        self.message = 'Incorrect audience'
        self.error = 'invalid_audience'

class InsufficientRoles(HTTPException):
    code = 401
    
    def __init__(self):
        self.message = 'Insufficient Roles'
        self.error = 'unauthorized'

class InvalidHeader(HTTPException):
    code = 401
    
    def __init__(self):
        self.message = 'Insufficient Roles'
        self.error = 'invalid_header'

class TokenNotFound(HTTPException):
    code = 401
    
    def __init__(self):
        self.message = 'Token not found'
        self.error = 'invalid_header'
        
class AuthorizationHeaderMustStartWithBearer(HTTPException):
    code = 401
    
    def __init__(self):
        self.message = 'Authorization header must start with Bearer'
        self.error = 'invalid_header'

class AuthorizationHeaderIsExpected(HTTPException):
    code = 403
    
    def __init__(self):
        self.message = 'Authorization header is expected'
        self.error = 'authorization_required'

class ConsentInformationNotAccepted(HTTPException):
    code = 403
    
    def __init__(self):
        self.message = 'Consent Information not accepted'
        self.error = 'forbidden'

class UserNotFound(NotFound):
    code = 404
    
    def __init__(self, UniqueID):
        self.message = 'Couldn\'t found a User with UniqueID={}.'.format(UniqueID)
        self.error = 'not_found'

class DiaryNotFound(NotFound):
    code = 404
    
    def __init__(self, _id):
        self.message = 'Couldn\'t found a Diary with id={}.'.format(_id)
        self.error = 'not_found'
        
class SurveyNotFound(NotFound):
    code = 404
    
    def __init__(self, _id):
        self.message = 'Couldn\'t found a Survey with id={}.'.format(_id)
        self.error = 'not_found'

class MethodNotAllowed(HTTPException):
    code = 405
    
    def __init__(self, message):
        super(MethodNotAllowed, self).__init__()
        self.message = 'Method not Allowed'
        self.error = 'method_not_allowed'


