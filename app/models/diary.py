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

from app import utils


class Diary(db.Document):
    user = db.ObjectIdField(User)
    timestamp = db.DateTimeField(default=datetime.utcnow())
    diary = db.DictField(db.AnythingField(), required=True)
    
    def getAllByUniqueID(self, uniqueID, from_datetime_iso8601=None, until_datetime_iso8601=None):
        if from_datetime_iso8601 is not None:
            from_datetime = utils.Time.Iso8601ToDatetime(from_datetime_iso8601)
        else:
            from_datetime = datetime.min
        
        if until_datetime_iso8601 is not None:
            until_datetime = utils.Time.Iso8601ToDatetime(until_datetime_iso8601)
        else:
            until_datetime = datetime.max
        
        return Diary.query.filter(Diary.user == User().query.filter(User.uniqueID == uniqueID, ).first().mongo_id,
                                  ({'timestamp': {'$gte': from_datetime, '$lte': until_datetime}})).all()
    
    def getByUniqueIDAndID(self, uniqueID, _id):
        return Diary.query.filter(Diary.user == User().query.filter(User.uniqueID == uniqueID).first().mongo_id, Diary.mongo_id == _id).first()
    
    def addByUniqueID(self, uniqueID, diary):
        self.user = User().query.filter(User.uniqueID == uniqueID).first().mongo_id
        self.diary = diary
        self.save()
        return True
    
    def serialize(self):
        d = {
                "id": str(self.mongo_id),
                "timestamp": self.timestamp.isoformat(),
                "diary": self.diary
            }
        
        return d


