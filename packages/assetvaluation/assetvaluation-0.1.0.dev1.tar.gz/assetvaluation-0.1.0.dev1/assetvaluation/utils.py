# vim: set tabstop=4
# utils.py
#!/usr/bin/env python3

"""Utility functions"""

# Copyright (C) 2019 Juan Pablo Carbajal
# Copyright (C) 2019 Reza Housseini
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# Author: Juan Pablo Carbajal <ajuanpi+dev@gmail.com>

import numpy as np
import datetime as dt

from collections.abc import Iterable

def mapifiter(func, x):
    """ Map function if input is iterable

        The output is the output of func or a numpy.array with func outputs for
        each x
    """
    if isinstance(x, Iterable):
        retval = np.array(list(map(func, x)))
    else:
        retval = func(x)
    return retval

def nearest2pivot(items, pivot):
    """ Find the element in items nearest to pivot

        :param items: array_like
        :param items: scalar
        :returns: tuple with the element from items
    """

    keyfun = lambda x: abs(x - pivot)
    #idxmin = np.argmin(list(map(keyfun, items)))
    return min(items, key=keyfun)

def nearestdate(dates, date):
    """ Find nearest date in dates

        :param dates: iterable of dates
        :param date: date(s) to search for
    """
    atom = lambda x: nearest2pivot(dates, x)
    return mapifiter(atom, date)

def hasdate(dates, date):
    """ Check if date is in dates

        :param dates: iterable of dates
        :param date: date(s) to search for
        :returns: boolean (numpy array) indicating if date is in the dates
    """
    atom = lambda x: x in dates
    return mapifiter(atom, date)

def includesdate(dates, date, *, precision=None):
    """ Check if dates range includes the given date

        :param dates: iterable of dates
        :param date: date(s) to search for
        :returns: boolean (numpy array) indicating if date is within dates
    """
    mindate = min(dates)
    maxdate = max(dates)
    atom = lambda x: (x >= mindate) and (x <= maxdate)
    return mapifiter(atom, date)

def commondate(dates1, dates2):
    """ Return the dates that are included in both date ranges.

        It is like an intersection between the two dates iterables.

        :param dates1: iterable of dates
        :param datea2: iterable of dates
        :returns: tuple of boolean (numpy array) indicating if dates in one
             iterable are is within the dates of the other iterable.
    """
    if not isinstance(dates1, np.ndarray):
        dates1 = np.array(dates1)
    if not isinstance(dates2, np.ndarray):
        dates2 = np.array(dates2)

    in2 = includesdate(dates2, dates1)
    in1 = includesdate(dates1, dates2)
    return in2, in1

def normalize(x, X = None):
    """ Divide each value in x by X

    :param x: an iterable or scalar with the values to convert
    :param X: the normalizing value. If not given then the sum of x is used.
    :return: numpy array with the normalized values
    """
    if not X:
        X = np.sum (x)

    return np.array(x) / X
