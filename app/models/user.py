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

from sqlalchemy.exc import IntegrityError

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    uniqueID = db.Column(db.String(64), nullable=False, unique=True, index=True)
    confirmed = db.Column(db.Boolean, default=False)
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))
    language = db.relationship("Language", back_populates="user")
    
    def create_if_not_exists(self, uniqueID):
        if self.get() is None:
            self.uniqueID = uniqueID
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
        return self.get().language_id
    
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
            'last_seen': self.last_seen
        }
        return json_user
    
    def __repr__(self):
        return '<User %r>' % self.uniqueID

