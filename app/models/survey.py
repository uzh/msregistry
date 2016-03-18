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

class Survey(db.Document):
    timestamp = db.DateTimeField(default=datetime.utcnow)
    survey = db.DictField()
    
    def getById(self, _id):
        return Survey.objects(id=_id).first()
    
    def getAll(self):
        return Survey.objects().all()
    
    def add(self, survey):
        self.survey = survey
        return self.save()
    
    def deleteById(self, _id):
        return Survey.objects(id=_id).delete()
       
    def serialize(self):
        d = {
                "id": str(self.id),
                "timestamp": self.timestamp.isoformat(),
                "survey": self.survey
            }
        
        return d

