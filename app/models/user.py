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
from __builtin__ import True

__author__ = "Filippo Panessa <filippo.panamenessa@uzh.ch>"
__copyright__ = ("Copyright (c) 2016 S3IT, Zentrale Informatik,"
" University of Zurich")


from datetime import datetime
from app import db

from role import Role

GENDER = ('M', 'F')

class User(db.Document):
    uniqueID = db.StringField(unique=True, required=True)
    member_since = db.DateTimeField(default=datetime.utcnow, required=True)
    last_seen = db.DateTimeField(default=datetime.utcnow, required=True)
    birthdate = db.DateTimeField()
    sex = db.StringField(max_length=1)
    physician_contact_permitted = db.BooleanField(default=False, required=True)
    medical_record_abstraction = db.BooleanField(default=False, required=True)
    data_exchange_cohort = db.BooleanField(default=False, required=True)
    signature = db.StringField(max_length=2)
    date_signed = db.DateTimeField()

    
    def createIfNotExistsByUniqueID(self, uniqueID):
        if User.objects(uniqueID=uniqueID).first() is None:
            self.uniqueID = uniqueID
            return self.save()
        
        return True
    
    def getByUniqueID(self, uniqueID):
        try:
            return User.objects(uniqueID=uniqueID).first()
        except Exception:
            return None
    
    def getDateSignedByUniqueID(self, uniqueID):
        try:
            return User.objects(uniqueID=uniqueID).first().date_signed
        except Exception:
            return None
    
    def getConsentByUniqueID(self, uniqueID):
        try:
            return User.objects(uniqueID=uniqueID).first()
        except Exception:
            return None
    
    def setConsentByUniqueIDAndRoles(self, uniqueID, roles, consent):
        if type(consent) is not type(dict()):
            return False
        
        if 'birthdate' not in consent:
            return False
        elif 'sex' not in consent:
            return False
        elif 'signature' not in consent:
            return False
        elif consent['sex'] not in GENDER:
            return False
        
        if Role.patient in roles:
            if 'physician_contact_permitted' not in consent:
                return False
            elif 'medical_record_abstraction' not in consent:
                return False
            elif 'data_exchange_cohort' not in consent:
                return False
            
            try:
                return User.objects(uniqueID=uniqueID).update(
                                                              birthdate=datetime.strptime(consent['birthdate'], "%m-%d-%Y"),
                                                              sex=consent['sex'],
                                                              signature=consent['signature'],
                                                              physician_contact_permitted=consent['physician_contact_permitted'],
                                                              medical_record_abstraction=consent['medical_record_abstraction'],
                                                              data_exchange_cohort=consent['data_exchange_cohort'],
                                                              date_signed=datetime.utcnow
                                                              )
            except db.ValidationError:
                return False
            except ValueError:
                return False
        
        if Role.relative in roles:
            try:
                return User.objects(uniqueID=uniqueID).update(
                                                              birthdate=datetime.strptime(consent['birthdate'], "%m-%d-%Y"),
                                                              sex=consent['sex'],
                                                              signature=consent['signature'],
                                                              date_signed=datetime.utcnow
                                                              )
            except db.ValidationError:
                return False
            except ValueError:
                return False
            
        return False
    
    def setLastSeenByUniqueID(self, uniqueID):
        return User.objects(uniqueID=uniqueID).update(last_seen=datetime.utcnow())
    
    def serialize(self, roles=[]):
        d = {
                "uniqueID": str(self.uniqueID),
                "member_since": self.member_since.isoformat(),
                "last_seen": self.last_seen.isoformat()
            }
    
        if Role.patient in roles or Role.relative in roles:
            d = {
                    "sex": self.sex,
                    "birthdate": datetime.strptime(self.birthdate.isoformat(), "%Y-%m-%dT%H:%M:%S").strftime("%m-%d-%Y"),
                    "signature": self.signature
                }
            
            if self.date_signed is not None:
                d["date_signed"] = self.date_signed.isoformat()
            else:
                d["date_signed"] = None
        
        if Role.patient in roles:
            d["physician_contact_permitted"] = bool(self.physician_contact_permitted)
            d["medical_record_abstraction"] = bool(self.medical_record_abstraction)
            d["data_exchange_cohort"] = bool(self.data_exchange_cohort)
        
        return d


