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


from datetime import datetime
from app import db

from user import User


class Diary(db.Document):
    user = db.ObjectIdField(User)
    timestamp = db.DateTimeField(required=True)
    diary = db.DictField(db.AnythingField(), required=True)
    
    def getAll(self):
        return Diary.query.all()
    
    def getAllByUniqueID(self, uniqueID, from_datetime=None, until_datetime=None):
        query = db.session.query(Diary)
        
        query.filter(Diary.user == User().query.filter(User.uniqueID == uniqueID).first().mongo_id)
        
        if from_datetime is not None:
            query.filter(Diary.timestamp >= from_datetime)
        
        if until_datetime is not None:
            query.filter(Diary.timestamp <= until_datetime)
        
        return query.all()
    
    def getByUniqueIDAndID(self, uniqueID, _id):
        return Diary.query.filter(Diary.user == User().query.filter(User.uniqueID == uniqueID)
                                  .first().mongo_id, Diary.mongo_id == _id).first()
    
    def addByUniqueID(self, uniqueID, diary):
        self.user = User().query.filter(User.uniqueID == uniqueID).first().mongo_id
        self.timestamp = datetime.utcnow()
        self.diary = diary
        self.save()
        return True
    
    def updateByUniqueIDAndID(self, uniqueID, _id, diary):
        Diary.query.filter(Diary.user == User().query.filter(User.uniqueID == uniqueID).first().mongo_id,
                           Diary.mongo_id == _id).set(diary=diary, timestamp=datetime.utcnow()).execute()
        return True
    
    def serialize(self):
        d = {
                "id": str(self.mongo_id),
                "timestamp": self.timestamp.isoformat(),
                "diary": self.diary
            }
        
        return d


