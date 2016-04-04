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
    user = db.ReferenceField(User)
    timestamp = db.DateTimeField(default=datetime.utcnow)
    diary = db.DictField()
    
    def getAllByUniqueID(self, uniqueID):
        user = User()
        return Diary.objects(user=user.getByUniqueID(uniqueID)).order_by('-id')
    
    def getByUniqueIDAndID(self, uniqueID, _id):
        user = User()
        return Diary.objects(id=_id, user=user.getByUniqueID(uniqueID)).first()
    
    def addByUniqueID(self, uniqueID, diary):
        user = User()
        self.user = user.getByUniqueID(uniqueID)
        self.diary = diary
        return self.save()

    def serialize(self):
        d = {
                "id": str(self.id),
                "timestamp": self.timestamp.isoformat(),
                "diary": self.diary
            }
        
        return d

