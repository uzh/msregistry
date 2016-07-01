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


class Time():
    @staticmethod
    def DatetimeToDMY(date):
        if date is not None:
            # dates older than year==1000 will not work with strftime
            strdate = date.isoformat(' ').split()[0]
            y, m, d = strdate.split('-')
            return "%s.%s.%s" % (d,m,y)

    @staticmethod
    def DMYToDatetime(date):
        if date is not None:
            return datetime.strptime(date, "%d.%m.%Y")

    @staticmethod
    def Iso8601ToDatetime(date):
        if date is not None:
            return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
