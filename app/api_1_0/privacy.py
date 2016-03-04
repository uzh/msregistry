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


from flask import current_app, jsonify, redirect, url_for

from flask.ext.babel import gettext

from . import api


@api.route('/privacy')
def get_privacy_policy():
    return redirect(url_for('api.get_multilanguage_privacy_policy', 
                            lang_code=current_app.config['BABEL_DEFAULT_LOCALE']))


@api.route('/<lang_code>/privacy')
def get_multilanguage_privacy_policy():
    return jsonify(text=unicode(gettext(u'Privacy policy')))

