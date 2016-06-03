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

from datetime import datetime

from app import create_app
from app.models import User

from app import utils

from time import sleep

class UserModelTestCase(unittest.TestCase):
    uniqueID = 'd4c74594d841139328695756648b6bd6'
    roles = ['patient']
    birthdate="25.12.1975"
    sex="male"
    signature="FP"
    physician_contact_permitted=True
    medical_record_abstraction=True
    data_exchange_cohort=True
    
    def setUp(self):
        self.app = create_app('TESTING')
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        self.app_context.pop()
    
    def test_createIfNotExistsByUniqueID(self):
        u = User()
        self.assertTrue(u.createIfNotExistsByUniqueID(self.uniqueID))
    
    def test_getByUniqueID(self):
        u = User()
        self.assertTrue(u.createIfNotExistsByUniqueID(self.uniqueID))
        u1 = u.getByUniqueID(self.uniqueID)
        self.assertEquals(u1.uniqueID, self.uniqueID)
    
    def test_setPatientConsentByUniqueID(self):
        u = User()
        u.createIfNotExistsByUniqueID(self.uniqueID)
        self.assertTrue(u.setPatientConsentByUniqueID(self.uniqueID, self.sex, utils.Time.DMYToDatetime(self.birthdate), self.signature,
                                                       self.physician_contact_permitted, self.medical_record_abstraction,
                                                       self.data_exchange_cohort))
    
    def test_setRelativeConsentByUniqueID(self):
        u = User()
        u.createIfNotExistsByUniqueID(self.uniqueID)
        self.assertTrue(u.setRelativeConsentByUniqueID(self.uniqueID, self.sex, utils.Time.DMYToDatetime(self.birthdate), self.signature))
        
    def test_getConsentByUniqueID(self):
        u = User()
        u.createIfNotExistsByUniqueID(self.uniqueID)
        self.assertTrue(u.setPatientConsentByUniqueID(self.uniqueID, self.sex, utils.Time.DMYToDatetime(self.birthdate), self.signature,
                                                      self.physician_contact_permitted, self.medical_record_abstraction,
                                                      self.data_exchange_cohort))
        self.assertNotEqual(u.getByUniqueID(self.uniqueID).date_signed, None)
    
    def test_timestamps(self):
        u = User()
        u.createIfNotExistsByUniqueID(self.uniqueID)
        u1 = u.getByUniqueID(self.uniqueID)
        sleep(2)
        self.assertTrue(
            (datetime.utcnow() - u1.member_since).total_seconds() > 2)
        self.assertTrue(
            (datetime.utcnow() - u1.last_seen).total_seconds() > 2)
    

