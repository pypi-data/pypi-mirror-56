# vim: set tabstop=4
# inflation.py
#!/usr/bin/env python3

"""Classes and functions related to inflation"""

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
from collections.abc import Iterable

from utils import (
nearestdate,
includesdate,
commondate,
)

class BasisError(KeyError):
    """ Raised when an operation attempts to access a basis that's not
    in the index table
    """
    def __init__(self, message, key):
        super().__init__(message, key)
        self.message = message
        self.key = key

class InflationIndex:
    """ Represents an inflation index of Laspeyres type

    Parameters
    ----------
    date : :py:class:`numpy.ndarray` or array_like of :py:class:`datetime.date`
        Dates of the index values
    index : :py:class:`numpy.ndarray` or array_like of :py:class:`float`
        Index values
    basis : :py:class:`datetime.date`
        Basis date for the index
    source : :py:class:`string`, optional
        String indicating the source of the data

    Returns
    -------
    index: callable

    Attributes
    ----------
    table : :py:class:`dict`
        A dictionary with `date` as keys and `index` as values
    basis : :py:class:`datetime.date`
        Basis date for the index
    source : :py:class:`string`
        String indicating the source of the data
    """

    def __init__(self, date, index, basis, source=None):
        self.basis = basis
        self.source = source
        self.table = {k:v for k,v in zip(date, index)}

    @property
    def dates(self):
        """ Return the keys of `self.table` as :py:class:`numpy.ndarray` """
        return np.array(list(self.table.keys()))
    @property
    def values(self):
        """ Return the values of `self.table` as :py:class:`numpy.ndarray` """
        return np.array(list(self.table.values()))

    def __call__(self, date, *, basis=None):
        """Return index at (nearest) date with given basis

        Parameters
        ----------
        date : :py:class:`numpy.ndarray`, array_like, or scalar of :py:class:`datetime.date`
            Date(s) to get the index for
        basis : :py:class:`datetime.date`, optional
            Basis date of the returned index. If not given `self.basis` is used.

        Returns
        -------
        :py:class:`numpy.ndarray` or scalar
            value of the index at `date` with basis `basis`

        Raises
        ------
        :py:clas:`BasisError`
            If `basis` is not within dates in `self.table`
        """
        # Make date always iterable
        isdatescalar = False
        if not isinstance(date, Iterable):
            date = [date]
            isdatescalar = True

        # build array with table entries nearest to given dates
        date = nearestdate(self.dates, date)

        # If no basis is given use the basis of the table, i.e. self.basis
        if basis is None:
            basis = self.basis
            return np.array([self.table[k] for k in date])
        else: # Otherwise check if basis is in table, if not fail.
            # Make basis always iterable
            isbasisscalar = False
            if not isinstance(basis, Iterable):
                basis = [basis]
                isbasisscalar = True

            if not np.all(includesdate(self.dates, basis)):
                func = lambda x: not includesdate(self.dates, x)
                erbasis = list(filter(func, basis))
                raise BasisError('Basis {} not in table range'.format(erbasis),\
                        erbasis)
            else:
                # closest basis in table
                basis = nearestdate(self.dates, basis)

        indexdate_oldbasis = np.array([self.table[k] for k in date])
        indexbasis_oldbasis = np.array([self.table[k] for k in basis])

        retval = change_basis(indexdate_oldbasis, indexbasis_oldbasis)

        if isdatescalar and isbasisscalar:
            retval = retval[0]

        return retval

def change_basis(idx_date, idx_basis):
    """ Changes the basis of an index

    Parameters
    ----------
    idx_date : scalar or :py:class:`numpy.ndarray`
        Index to convert to the new basis
    idx_basis : scalar or :py:class:`numpy.ndarray`
        Index of the new basis

    Returns
    -------
    scalar or :py:class:`numpy.ndarray`
        The modified index

    Notes
    -----

    To convert the index of date :math:`X` given in basis date :math:`B` to a
    new basis date :math:`C`, we do the following:

    .. math:: \\text{index}_C(X) = \\frac{\\text{index}_B(X)}{\\text{index}_B(C)}

    This is analogous to the change of basis of logarithms.

    The method absolutely correct for index of the `Laspeyres type <https://en.wikipedia.org/wiki/Price_index#Relative_ease_of_calculating_the_Laspeyres_index>`_.
    For indexes of the Paasche type, is it good only when :math:`X` (the date of
    the index you want to know) is close to :math:`C` (the basis date of the
    table you do not have).

    As an exmaple, let's say you have an index table with basis year
    :math:`B = 2004`, and need to know the index in :math:`X = 2010`
    with basis year :math:`C = 2005`, then:

    .. math:: \\text{index}_{2005}(2010) = \\frac{\\text{index}_{2004}(2010)}{\\text{index}_{2004}(2010)}

    """
    return idx_date / idx_basis

def merge_index(index, moreindex, *, basis=None):
    """ Merges two index tables by converting to a common basis

    The indexes have to share some part of their date ranges.
    If provided the basis has to be include din both indexes. If not provided
    the basis is selected as the oldest date that is common to both indexes.

    Parameters
    ----------
    index, moreindex : :py:class:`.InflationIndex`
        Indexes to merge
    basis : :py:class:`datetime.date`
        Basis of the merged index

    Returns
    -------
    :py:class:`.InflationIndex`
        The merged index
    """

    date1 = index.dates
    date2 = moreindex.dates
    date1in2, date2in1 = commondate(date1, date2)
    if basis is None:
        # Check for common dates
        if not np.any(date2in1):
            raise ValueError('Indexes have no common dates')
        # Find the oldest date that is common to both indexes
        basis = min(date1[date1in2].min(), date2[date2in1].min())
    else:
        if not (includesdate(index.dates, basis)\
                and includesdate(index.dates, basis)):
            raise BasisError('Basis is not in both indexes date range', basis)

    # Get indexes on common base
    val1 = index(date1, basis=basis)
    val2 = moreindex(date2, basis=basis)
    # Make new index by joining the previous
    date = np.concatenate((date1, date2))
    # If any date is in equal, then average
    for d1 in date1[date1in2]:
        for d2 in date2[date2in1]:
            if d1 == d2:
                i1 = np.nonzero(date1 == d1)[0]
                i2 = np.nonzero(date2 == d2)[0]
                avg = (val1[i1] + val2[i2]) / 2.0
                val1[i1] = avg
                val2[i2] = avg
    date, idx = np.unique(date, return_index=True)
    val = np.concatenate((val1, val2))[idx]

    return InflationIndex(date=date, index=val, basis=basis,\
        source=(index.source, moreindex.source))

def rebase_index(index, basis):
    """ Change the basis of an py:class`.InflationIndex` object

    Parameters
    ----------
    index : :py:class:`.InflationIndex`
        Index to alter
    basis : :py:class:`datetime.date`
        New basis for the index

    Returns
    -------
    :py:class`.InflationIndex`
        The index in the new basis
    """
    newval = index(index.dates, basis=basis)
    return InflationIndex(index.dates, newval, basis, source=index.source)

def inflate(value, *, ondate, todate, index):
    """ Update a value using inflation index

    The `value` is expressed on monetary units at time `ondate`
    and the return value is expressed on monetary units at time
    `todate`.

    Parameters
    ----------
    value : :py:class:`numpy.ndarray` or array_like
        Values to inflate
    ondate : array_like of :py:class:`datetime.date`
        Dates of the values to inflate
    todate : array_like of :py:class:`datetime.date`
        Dates of the inflated values
    index : :py:class:`.InflationIndex` or array_like
        Inflation index

    Returns
    -------
    :py:class:`numpy.ndarray`
        Inflated values

    Raises
    ------
    :py:class:`ValueError`
        When ``index`` is not of type :py:class:`.InflationIndex`
    """

    if isinstance(index, InflationIndex):
        index = index(todate, basis=ondate)
    elif isinstance(index, np.ndarray):
        pass
    else:
        raise ValueError('index must be of type InflationIndex')

    return value * index

if __name__ == '__main__':
    """ Show examples of inflation index functionality """
    import datetime as dt
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    # Load two indexes with different bases and date ranges
    data = np.genfromtxt('../data/baukosten_071939.csv', delimiter=',',\
        dtype=None, encoding='UTF-8')
    date  = [];
    value = [];
    for d,v in data:
        date.append(dt.datetime.strptime(d, '%d.%m.%Y').date())
        value.append(float(v) / 100.0)

    index39 = InflationIndex(basis=dt.date(day=1,month=7,year=1939),\
        source='baukosten_071929.csv', date=date, index=value)

    data = np.genfromtxt('../data/baukosten_102015.csv', delimiter=',',\
        dtype=None, encoding='UTF-8')
    date  = [];
    value = [];
    for d,v in data:
        date.append(dt.datetime.strptime(d, '%d.%m.%Y').date())
        value.append(float(v) / 100.0)

    index15 = InflationIndex(basis=dt.date(day=1,month=10,year=2015),\
        source='baukosten_102015.csv', date=date, index=value)

    newbasis = dt.date(day=1,month=10, year=2000)
    # Change of basis 1939 --> 2000
    idx39_00 = index39(index39.dates, basis=newbasis)
    # Change of basis 2015 --> 2000
    idx15_00 = index15(index15.dates, basis=newbasis)
    # merge both autoselect basis
    newidx = merge_index(index39, index15)
    # merge both select basis 2000
    newidx00 = merge_index(index39, index15, basis=newbasis)

    dates39 = mdates.date2num(index39.dates)
    dates15 = mdates.date2num(index15.dates)
    ndates  = mdates.date2num(newidx.dates)
    ndates00 = mdates.date2num(newidx00.dates)

    plt.plot_date(dates39, index39.values, 'o', label='b 1939')
    plt.plot_date(dates39, idx39_00, 'o', label='b 1939->2000')
    plt.plot_date(dates15, index15.values,'s', label='b 2015')
    plt.plot_date(dates15, idx15_00, 's', label='b 2015->2000')
    plt.plot_date(ndates, newidx.values,'-', label='auto merge')
    plt.plot_date(ndates00, newidx00.values,'-', label='merge b 2000')
    plt.legend()

    ax = plt.gca()
    ax.axhline(y=1.0)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%m'))
    ax.format_xdate = mdates.DateFormatter('%d.%m.%Y')
    plt.gcf().autofmt_xdate()
    plt.minorticks_on()
    plt.show()
