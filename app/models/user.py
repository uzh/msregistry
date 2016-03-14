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

class User(db.Document):
    uniqueID = db.StringField(unique=True, required=True)
    consent = db.BooleanField(default=False, required=True)
    member_since = db.DateTimeField(default=datetime.utcnow, required=True)
    last_seen = db.DateTimeField(default=datetime.utcnow, required=True)
    
    def createIfNotExistsByUniqueID(self, uniqueID):
        if User.objects(uniqueID=uniqueID).first() is None:
            self.uniqueID = uniqueID
            return self.save()
        
        return True
    
    def getByUniqueID(self, uniqueID):
        return User.objects(uniqueID=uniqueID).first()
    
    def getConsentByUniqueID(self, uniqueID):
        return User.objects(uniqueID=uniqueID).consent
    
    def setConsentByUniqueID(self, consent, uniqueID):
        if consent not in (True, False):
            return False
        return User.objects(uniqueID=uniqueID).update(consent=consent)
    
    def setLastSeenByUniqueID(self, uniqueID):
        return User.objects(uniqueID=uniqueID).update(last_seen=datetime.utcnow())
    
    def serialize(self):
        d = {
               "uniqueID": str(self.uniqueID),
               "consent": bool(self.consent)
            }
        d['member_since'] = self.member_since.isoformat()
        d['last_seen'] = self.last_seen.isoformat()
        
        return d

