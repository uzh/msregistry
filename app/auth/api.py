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


import json
import urllib, urllib2

from flask import current_app


def get_tokeninfo(token):
    url = current_app.config['URL_TOKENINFO']
    
    values = {'id_token' : token }
    headers = { 'Accept' : 'application/json',
                'Authorization' : 'Bearer %s' % token }
    
    data = urllib.urlencode(values)
    request = urllib2.Request(url, data, headers)
    
    json_data = urllib2.urlopen(request).read()
    json_object = json.loads(json_data)
    
    if 'app_metadata' in json_object and 'roles' in json_object:
        roles = json_object['app_metadata']['roles']
    else:
        roles = []
    
    if 'app_metadata' in json_object and 'lang' in json_object:
        lang = json_object['app_metadata']['lang']
    else:
        lang = current_app.config['DEFAULT_LANG']
    
    return roles, lang

