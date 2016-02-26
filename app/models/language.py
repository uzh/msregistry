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


from app import db

from serializer import Serializer

class Language(db.Model, Serializer):
    __tablename__ = 'language'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(2))
    name = db.Column(db.String(16))
    user = db.relationship("User", uselist=False, back_populates="language")

    def __init__(self, code=None, name=None):
        self.code = code
        self.name = name
    
    def getById(self, id):
        return Language.query.get(id)
    
    def getAll(self):
        return Language.query.all()
    
    def getCodeById(self, id):
        return self.getById(id).code

    def getNameById(self, id):
        return self.getById(id).name

    def serialize(self):
        d = Serializer.serialize(self)
        del d['id']
        del d['user']
        return d
    
    def __repr__(self):
        return '<Language %r>' % (self.name)

