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

from language import Language
from serializer import Serializer

from sqlalchemy.exc import IntegrityError


class User(db.Model, Serializer):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    uniqueID = db.Column(db.String(64), nullable=False, unique=True, index=True)
    confirmed = db.Column(db.Boolean, default=False)
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'), default=2)
    language = db.relationship("Language", back_populates="user")
    
    def __init__(self, uniqueID=None, confirmed=None, member_since=None, 
                 last_seen=None, language_id=None):
        self.uniqueID = uniqueID
        self.confirmed = confirmed
        self.member_since = member_since
        self.last_seen = last_seen
        self.language_id = language_id
    
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
    
    def getLanguageByUniqueID(self, uniqueID):
        return db.session.query(User).filter_by(uniqueID=uniqueID).join(User.language).all()[0].language.code
    
    def setLanguageByUniqueID(self, uniqueID, language):
        return db.session.query(User).filter_by(uniqueID=uniqueID).update({'language': language})
    
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
    
    def serialize(self):
        d = Serializer.serialize(self)
        del d['id']
        del d['language_id']
        del d['language']
        return d
    
    def __repr__(self):
        return '<User %r>' % (self.uniqueID)

