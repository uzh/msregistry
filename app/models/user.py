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
    sex = db.EnumField(db.StringField(), ('male', 'female'), default=None)
    physician_contact_permitted = db.BoolField(default=False, required=True)
    medical_record_abstraction = db.BoolField(default=False, required=True)
    data_exchange_cohort = db.BoolField(default=False, required=True)
    signature = db.StringField(max_length=2, default=None)
    date_signed = db.DateTimeField(default=None)

    def getBirthdate(self):
        return datetime.strptime(self.birthdate.isoformat(), "%Y-%m-%dT%H:%M:%S").strftime("%m-%d-%Y")
     
    def setBirthdate(self, value):
        self.birthdate = datetime.strptime(value, "%m-%d-%Y")
    
    def createIfNotExistsByUniqueID(self, uniqueID):
        if self.getByUniqueID(uniqueID) is None:
            self.uniqueID = uniqueID
            self.save()
        
        return True
    
    def getByUniqueID(self, uniqueID):
        return User.query.filter_by(uniqueID=uniqueID).first()
        
    def getDateSignedByUniqueID(self, uniqueID):
        return self.getByUniqueID(uniqueID).date_signed
    
    def setConsentByUniqueIDAndRoles(self, uniqueID, roles, sex, birthdate, signature,
                                     physician_contact_permitted=None, 
                                     medical_record_abstraction=None,
                                     data_exchange_cohort=None):
        
        if sex is None:
            raise ValueError('Sex None')
        if birthdate is None:
            raise ValueError('Birthdate None')
        if signature is None:
            raise ValueError('Signature None')
        
        if Role.patient in roles:
            if physician_contact_permitted is None:
                raise ValueError('Physician Contact Permitted None')
            if medical_record_abstraction is None:
                raise ValueError('Medical Record Abstraction None')
            if data_exchange_cohort is None:
                raise ValueError('Data Exchange Cohort None')
            
            return User.objects(uniqueID=uniqueID).update(
                                                          sex=sex,
                                                          birthdate=birthdate,
                                                          signature=signature,
                                                          physician_contact_permitted=physician_contact_permitted,
                                                          medical_record_abstraction=medical_record_abstraction,
                                                          data_exchange_cohort=data_exchange_cohort,
                                                          date_signed=datetime.utcnow()
                                                          )
        
        elif Role.relative in roles:
            return User.objects(uniqueID=uniqueID).update(
                                                          sex=sex,
                                                          birthdate=birthdate,
                                                          signature=signature,
                                                          date_signed=datetime.utcnow
                                                          )
        
        raise ValueError('No Role provided')
    
    def setLastSeenByUniqueID(self, uniqueID):
        return User.query.filter(User.uniqueID == uniqueID).set(User.last_seen, datetime.utcnow()).execute()
    
    def serialize(self, roles=[]):
        d = {
                "uniqueID": str(self.uniqueID),
                "member_since": self.member_since.isoformat(),
                "last_seen": self.last_seen.isoformat()
            }
    
        if Role.patient in roles or Role.relative in roles:
            d = {
                    "sex": self.sex,
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


