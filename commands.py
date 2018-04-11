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


import os
from flask import abort, request

from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'DEFAULT')

@app.cli.command()
def get_all_users():
    """ Get all users """
    from app.models import User, Survey
    user = User()
    survey = Survey()
    all_users = user.getAll()
    all_surveys = survey.getAll()
    print("Found {0} users".format(len(all_users)))
    print("Found {0} surveys".format(len(all_surveys)))

@app.cli.command()
def reports():
    """Generate reports."""
    from app import mail
    from flask_mail import Message
    
    from app.models import User, Survey
    
    user = User()
    survey = Survey()
    
    msg = Message("MS-Registry Reports", recipients=app.config['MAIL_RECIPIENTS'])
    
    user_report_filename = user.getCSVReportInformedConsent()
    with app.open_resource(os.path.join(app.config['REPORTS_DIR'] , user_report_filename)) as fp:
        msg.attach(user_report_filename, "text/csv", fp.read())
    
    survey_report_filename = survey.getCSVReportTagsAndOngoing()
    with app.open_resource(os.path.join(app.config['REPORTS_DIR'] , survey_report_filename)) as fp:
        msg.attach(survey_report_filename, "text/csv", fp.read())
    
    mail.send(msg)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    rc = unittest.TextTestRunner(verbosity=2).run(tests)
    return (1 if rc.errors or rc.failures else 0)

