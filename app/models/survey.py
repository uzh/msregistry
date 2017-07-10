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


from flask import current_app

from datetime import datetime

from app import db

from user import User

import csv
import os
import uuid


class Survey(db.Document):
    user = db.ObjectIdField(User)
    timestamp = db.DateTimeField(required=True)
    survey = db.DictField(db.AnythingField(), required=True)
    tags = db.ListField(db.StringField(), required=True, default=[])
    ongoing = db.BoolField(default=True, required=True)
    
    def getAll(self):
        return Survey.query.all()
    
    def getAllByUniqueID(self, uniqueID, from_datetime=None, until_datetime=None,
                         tags=None, ongoing=None):
        query = db.session.query(Survey)
        
        query.filter(Survey.user == User().query.filter(User.uniqueID == uniqueID).first().mongo_id)
        
        if from_datetime is not None:
            query.filter(Survey.timestamp >= from_datetime)
        
        if until_datetime is not None:
            query.filter(Survey.timestamp <= until_datetime)
        
        if tags is not None:
            query.filter(Survey.tags.in_(tags))

        if ongoing is not None:
            query.filter(Survey.ongoing == ongoing)
        
        return query.all()
    
    def getByUniqueIDAndID(self, uniqueID, _id):
        return Survey.query.filter(Survey.user == User().query.filter(User.uniqueID == uniqueID)
                                   .first().mongo_id, Survey.mongo_id == _id).first()
    
    def addByUniqueID(self, uniqueID, survey, tags=[], ongoing=True):
        self.user = User().query.filter(User.uniqueID == uniqueID).first().mongo_id
        self.timestamp = datetime.utcnow()
        self.survey = survey
        self.tags = tags
        self.ongoing = ongoing
        self.save()
        return True
    
    def updateByUniqueIDAndID(self, uniqueID, _id, survey, tags, ongoing):
        Survey.query.filter(Survey.user == User().query.filter(User.uniqueID == uniqueID).first().mongo_id, 
                            Survey.mongo_id == _id).set(
                                                        survey=survey, 
                                                        tags=tags, 
                                                        ongoing=ongoing, 
                                                        timestamp=datetime.utcnow()).execute()
        return True
    
    def getCSVReportTagsAndOngoing(self):
        data = [ob.serializeTagsAndOngoing() for ob in self.getAll()]
        
        filename = str(uuid.uuid4()) + '.csv'
        path = os.path.join(current_app.config['REPORTS_DIR'], filename)
        csv_file = csv.writer(open(path, mode="w"))
        
        csv_file.writerow(['User ID', 'Survey ID', 'timestamp', 'tags', 'ongoing'])
        for item in data:
            # the `tags` field can apparently contain arbitrary Unicode data (limited to Latin-1, actually, looking
            # at the samples collected so far) so we need to escape it to UTF-8 in order to save into a CSV file
            # According to the Python 2.7 `csv` module docs, "The csv module does not directly support reading
            # and writing Unicode, but it is 8-bit-clean save for some problems with ASCII NUL characters."
            # so reading and writing UTF-8 is OK.
            csv_file.writerow([item['user_id'], item['id'], item['timestamp'], item['tags'].encode('utf-8'), item['ongoing']])
        
        return filename
    
    def serialize(self):
        d = {
                "id": str(self.mongo_id),
                "timestamp": self.timestamp.isoformat(),
                "survey": self.survey,
                "tags": self.tags,
                "ongoing": bool(self.ongoing)
            }
        
        return d

    def serializeTagsAndOngoing(self):
        d = {
                "user_id": User().query.filter(User.mongo_id == self.user).first().uniqueID,
                "id": str(self.mongo_id),
                "timestamp": self.timestamp.isoformat(),
                "tags": ', '.join(self.tags),
                "ongoing": bool(self.ongoing)
            }
        
        return d


