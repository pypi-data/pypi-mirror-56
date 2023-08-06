# vim: set tabstop=4
# valuation.py
#!/usr/bin/env python3

"""Classes and function to build valuation models"""

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

from inflation import (
BasisError,
InflationIndex,
inflate
)

#######################
## Model composite
#######################
def valuation_and_depreciation_varlifespan(*, value, date_of_value, lifespan,
         lifespan_start, calculation_date, index, interest, trim=False):
    """ Valuation and depreciation composite model

    Computes replacement value and depreciation using a constant
    depreciation model.
    The function accepts `lifespan_start` as the reference of the lifespan,
    which allows the computation even if the asset is renewed during its lifespan.

    The function computes the present(replacement) value, depreciation rate,
    book value, annuity, remainig life, age of asset.

    Parameters
    ----------
    value :
        Value of asset
    date_of_value :
        Date of value of asset
    lifespan :
        Lifespan of asset
    lifespan_start :
        Date when lifespan started
    calculation_date :
        date of the output calculation
    index :
        cost index. value (date_of_value --> calculation_date)
    interest :
        annual interest rate
    trim : optional
        Default False

    Returns
    -------
    :py:class:`dict`
        Calculation results. Keys are replacement_value, loss_value, book_value,
        annual_depo, rem_life, value_age


    Raises
    ------
    :py:class:`ValueError`
        If either `value` or `date_of_value` are None

    """

    # Use only values that are not None
    baddata = (value == np.array(None)) & (date_of_value == np.array(None))
    if np.any(baddata):
        raise ValueError('not valid value data')

    # replacement value
    rep_value = value * index
    # year of life end
    yeareol = np.array([lifespan + l.year for l in lifespan_start])
    # remaining life at date of value
    rem_life_value = np.array([yeol - d.year
                            for yeol, d in zip(yeareol, date_of_value)])
    rateloss_value = value / rem_life_value
    # Age of Value
    age = np.array([calculation_date.year - d.year for d in date_of_value])
    book_value = value - rateloss_value * age
    #book_value, loss_value = depreciation_constant(value, lifspan, age)
    annual_depo = value * interest / 2
    # Remianing life of asset
    rem_life =  yeareol - calculation_date.year

    if trim:
        # if age is more than lifespan return 0
        isoverused = rem_life <= 0
        rateloss_value[isoverused] = 0.0
        book_value[isoverused] = 0.0
        annual_depo[isoverused] = 0.0
        rem_life[isoverused] = 0

    return dict(replacement_value=rep_value,
              loss_value=rateloss_value,
              book_value=book_value,
              annual_depo=annual_depo,
              rem_life=rem_life,
              value_age=age)

def valuation_and_depreciation(*, value, date_of_value, lifespan,
         calculation_date, index, interest, trim=False):
    """ Valuation and depreciation composite model

    Computes replacement value and depreciation using a constant
    depreciation model.

    The function computes the present(replacement) value, depreciation rate,
    book value, annuity, remainig life, age of asset.

    Parameters
    ----------
    value :
        Value of asset
    date_of_value :
        Date of value of asset
    lifespan :
        Lifespan of asset
    calculation_date :
        date of the output calculation
    index :
        cost index. value (date_of_value --> calculation_date)
    interest :
        annual interest rate
    trim : optional
        Default False

    Returns
    -------
    :py:class:`dict`
        Calculation results. Keys are replacement_value, loss_value, book_value,
        annual_depo, rem_life, value_age

    Raises
    ------
    :py:class:`ValueError`
        If either `value` or `date_of_value` are None
    """

    # Use only values that are not None
    baddata = (value == np.array(None)) & (date_of_value == np.array(None))
    if np.any(baddata):
        raise ValueError('not valid value data')

    # replacement value
    rep_value = value * index
    # Annula deposit
    annual_depo = value * interest / 2

    # year of life end
    yeareol = np.array([lifespan + d.year for d in date_of_value])
    # Remianing life of asset and value
    rem_life =  yeareol - calculation_date.year
    # Age of Value
    age = np.array([calculation_date.year - d.year for d in date_of_value])
    # Book value and depreciation rate
    book_value, rateloss_value = depreciation_constant(value, lifespan, age)

    if trim:
        # if age is more than lifespan return 0
        isoverused = rem_life <= 0
        rateloss_value[isoverused] = 0.0
        book_value[isoverused] = 0.0
        annual_depo[isoverused] = 0.0
        rem_life[isoverused] = 0

    return dict(replacement_value=rep_value,
              loss_value=rateloss_value,
              book_value=book_value,
              annual_depo=annual_depo,
              rem_life=rem_life,
              value_age=age)

#######################
## Model atomic
#######################

def annuity_factor(p, J):
    """ Annuity formula factor for constant interest rate.

    The annuity formula factor is used to compute the annuity (a series of
    payments made at equal intervals), by multiplying the factor with the
    present value of an asset.

    Parameters
    ----------
    p : :py:class:`numpy.ndarray` or scalar
        Interest rate
    J : :py:class:`numpy.ndarray` or scalar
        Total of years

    Returns
    -------
    :py:class:`numpy.ndarray` (ndims >= 2) or scalar
        Annuity factor

    Notes
    -----
    This formula is modified to consider that the first payment happens after a
    year.

    .. math::
        \\text{Payment} &= \\text{Future Value} \\times \\text{Factor}\\\\
        \\text{Factor} &= \\frac{p}{(p+1) \\left[(p+1)^J - 1\\right]}

    This formula is derived from the partial sum of the geometric series.
    The constraint is that the sum of all the payments over the :math:`J` years must
    equal the value fo the asset at that time (future value):

    .. math::
        V(J) = \\sum_{n=1}^{J} P_n

    where :math:`V(J)` is the value of the asset after :math:`J` years (future value), and
    :math:`P_n` is the payment made on year :math:`n`.

    Assuming that the interest rate is contant over all the :math:`J` years,
    the payment is given by the depreciation :math:`A` indexed with the interest:

    .. math:: P_n = A q^n

    where :math:`q` is the interest factor :math:`q = p + 1`, and :math:`p` the
    interest rate.
    Further assuming constant depreciation we get,

    .. math::
        V(J) =& \\sum_{n=1}^{J} A q^n = A q \sum_{n=0}^{J-1} q^n = A \\frac{q \\left(q^J - 1\\right)}{q - 1} = \\\\
        &= A \\frac{(p+1) \\left[(p+1)^J - 1\\right]}{p}

    """
    q = p + 1
    af = p / (q * (np.power(q, J) - 1))
    return af

def annuity(T, p, J):
    """ Annuity (a sum of money to be paid in regular intervals) for constant
    insterest rate.

    The annuity is calculated using the output of :py:func:`.annuity_factor`.
    See help of that function for details of the calculation.

    Parameters
    ----------
    p : :py:class:`numpy.ndarray` or scalar
        Interest rate
    J : :py:class:`numpy.ndarray` or scalar
        Total of years
    :param T: total amount to be indexed (scalar or array)

    Returns
    -------
    :py:class:`numpy.ndarray` (ndims >= 2) or scalar
        Annuity
    """
    return T * annuity_factor (p, J)

def replacement_value(historicalvalue, index):
    """ Replacement value (present value) using the cost index method.
    """
    return historicalvalue * index

def depreciation_constant(value, lifespan, age, *, scrap_value=0):
    """  Constant depreciation of asset during its lifespan.

    Also know as the straight-line model for depreciation, i.e. the asset
    looses value at constant rate during its life.

    Parameters
    ----------
    value : :py:class:`numpy.ndarray` or scalar
        historic value of asset
    lifespan : :py:class:`numpy.ndarray` or scalar
        useful lifespan of asset
    age : :py:class:`numpy.ndarray` or scalar
        Age of asset
    scrap_value : :py:class:`numpy.ndarray` or scalar, optional
        Scrap value of the asset. Default 0

    Returns
    -------
    :py:class:`tuple` of :py:class:`numpy.ndarray` or scalar
        Book value and depreciation rate
    """
    depreciation_rate = (value - scrap_value) / lifespan
    bookvalue = value - depreciation_rate * age # same as depreciation * remlife
    return bookvalue, depreciation_rate

def value_from_expenditure(expenditure, date, *, update_func=None,
        initial_value=0.0):
    """ Obtain cumulative present value from series of expenditures.

        Expenditures are updated using `update_func` then accumulated.
        The default update function is the identity (do nothing).

        Parameters
        ----------
        expenditure : :py:class:`numpy.ndarray` or array_like
        date : :py:class:`numpy.ndarray`, array_like, or scalar of :py:class:`datetime.date`
        calculation_date : :py:class:`datetime.date`
            Date of calculation
        update_func : callable, optional
            The signature is `update_func(value, ondate, todate)`
        initial_value : float, optional
            Default 0.0

        Returns
        -------
        :py:class:`numpy.ndarray`

    """
    if update_func is None:
        update_func = lambda v, ondate, todate: v

    # update loop
    value = np.zeros_like(expenditure)
    value[0] = initial_value + expenditure[0]
    for i, e in enumerate(expenditure[1:], start=1):
        value[i] = update_func(value[i-1], date[i-1], date[i]) + e

    return value

def value_from_dimension(quantity, specific_value):
    """ Obtain present value by multiplying with specific value """
    return quantity * specific_value

###########################
### Helpers
###########################
def depreciation_basis(t, tN, dN):
     """ Basis with finite support [tN, tN+dN] for depreciation models """
     tN_inf = np.concatenate((tN, [np.inf]))
     tmin = np.minimum(tN + dN, tN_inf[1:])
     t = np.atleast_2d(t).T
     phi = (1 - (t - tN) / dN)
     # Reseting expeditures
     H_rst = np.heaviside(tmin - t, 0) * np.heaviside(t - tN, 1)
     # Additive expeditures
     #H_norst = np.heaviside(tN + dN - t, 0) * np.heaviside(t - tN, 1)
     return H_rst * phi

def value_curve(t, dates, values, types, lifespans):
    #FIXME filter value types
    v = values
    B = depreciation_basis(t, dates, lifespans)
    return B.dot(v)

if __name__ == "__main__":
    import datetime as dt
    import matplotlib.pyplot as plt

    date = dt.date(year=2012, month=1, day=1)
    investment = np.array([100, 50, 50, 20, 50, 10, 0])
    todatetime = lambda y: dt.date(year=y, month=6, day=15)
    dateofinvest = 2000 + np.array([0, 1, 3, 5, 8, 9])
    dateofinvest = np.array(list(map(todatetime,dateofinvest))+[date])
    lifespan = 25

    indexes = np.array([1.2, 1.15, 1.1, 1.0, 0.9, 1.2, 1.0])
    index = InflationIndex(index=indexes, date=dateofinvest, basis=date)

    # Uniform indexing
    # Index all values, then depreciate each one to the date of calculation
    investment_ = inflate(investment, ondate=dateofinvest, todate=date,\
        index=index)
    update_func = \
        lambda v,d1,d2: depreciation_constant(v, lifespan, (d2-d1).days/365)[0]
    val_unif = value_from_expenditure(investment_, dateofinvest,\
        calculation_date=date.year, update_func=update_func)

    # Index then depreciate
    update_func = lambda v,d1,d2:\
         depreciation_constant(inflate(v,ondate=d1,todate=d2,index=index),\
             lifespan, (d2-d1).days/365)[0]
    val_inddep = value_from_expenditure(investment_, dateofinvest,\
        calculation_date=date.year, update_func=update_func)
    val_inddep = inflate(val_inddep, ondate=dateofinvest, todate=date,\
        index=index)

    # Depreciate then index
    update_func = lambda v,d1,d2:\
         inflate(depreciation_constant(v, lifespan, (d2-d1).days/365)[0],\
            ondate=d1, todate=d2, index=index)
    val_depind = value_from_expenditure(investment_, dateofinvest,\
        calculation_date=date.year, update_func=update_func)
    val_depind = inflate(val_depind, ondate=dateofinvest, todate=date,\
        index=index)

    plt.stem(dateofinvest, investment, label='investments [local time value]')
    lbl = 'investments [value@{}]'.format(str(date))
    plt.stem(dateofinvest, investment_, markerfmt='ro', label=lbl)
    plt.plot(dateofinvest, val_unif, '-ro', label='uniform')
    plt.plot(dateofinvest, val_inddep, '-o', label='dep(ind)')
    plt.plot(dateofinvest, val_depind, '-o', label='ind(dep)', fillstyle='none')
    plt.legend()
    plt.show()

### Doc tests
###########################
#if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
