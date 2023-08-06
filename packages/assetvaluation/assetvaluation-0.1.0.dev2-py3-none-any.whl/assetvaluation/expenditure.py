# vim: set tabstop=4
# expenditure.py
#!/usr/bin/env python3

""" Classes and functions for expenditures """

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

from enum import Enum

class ExpenditureType(Enum):
     BUILD = 1                  # asset is rebuilt
     START_BUILD = 10           # build starts
     END_BUILD = 11             # build ends
     REVIVE = 2                 # asset's life span is changed (value changes)
     START_REVIVE = 20          # start
     END_REVIVE = 21            # end
     UPDATE = 3                 # asset's life span is kept (value changes)
     START_UPDATE = 30          # start
     END_UPDATE = 31            # end
     DECOMISSION = 4            # asset is decommissioned
     IGNORED = 5                # expenditure is ignored

def range_expenditurestype(types, ref):
    """ Find the segments of sequential ``START_`` ``END_`` expenditures

    Computes the indexes marking the segment between a ``START_ref`` and an
    ``END_ref``. Since these segments are continuous they are returned
    as ranges.

    Parameters
    ----------
    types : :py:class:'numpy.ndarray'
        Array with expenditure types py:class:`.ExpenditureType`
    ref : :py:class:`.ExpenditureType`
        The expenditure type for which index ranges are computed

    Returns
    -------
    :py:class:`list`
        List of :py:class:`range` for each segment found

    Raises
    ------
    :py:class:`ValueError`
        When the argument ``types`` is malformed

    See also
    --------
    :py:func:`.collapse_expenditure`
    :py:class:`.ExpenditureType`

    Examples
    --------
    >>> etyp = np.array([
    ...         ExpenditureType.START_BUILD,
    ...         ExpenditureType.BUILD,
    ...         ExpenditureType.END_BUILD,
    ...         ExpenditureType.START_UPDATE,
    ...         ExpenditureType.UPDATE,
    ...         ExpenditureType.UPDATE,
    ...         ExpenditureType.END_UPDATE,
    ...         ExpenditureType.IGNORED,
    ...         ExpenditureType.UPDATE,
    ...         ExpenditureType.START_UPDATE,
    ...         ExpenditureType.UPDATE,
    ...         ExpenditureType.END_UPDATE,
    ...         ])
    >>> print(range_expenditurestype(etyp, ExpenditureType.BUILD))
    [range(0, 3)]
    >>> print(range_expenditurestype(etyp, ExpenditureType.UPDATE))
    [range(3, 7), range(9, 12)]
    """

    start = np.nonzero(types == ExpenditureType['START_'+ref.name])[0]
    end = np.nonzero(types == ExpenditureType['END_'+ref.name])[0] + 1

    # Assume that either the lengths are equal or that
    # start is longer than end, and start[-1] > end[-1]
    if len(start) == len(end)+1:
        end = np.concatenate((end,[len(types)]))
    elif len(start) < len(end):
        raise ValueError(
                'Ranges have too many END_{}'.format(ref.name)
        )
    elif len(start) > len(end):
        raise ValueError(
                'Ranges have too many START_{}'.format(ref.name)
        )

    # Check for consecutive starts and ends
    for i in range(len(start)):
        if np.any(end[i] >= start[i+1:]):
            raise ValueError(
                'Consecutive START_{} found'.format(ref.name)
            )
        if i < len(start)-1:
            if np.any(end[i+1:] <= start[i+1]):
                raise ValueError(
                    'Consecutive END_{} found'.format(ref.name)
                )

    return [range(s,e) for s,e in zip(start,end)]

def collapse_expenditure(date, expend, expendtype, *, valuefunc=None):
    """ Collapse segments with ``START_`` and ``END_`` expenditure types.

    The elements in the first array (`date`) within a segment starting
    with ``START_`` and finishing with ``END_`` are removed and only one entry
    is returned for each segment.
    The value of that entry is the last element of the arrray.

    The elements in the second array (`expend`) within each segment are
    added.

    The elements in the expenditure type array (`expendtype`) are collapsed
    and the type without decoration is returned.

    Parameters
    ----------
    date : :py:class:`numpy.ndarray`
        Array with the dates of the expenditures.
    expend : :py:class:`numpy.ndarray`
        Array with the values of the expenditures.
    expendtype : :py:class:`numpy.ndarray`
        Array with the type of the expneditures
    valuefunc : function, optional
        Function to override the default behavior when collpasing
        expenditure values. The function should take three input arguments:
        the first two are array correspoding to dates, and values in a given
        segment; the last argument is an expenditure type indicating the
        type of segment being treated. The function should return a value
        Default is :py:func:`numpy.sum` applied to the values.

    Returns
    -------
    date_of_value : :py:class:`numpy.ndarray`
        Array with the filtered dates.
    expend : :py:class:`numpy.ndarray`
        Array with filtered values.
    expendtype : :py:class:`numpy.ndarray`
        Array filtered types. It does not contain ``START_`` and ``END_`` types.

    See also
    --------
    :py:func:`.range_expenditure` :
    :py:class:`.ExpenditureType` :

    Examples
    --------
    >>> etyp = np.array([
    ...         ExpenditureType.START_BUILD,
    ...         ExpenditureType.BUILD,
    ...         ExpenditureType.END_BUILD,
    ...         ExpenditureType.START_UPDATE,
    ...         ExpenditureType.UPDATE,
    ...         ExpenditureType.UPDATE,
    ...         ExpenditureType.END_UPDATE,
    ...         ExpenditureType.IGNORED,
    ...         ExpenditureType.UPDATE,
    ...         ExpenditureType.START_UPDATE,
    ...         ExpenditureType.UPDATE,
    ...         ExpenditureType.END_UPDATE,
    ...         ])
    >>> edate = np.arange(len(etyp)) + 2000   # investment year
    >>> eval = np.arange(len(etyp)) * 5 + 10  # investment value
    >>> date, value, typ = collapse_expenditure(edate, eval, etyp)
    >>> for y, v, t in zip(edate, eval, etyp):
    ...    print('{:5} {:3} {}'.format(y,v,t.name))
     2000  10 START_BUILD
     2001  15 BUILD
     2002  20 END_BUILD
     2003  25 START_UPDATE
     2004  30 UPDATE
     2005  35 UPDATE
     2006  40 END_UPDATE
     2007  45 IGNORED
     2008  50 UPDATE
     2009  55 START_UPDATE
     2010  60 UPDATE
     2011  65 END_UPDATE
    >>> for y, v, t in zip(date, value, typ):
    ...    print('{:5} {:3} {}'.format(y,v,t.name))
     2002  45 BUILD
     2006 130 UPDATE
     2008  50 UPDATE
     2011 180 UPDATE
    """
    # Function for collapsing values
    if valuefunc is None:
            valuefunc = lambda date,val,typ: np.sum(val)

    # Collapse block expenditure types
    value = expend.copy()
    date_of_value = date.copy()
    valtype = expendtype.copy()
    to_remove = []
    e_compressible = (ExpenditureType.BUILD,\
                      ExpenditureType.REVIVE,\
                      ExpenditureType.UPDATE)

    for e in e_compressible:
        ranges = range_expenditurestype(expendtype, e)
        for idx in ranges:
            date_of_value[idx[-1]] = date[idx[-1]]
            valtype[idx[-1]] = e
            value[idx[-1]] = valuefunc(date[idx], expend[idx], e)
            to_remove += idx[:-1]

    # Mark for removal ignored expenditures
    for i,e in enumerate(expendtype):
        if e == ExpenditureType.IGNORED:
            to_remove.append(i)

    # Remove expenditures
    value = np.delete(value, to_remove)
    valtype = np.delete(valtype, to_remove)
    date_of_value = np.delete(date_of_value, to_remove)

    return date_of_value, value, valtype

def filter_expenditure(date, expend, expendtype, *, valuefunc=None):
    """ Filter out ignored expenditure types

    Wrapper around :py:func:`.collapse_expenditure`
    See the documentation of that function for details.

    See also
    --------
    :py:func:`.collapse_expenditure`
    :py:class:`.ExpenditureType`

    Examples
    --------
    >>> etyp = np.array([
    ...         ExpenditureType.START_BUILD,
    ...         ExpenditureType.BUILD,
    ...         ExpenditureType.END_BUILD,
    ...         ExpenditureType.START_UPDATE,
    ...         ExpenditureType.UPDATE,
    ...         ExpenditureType.UPDATE,
    ...         ExpenditureType.END_UPDATE,
    ...         ExpenditureType.IGNORED,
    ...         ExpenditureType.UPDATE,
    ...         ExpenditureType.BUILD,
    ...         ExpenditureType.START_UPDATE,
    ...         ExpenditureType.UPDATE,
    ...         ExpenditureType.END_UPDATE,
    ...         ])
    >>> edate = np.arange(len(etyp)) + 2000   # investment year
    >>> eval = np.arange(len(etyp)) * 5 + 10  # investment value
    >>> date, value, typ = filter_expenditure(edate, eval, etyp)
    >>> for y, v, t in zip(edate, eval, etyp):
    ...    print('{:5} {:3} {}'.format(y,v,t.name))
     2000  10 START_BUILD
     2001  15 BUILD
     2002  20 END_BUILD
     2003  25 START_UPDATE
     2004  30 UPDATE
     2005  35 UPDATE
     2006  40 END_UPDATE
     2007  45 IGNORED
     2008  50 UPDATE
     2009  55 BUILD
     2010  60 START_UPDATE
     2011  65 UPDATE
     2012  70 END_UPDATE
    >>> for y, v, t in zip(date, value, typ):
    ...    print('{:5} {:3} {}'.format(y,v,t.name))
     2009  55 BUILD
     2012  195 UPDATE
    """

    empty = np.array([])
    # If decomosioned then return empty
    if ExpenditureType.DECOMISSION in expendtype:
        return empty, empty, empty

    date_of_value, value, valtype = collapse_expenditure(date, expend,
    expendtype, valuefunc=valuefunc)

    # Get index of last BUILD value
    # Only values from there on are considered
    idxbuild = np.nonzero(valtype == ExpenditureType.BUILD)[0]
    if idxbuild.size == 0:
        return empty, empty, empty

    idxbuild = idxbuild[-1]
    date_of_value = date_of_value[idxbuild:]
    value = value[idxbuild:]
    valtype = valtype[idxbuild:]
    return date_of_value, value, valtype

if __name__ == '__main__':

     # Create expenditure sequence
     inves_type = [
          ExpenditureType.BUILD,   # initial investment
          ExpenditureType.START_UPDATE,   # start of update (lifespan remains)
          ExpenditureType.UPDATE,         # continue update
          ExpenditureType.END_UPDATE,     # end of update
     ]
     inves_val = [
          100,
          50,
          10,
          60,
     ]
     inves_year = [
          2000,
          2005,
          2006,
          2007,
     ]
     inves_type = np.array(inves_type)
     inves_year = np.array(inves_year)
     inves_val = np.array(inves_val)
     year, value, vtype = collapse_expenditure(inves_year, inves_val, inves_type)

     print('Input')
     for y, v, t in zip(inves_year, inves_val, inves_type):
         print('{}  {}  {}'.format(y,v,t.name))

     print('\nOutput')
     for y, v, t in zip(year, value, vtype):
         print('{}  {}  {}'.format(y,v,t.name))
