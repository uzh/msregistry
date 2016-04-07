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

__author__ = "Filippo Panessa <filippo.panamenessa@uzh.ch>"
__copyright__ = ("Copyright (c) 2016 S3IT, Zentrale Informatik,"
" University of Zurich")


from datetime import datetime
from app import db

from role import Role


class User(db.Document):
    uniqueID = db.StringField(required=True)
    member_since = db.DateTimeField(default=datetime.utcnow(), required=True)
    last_seen = db.DateTimeField(default=datetime.utcnow(), required=True)
    birthdate = db.DateTimeField(default=None)
    sex = db.EnumField(db.StringField(), 'male', 'female', default=None)
    physician_contact_permitted = db.BoolField(default=False, required=True)
    medical_record_abstraction = db.BoolField(default=False, required=True)
    data_exchange_cohort = db.BoolField(default=False, required=True)
    signature = db.StringField(max_length=3, default=None)
    date_signed = db.DateTimeField(default=None)

    def _DatetimeToMDY(self, birthdate):
        return datetime.strptime(birthdate.isoformat(), "%Y-%m-%dT%H:%M:%S").strftime("%d.%m.%Y")
    
    def _MDYToDatetime(self, birthdate):
        return datetime.strptime(birthdate, "%d.%m.%Y")
    
    def createIfNotExistsByUniqueID(self, uniqueID):
        if self.getByUniqueID(uniqueID) is None:
            self.uniqueID = uniqueID
            self.save()
        
        return True
    
    def getByUniqueID(self, uniqueID):
        return User.query.filter_by(uniqueID=uniqueID).first()
    
    def getUserConsentByUniqueID(self, uniqueID):
        if self.getByUniqueID(uniqueID).date_signed is not None:
            return True
        else:
            return False
    
    def setRelativeConsentByUniqueID(self, uniqueID, sex, birthdate, signature):
        
        if sex is None:
            raise ValueError('Bad value for field of type "sex". Reason: "Value cannot be null"')
        if birthdate is None:
            raise ValueError('Bad value for field of type "birthdate". Reason: "Value cannot be null"')
        if signature is None:
            raise ValueError('Bad value for field of type "signature". Reason: "Value cannot be null"')
        
        User.query.filter(User.uniqueID == uniqueID).set(
                                                         sex=sex,birthdate=self._MDYToDatetime(birthdate),
                                                         signature=signature,
                                                         date_signed=datetime.utcnow()
                                                         ).execute()
        return True
    
    def setPatientConsentByUniqueID(self, uniqueID, sex, birthdate, signature,
                                     physician_contact_permitted=None, 
                                     medical_record_abstraction=None,
                                     data_exchange_cohort=None):
    
        self.setRelativeConsentByUniqueID(uniqueID, sex, birthdate, signature)
        
        if physician_contact_permitted is None:
            raise ValueError('Bad value for field of type "physician_contact_permitted". Reason: "Value cannot be null"')
        if medical_record_abstraction is None:
            raise ValueError('Bad value for field of type "medical_record_abstraction". Reason: "Value cannot be null"')
        if data_exchange_cohort is None:
            raise ValueError('Bad value for field of type "data_exchange_cohort". Reason: "Value cannot be null"')
        
        User.query.filter(User.uniqueID == uniqueID).set(sex=sex, 
                                                         birthdate=self._MDYToDatetime(birthdate), 
                                                         signature=signature, 
                                                         physician_contact_permitted=physician_contact_permitted,
                                                         medical_record_abstraction=medical_record_abstraction,
                                                         data_exchange_cohort=data_exchange_cohort,
                                                         date_signed=datetime.utcnow()
                                                         ).execute()
        return True
    
    def setLastSeenByUniqueID(self, uniqueID):
        User.query.filter(User.uniqueID == uniqueID).set(last_seen=datetime.utcnow()).execute()
        return True
    
    def serialize(self, roles=[]):
        d = {
                "uniqueID": str(self.uniqueID),
                "member_since": self.member_since.isoformat(),
                "last_seen": self.last_seen.isoformat()
            }
    
        if Role.patient in roles or Role.relative in roles:
            d = {
                    "sex": self.sex,
                    "birthdate": self._DatetimeToMDY(self.birthdate) if self.birthdate is not None else None,
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


