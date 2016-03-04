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

from serializer import Serializer

from sqlalchemy.exc import IntegrityError


class User(db.Model, Serializer):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    uniqueID = db.Column(db.String(64), nullable=False, unique=True, index=True)
    privacy_policy = db.Column(db.Boolean, default=False)
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, uniqueID=None, privacy_policy=None,
                 member_since=None, last_seen=None):
        self.uniqueID = uniqueID
        self.privacy_policy = privacy_policy
        self.member_since = member_since
        self.last_seen = last_seen
    
    def createIfNotExistsByUniqueID(self, uniqueID):
        if self.getByUniqueID(uniqueID) is None:
            self.uniqueID = uniqueID
            db.session.add(self)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return False
        return True
    
    def getByUniqueID(self, uniqueID):
        return User.query.filter_by(uniqueID=uniqueID).first()

    def getPrivacyPolicyByUniqueID(self, uniqueID):
        return self.getByUniqueID(uniqueID).privacy_policy
    
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
    
    def serialize(self):
        d = Serializer.serialize(self)
        del d['id']
        return d
    
    def __repr__(self):
        return '<User %r>' % (self.uniqueID)

