#!/usr/bin/python3.7
"""
Copyright (C) 2019 Reinventing Geospatial, Inc.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>,
or write to the Free Software Foundation, Inc., 59 Temple Place -
Suite 330, Boston, MA 02111-1307, USA.

Author: Jenifer Cochran, Reinventing Geospatial Inc (RGi)
Date: 2019-19-9
Credits:
Version:
"""
from enum import Enum


class EnumWithAttributes(Enum):
    """Creates an enum type that has attribute members."""

    def __new__(cls, *args, **kwds):  # pylint: disable=W0613
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value  # pylint: disable=W0212
        return obj
