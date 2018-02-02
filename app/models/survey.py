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
from app.exceptions import SurveyNotFound, MethodNotAllowed, UserNotFound

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
    
    def getAll(self, from_datetime=None, until_datetime=None,
               tags=None, ongoing=None):
        """
        Return all surveys registered.
        By setting 'from_datetime'm, 'until_datetime', 'tags' or 'ongoing'
        one could further filter the scope of the query
        """
        # return Survey.query.all()
        query = db.session.query(Survey)

        if from_datetime is not None:
            query.filter(Survey.timestamp >= from_datetime)

        if until_datetime is not None:
            query.filter(Survey.timestamp <= until_datetime)

        if tags is not None:
            query.filter(Survey.tags.in_(tags))

        if ongoing is not None:
            query.filter(Survey.ongoing == ongoing)

        return query.all()

    def getAllByUniqueID(self, uniqueID, from_datetime=None, until_datetime=None,
                         tags=None, ongoing=None):
        """
        Return all surveys registered by a given user.
        By setting 'from_datetime'm, 'until_datetime', 'tags' or 'ongoing'
        one could further filter the scope of the query
        """

        # Check if user exists
        user = User().query.filter(User.uniqueID == uniqueID).first()
        try:
            assert not user is None, "User not found"
        except AssertionError as ax:
            raise UserNotFound(uniqueID)
            
        query = db.session.query(Survey)
        
        query.filter(Survey.user == user.mongo_id)
        
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

    def updateByUniqueID(self, _id, survey, tags, ongoing):
        """
        Verify survey exists.
        Then update its 'survey' content and save it back.
        """

        try:
            surveys = Survey.query.filter(Survey.mongo_id == _id)
            if surveys.count() == 0:
                raise SurveyNotFound(_id)
            if surveys.count() > 1:
                raise NonUniqueSurveyIDError(_id)
        except db.BadValueException as error:
            raise SurveyNotFound(_id)

        existing_survey_object = surveys.first()
        existing_survey_object.survey = survey
        existing_survey_object.tags = tags
        existing_survey_object.ongoing = ongoing
        existing_survey_object.timestamp=datetime.utcnow()
        existing_survey_object.save()
        return True
        
    def deleteByUniqueID(self, _id):
        """
        Verify survey exists.
        Then delete it.
        """
        try:
            surveys = Survey.query.filter(Survey.mongo_id == _id)
            if surveys.count() == 0:
                raise SurveyNotFound(_id)
            if surveys.count() > 1:
                raise NonUniqueSurveyIDError(_id)
        except db.BadValueException as error:
            raise SurveyNotFound(_id)

        existing_survey_object = surveys.first()
        existing_survey_object.remove()
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


