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


from flask import jsonify
from app.exceptions import ValidationError
from . import main

@main.app_errorhandler(403)
def forbidden(e):
    response = jsonify({'error': 'forbidden'})
    response.status_code = 403
    return response

@main.app_errorhandler(404)
def page_not_found(message):
    response = jsonify({'error': 'not found', 'message': message})
    response.status_code = 404
    return response

@main.app_errorhandler(500)
def internal_server_error(e):
    response = jsonify({'error': 'internal server error'})
    response.status_code = 500
    return response

@main.app_errorhandler(401)
def invalid_header(message):
    response = jsonify({'code': 'invalid_header', 'description': message})
    response.status_code = 401
    return response

@main.app_errorhandler(403)
def authorization_required(message):
    response = jsonify({'code': 'authorization_required', 'description': message})
    response.status_code = 403
    return response

@main.app_errorhandler(400)
def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response

@main.app_errorhandler(400)
def token_expired(message):
    response = jsonify({'code': 'token_expired', 'description': message})
    response.status_code = 400
    return response

@main.app_errorhandler(400)
def invalid_audience(message):
    response = jsonify({'code': 'invalid_audience', 'description': message})
    response.status_code = 400
    return response

@main.app_errorhandler(400)
def invalid_signature(message):
    response = jsonify({'code': 'invalid_signature', 'description': message})
    response.status_code = 400
    return response

@main.app_errorhandler(401)
def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


@main.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
