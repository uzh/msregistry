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

from sqlalchemy.exc import IntegrityError


class User(db.Model):
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
    
    def create_if_not_exists(self):
        if self.get() is None:
            db.session.add(self)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return False
        return True
    
    def get(self):
        return User.query.filter_by(uniqueID=self.uniqueID).first()
    
    def getLanguage(self):
        return db.session.query(User).filter_by(uniqueID=self.uniqueID).join(User.language).all()[0].language.code
    
    def setLanguage(self, language):
        return db.session.query(User).filter_by(uniqueID=self.uniqueID).update({'language': language})
    
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
    
    def to_json(self):
        json_user = {
            'uniqueID': self.uniqueID,
            'confirmed': self.confirmed,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'language': self.language_id
        }
        return json_user
    
    def __repr__(self):
        return '<User %r>' % (self.uniqueID)

