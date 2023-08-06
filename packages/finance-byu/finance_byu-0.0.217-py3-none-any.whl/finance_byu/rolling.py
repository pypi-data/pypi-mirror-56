import numpy as np
from numba import njit,jit,prange
import pandas as pd

@njit(parallel=False)
def _check_minp(win,minp,N):
    if minp > win:
        raise ValueError('minp must be <= win')
    elif minp > N:
        minp = N + 1
    elif minp == 0:
        minp = 1
    elif minp < 0:
        raise ValueError('minp must be >= 0')
    return minp

def roll_sum(input,win,minp):
    """
    Computes the rolling sum of each column in a :code:`pandas` DataFrame.

    Parameters
    ----------
    input: pandas.core.frame.DataFrame
        This dataframe must have strictly numeric types.
    win: int
        Length of the moving window
    minp: int
        Minimum number of observations in window required to have a value 
        (otherwise result is NaN).

    Returns
    -------
    output: pandas.core.frame.DataFrame
        A :code:`pandas` DataFrame with the rolling sum of :code:`input`.
    """
    _assertions(input,win,minp)
    return pd.DataFrame(_roll_sum(input.values,win,minp),input.index)

@njit(parallel=False)
def _roll_sum(input,win,minp):
    """
    Computes the rolling sum of a :code:`numpy` array.

    Parameters
    ----------
    input: np.array of type double
    win: int
        Length of the moving window
    minp: int
        Minimum number of observations in window required to have a value 
        (otherwise result is NaN).

    Returns
    -------
    output: np.array of type double
    """

    val = float(0) 
    prev = float(0)
    sum_x = float(0)
    nobs = int(0)
    N = int(len(input))

    minp = _check_minp(win, minp, N)   
    output = np.empty(N,dtype=np.float64)

    for i in range(minp - 1):
        val = input[i]

        if val == val:
            nobs += 1
            sum_x += val

        output[i] = np.nan
        

    for i in range(minp - 1,N):        
        val = input[i]

        if val == val:        
            nobs += 1
            sum_x += val

        if i > win - 1:
            prev = input[i - win]
            
            if prev == prev:
                sum_x -= prev                
                nobs -= 1

        if nobs >= minp:
            output[i] = sum_x
        else:
            output[i] = np.nan            

    return output            

def roll_mean(input,win,minp):
    """
    Computes the rolling mean of each column in a :code:`pandas` DataFrame.

    Parameters
    ----------
    input: pandas.core.frame.DataFrame
        This dataframe must have strictly numeric types.
    win: int
        Length of the moving window
    minp: int
        Minimum number of observations in window required to have a value 
        (otherwise result is NaN).

    Returns
    -------
    output: pandas.core.frame.DataFrame
        A :code:`pandas` DataFrame with the rolling mean of :code:`input`.
    """
    _assertions(input,win,minp)
    return pd.DataFrame(_roll_mean(input.values,win,minp),input.index)


@njit(parallel=False)
def _roll_mean(input,win,minp):
    """
    Computes the rolling mean of a numpy array.

    Parameters
    ----------
    input: np.array of type double
    win: int 
        Length of the moving window
    minp: int
        Minimum number of observations in window required to have a value 
        (otherwise result is NaN).

    Returns
    -------
    output: np.array of type double
    """

    val = float(0)
    prev = float(0)
    sum_x = float(0)
    nobs = int(0)
    N = int(len(input))

    minp = _check_minp(win, minp, N)   
    output = np.empty(N,dtype=np.float64)

    for i in range(minp - 1):
        val = input[i]

        if val == val:
            nobs += 1
            sum_x += val

        output[i] = np.nan
        
    for i in range(minp - 1,N):        
        val = input[i]

        if val == val:        
            nobs += 1
            sum_x += val

        if i > win - 1:
            prev = input[i - win]
            
            if prev == prev:
                sum_x -= prev                
                nobs -= 1

        if nobs >= minp:
            output[i] = sum_x/nobs
        else:
            output[i] = np.nan            

    return output            


def roll_var(input,win,minp,ddof=1):
    """
    Computes the rolling variance of each column in a :code:`pandas` DataFrame.

    Parameters
    ----------
    input: pandas.core.frame.DataFrame
        This dataframe must have strictly numeric types.
    win: int
        Length of the moving window
    minp: int
        Minimum number of observations in window required to have a value 
        (otherwise result is NaN).
    ddof: int
        Delta degrees of freedom. The divisor used in calculations is N - ddof, 
        where N represents the number of elements.

    Returns
    -------
    output: pandas.core.frame.DataFrame
        A :code:`pandas` DataFrame with the rolling variance of :code:`input`.
    """
    _assertions(input,win,minp,ddof=ddof)
    return pd.DataFrame(_roll_var(input.values,win,minp,ddof=ddof),input.index)


@njit(parallel=False)
def _roll_var(input,win,minp,ddof=1):
    """
    Computes the rolling variance of a numpy array.

    Parameters
    ----------
    input: np.array of type double
    win: int 
        Length of the moving window
    minp: int
        Minimum number of observations in window required to have a value 
        (otherwise result is NA).
    ddof: int
        Delta degrees of freedom. The divisor used in calculations is N - ddof, 
        where N represents the number of elements.

    Returns
    -------
    output: np.array of type double
    """

    val = float(0)
    prev = float(0)
    sum_x = float(0)
    sum_xx = float(0)
    nobs = int(0)
    N = int(len(input))

    minp = _check_minp(win, minp, N)        
    output = np.empty(N,dtype=np.float64)

    for i in range(minp - 1):
        val = input[i]

        if val == val:
            nobs += 1
            sum_x += val
            sum_xx += val**2

        output[i] = np.nan


    for i in range(minp - 1,N):        
        val = input[i]

        if val == val:
            nobs += 1
            sum_x += val
            sum_xx += val**2

        if i > win - 1:
            prev = input[i - win]
            
            if prev == prev:
                sum_x -= prev
                sum_xx -= prev**2
                nobs -= 1

        if nobs >= minp:
            # pathological case
            if nobs == 1:
                output[i] = 0
                continue

            val = (nobs * sum_xx - sum_x**2) / (nobs * (nobs - ddof))
            if val < 0:
                val = 0

            output[i] = val
        else:
            output[i] = np.nan

    return output

def roll_std(input,win,minp,ddof=1):
    """
    Computes the rolling standard deviation of each column in a :code:`pandas` DataFrame.

    Parameters
    ----------
    input: pandas.core.frame.DataFrame
        This dataframe must have strictly numeric types.
    win: int
        Length of the moving window
    minp: int
        Minimum number of observations in window required to have a value 
        (otherwise result is NaN).
    ddof: int
        Delta degrees of freedom. The divisor used in calculations is N - ddof, 
        where N represents the number of elements.

    Returns
    -------
    output: pandas.core.frame.DataFrame
        A :code:`pandas` DataFrame with the rolling standard deviation of :code:`input`.
    """
    _assertions(input,win,minp,ddof=ddof)
    return pd.DataFrame(_roll_std(input.values,win,minp,ddof=ddof),input.index)


@njit(parallel=False)
def _roll_std(input,win,minp,ddof=1):
    """
    Computes the rolling standard deviation of a numpy array.

    Parameters
    ----------
    input: np.array of type double
    win: int 
        Length of the moving window
    minp: int 
        Minimum number of observations in window required to have a value 
        (otherwise result is NA).
    ddof: int
        Delta cegrees of freedom. The divisor used in calculations is N - ddof, 
        where N represents the number of elements.

    Returns
    -------
    output: np.array of type double
    """

    val = float(0)
    prev = float(0)
    sum_x = float(0)
    sum_xx = float(0)
    nobs = int(0)
    N = int(len(input))

    minp = _check_minp(win, minp, N)        
    output = np.empty(N,dtype=np.float64)

    for i in range(minp - 1):
        val = input[i]
        
        if val == val:
            nobs += 1
            sum_x += val
            sum_xx += val**2

        output[i] = np.nan

    for i in range(minp - 1,N):        
        val = input[i]

        if val == val:
            nobs += 1
            sum_x += val
            sum_xx += val**2

        if i > win - 1:
            prev = input[i - win]
            
            if prev == prev:
                sum_x -= prev
                sum_xx -= prev**2
                nobs -= 1

        if nobs >= minp:
            # pathological case
            if nobs == 1:
                output[i] = 0
                continue

            val = (nobs * sum_xx - sum_x**2) / (nobs * (nobs - ddof))
            if val < 0:
                val = 0

            output[i] = np.sqrt(val)
        else:
            output[i] = np.nan

    return output

def _assertions(input,win,minp,ddof=-999):
    assert (isinstance(input,pd.core.frame.DataFrame) or isinstance(input,pd.core.series.Series)), 'Input must be a pandas Series or DataFrame'
    assert ddof<input.shape[0], 'Invalid input for ddof: ddof must be less than the number of observations in input'
    if len(input.dtypes) > 0:
        assert input.dtypes in 'biufc', 'All columns must be a numeric type.'
    else:
        assert all([(d.kind in 'biufc') for d in input.dtypes]), 'All columns must be a numeric type.'

def _assertions2(x,y,win,minp,idx,ddof=-999):
    assert isinstance(x,pd.core.series.Series), 'x must be a pandas Series'
    assert isinstance(y,pd.core.series.Series), 'y must be a pandas Series'
    assert ddof<x.shape[0], 'Invalid input for ddof: ddof must be less than the number of observations in x and y'
    assert x.shape==y.shape, 'x and y must have the same shape'
    assert (idx=='x' or idx=='y'), 'Invalid input for idx'
    if len(input.dtypes) > 0:
        assert input.dtypes in 'biufc', 'All columns must be a numeric type.'
    else:
        assert all([(d.kind in 'biufc') for d in input.dtypes]), 'All columns must be a numeric type.'


def roll_cov(x,y,win,minp,ddof=1,idx='x'):
    """
    Computes the rolling covariance of two :code:`pandas` series.

    Parameters
    ----------
    x: pandas.core.series.Series
        This series must have strictly numeric type.
    y: pandas.core.series.Series
        This series must have strictly numeric type.
    win: int
        Length of the moving window
    minp: int
        Minimum number of observations in window required to have a value 
        (otherwise result is NaN).
    ddof: int
        Delta degrees of freedom. The divisor used in calculations is N - ddof, 
        where N represents the number of elements.
    idx: {'x','y'}
        Whether to use the index for x or for y for the return series. Defaults to 'x'.

    Returns
    -------
    output: pandas.core.series.Series
        A :code:`pandas` Series with the rolling covariance of x and y.
    """
    _assertions2(x,y,win,minp,idx,ddof=ddof)
    if idx=='x':
        myidx = x.index
    else: 
        myidx = y.index
    return pd.DataFrame(_roll_cov(x.values,y.values,win,minp,ddof=ddof),myidx)

@njit(parallel=False)
def _roll_cov(arr_x,arr_y,win,minp,ddof=1):
    """
    Computes the rolling covariance between two numpy arrays

    Parameters
    ----------
    arr_x: np.array of type double
    arr_y : np.array of type double
    win: int 
        Length of the moving window
    minp: int
        Minimum number of observations in window required to have a value 
        (otherwise result is NA).
    ddof: int
        Delta degrees of freedom. The divisor used in calculations is N - ddof, 
        where N represents the number of elements.

    Returns
    -------
    output: np.array of type double
    """

    sum_x = float(0)
    sum_y = float(0)
    sum_xy = float(0)
    nobs = int(0)
    N = int(len(arr_x))

    minp = _check_minp(win, minp, N)        
    output = np.empty(N,dtype=np.float64)

    for i in range(minp - 1):    
        x = arr_x[i]
        y = arr_y[i]        

        if x == x and y == y:
            nobs += 1
            sum_x += x
            sum_y += y
            sum_xy += x*y

        output[i] = np.nan

    for i in range(minp - 1,N):        
        x = arr_x[i]
        y = arr_y[i]        

        if x == x and y == y:
            nobs += 1
            sum_x += x
            sum_y += y
            sum_xy += x*y

        if i > win - 1:
            prev_x = arr_x[i - win]
            prev_y = arr_y[i - win]
            
            if prev_x == prev_x and prev_y == prev_y:
                nobs -= 1
                sum_x -= prev_x
                sum_y -= prev_y                
                sum_xy -= prev_x*prev_y

        if nobs >= minp:
            # pathological case
            if nobs == 1:
                output[i] = 0
                continue

            output[i] = (nobs * sum_xy - sum_x*sum_y) / (nobs * (nobs - ddof))
        else:
            output[i] = np.nan

    return output

def roll_idio(y,x,win,minp,ddof=1,idx='x'):
    """
    Computes the rolling idio residual standard deviation from a univariate 
    regression, y = a + bx + e.

    Parameters
    ----------
    y: pandas.core.series.Series
        This series must have strictly numeric type.
    x: pandas.core.series.Series
        This series must have strictly numeric type.
    win: int
        Length of the moving window
    minp: int
        Minimum number of observations in window required to have a value 
        (otherwise result is NaN).
    ddof: int
        Delta degrees of freedom. The divisor used in calculations is N - ddof, 
        where N represents the number of elements.
    idx: {'x','y'}
        Whether to use the index for x or for y for the return series. Defaults to 'x'.

    Returns
    -------
    output: pandas.core.series.Series
        A :code:`pandas` Series with the rolling idio residual standard deviation from a univariate regression, y = a + bx + e.
    """
    _assertions2(x,y,win,minp,idx,ddof=ddof)
    if idx=='x':
        myidx = x.index
    else: 
        myidx = y.index
    return pd.DataFrame(_roll_idio(y.values,x.values,win,minp,ddof=ddof),myidx)


@njit(parallel=False)
def _roll_idio(arr_y,arr_x,win,minp,ddof=1):
    """
    Computes the rolling idio residual standard deviation from a univariate 
    regression, y = a + bx + e.

    Parameters
    ----------
    arr_y: np.array, dtype=double
        the dependent variable 
    arr_x: np.array, dtype=double
        the independent variable
    win: float
        Length of the moving window
    minp: float
        Minimum number of observations in window required to have a value 
        (otherwise result is NA).
    ddof: float 
        Delta cegrees of freedom. The divisor used in calculations is N - ddof,
        where N represents the number of elements.

    Returns
    -------
    out: np.array, dtype = double
    """
    
    var_y = _roll_var(arr_y,win,minp,ddof)
    var_x = _roll_var(arr_x,win,minp,ddof)
    cov   = _roll_cov(arr_y,arr_x,win,minp,ddof)    

    N = int(len(arr_x))
    out = np.empty(N,dtype=np.float64)

    for i in range(0,N):
        out[i] = np.sqrt(var_y[i] - cov[i]**2/var_x[i])

    return out

def roll_beta(y,x,win,minp,ddof=1,idx='x'):
    """
    Computes the rolling estimated slope coefficient (beta)  from an univariate regression, y = a + bx + e. 

    Parameters
    ----------
    y: pandas.core.series.Series
        This series must have strictly numeric type.
    x: pandas.core.series.Series
        This series must have strictly numeric type.
    win: int
        Length of the moving window
    minp: int
        Minimum number of observations in window required to have a value 
        (otherwise result is NaN).
    ddof: int
        Delta degrees of freedom. The divisor used in calculations is N - ddof, 
        where N represents the number of elements.
    idx: {'x','y'}
        Whether to use the index for x or for y for the return series. Defaults to 'x'.

    Returns
    -------
    output: pandas.core.series.Series
        A :code:`pandas` Series with the rolling estimated slope coefficient (beta)  from an univariate regression, y = a + bx + e. 
    """
    _assertions2(x,y,win,minp,idx,ddof=ddof)
    if idx=='x':
        myidx = x.index
    else: 
        myidx = y.index
    return pd.DataFrame(_roll_beta(y.values,x.values,win,minp,ddof=ddof),myidx)

@njit(parallel=False)
def _roll_beta(arr_y,arr_x,win,minp,ddof=1):
    """
    Computes the rolling estimated slope coefficient (beta)  from an 
    univariate regression, y = a + bx + e. 

    Parameters
    ----------
    arr_y: np.array, dtype=double
        the dependent variable 
    arr_x: np.array, dtype=double
        the independent variable
    win: float
        Length of the moving window
    minp: float
        Minimum number of observations in window required to have a value 
        (otherwise result is NA).
    ddof: float 
        Delta cegrees of freedom. The divisor used in calculations is N - ddof,
        where N represents the number of elements.

    Returns
    -------
    out: np.array, dtype = double
    """
    
    var_x = _roll_var(arr_x,win,minp,ddof)
    cov   = _roll_cov(arr_y,arr_x,win,minp,ddof)    

    N = int(len(arr_x))
    out = np.empty(N,dtype=np.float64)

    for i in range(N):
        out[i] = cov[i]/var_x[i]

    return out

 
