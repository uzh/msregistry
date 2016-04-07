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
from app.models.role import Role

from app import db

from app.auth.decorators import requires_auth, requires_roles

from app.errors import UserNotFound, MethodNotAllowed

from jsonschema import validate, ValidationError
from app.inputs import user_consent_patient, user_consent_relative


@api.route('/user')
@requires_auth
def get_user():
    user = User()
    result = user.getByUniqueID(_request_ctx_stack.top.uniqueID)
    if result is not None:
        return jsonify(result.serialize())
    
    raise UserNotFound(_request_ctx_stack.top.uniqueID)


@api.route('/user/consent', methods=['GET'])
@requires_auth
@requires_roles(roles=[Role.patient, Role.relative])
def get_user_consent():
    user = User()
    result = user.getByUniqueID(_request_ctx_stack.top.uniqueID)
    
    if result is not None:
        return jsonify(result.serialize(_request_ctx_stack.top.roles))
    
    raise UserNotFound(_request_ctx_stack.top.uniqueID)


@api.route('/user/consent', methods=['POST'])
@requires_auth
@requires_roles(roles=[Role.patient, Role.relative])
def set_user_consent():
    user = User()
    consent = request.get_json(silent=True, force=True)
    
    if Role.relative in _request_ctx_stack.top.roles:
        try:
            validate(consent, user_consent_relative)
        except ValidationError as error:
            raise MethodNotAllowed(error.message)
        
        try:
            return jsonify(success=bool(user.setRelativeConsentByUniqueID(uniqueID=_request_ctx_stack.top.uniqueID,
                                                                          sex=consent['sex'], birthdate=consent['birthdate'], signature=consent['signature'])))
        except ValueError as error:
            raise MethodNotAllowed(error.message)
        except db.BadValueException as error:
            raise MethodNotAllowed(error.message)
    if Role.patient in _request_ctx_stack.top.roles:
        try:
            validate(consent, user_consent_patient)
        except ValidationError as error:
            raise MethodNotAllowed(error.message)
        
        try:
            return jsonify(success=bool(user.setPatientConsentByUniqueID(uniqueID=_request_ctx_stack.top.uniqueID,
                                                                      sex=consent['sex'], birthdate=consent['birthdate'], signature=consent['signature'],
                                                                      physician_contact_permitted=consent['physician_contact_permitted'], 
                                                                      medical_record_abstraction=consent['medical_record_abstraction'],
                                                                      data_exchange_cohort=consent['data_exchange_cohort'])))
        except ValueError as error:
            raise MethodNotAllowed(error.message)
        except db.BadValueException as error:
            raise MethodNotAllowed(error.message)
    else:
        raise MethodNotAllowed('Bad value for field of type "roles". Reason: "Value cannot be null"')


