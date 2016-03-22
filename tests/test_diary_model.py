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


import unittest

from app import create_app
from app.models import Diary, User

class DiaryModelTestCase(unittest.TestCase):
    uniqueID = 'd4c74594d841139328695756648b6bd6'
    
    def setUp(self):
        self.app = create_app('TESTING')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_addByUniqueID(self):
        u = Diary()
        self.assertTrue(u.addByUniqueID(self.uniqueID, {}))

    def test_getByUniqueID(self):
        a = User()
        self.assertTrue(a.createIfNotExistsByUniqueID(self.uniqueID))
        u = Diary()
        u1 = u.getByUniqueID(self.uniqueID)
        self.assertEqual(u1.user.uniqueID, self.uniqueID)

