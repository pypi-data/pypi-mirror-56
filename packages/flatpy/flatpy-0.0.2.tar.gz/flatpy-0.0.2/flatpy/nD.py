import numpy as np
import copy
import math
import scipy.optimize


def ackley(x, a=20, b=0.2, c=2*math.pi):
    x = 2*np.atleast_2d(x)-1
    d = x.shape[1]

    sum1 = 0
    sum2 = 0
    for ii in range(d):
        xi = x[:, ii]
        sum1 = sum1 + xi**2
        sum2 = sum2 + np.cos(c*xi)

    term1 = -a * np.exp(-b*np.sqrt(sum1/d))
    term2 = -np.exp(sum2/d)

    y = term1 + term2 + a + np.exp(1)
    return y


def decay(x):
    x = np.atleast_2d(x)
    d = x.shape[1]
    eps = 0
    for i in range(d):
        eps += x[:, i]*1e-6

    dist = np.zeros(x.shape[0])
    for i in range(d):
        dist += x[:, i]**2
    dist = np.sqrt(dist)
    ans = (0.1 + eps)
    indices = np.where(dist <= 1)
    ans[indices] = 0.1 + (1-dist[indices]**3)**3 + eps[indices]
    return ans


def diagonal(x, max_count=3):
    x = np.atleast_2d(x)
    d = x.shape[1]

    summand = 0
    sum_squared = 0

    for i in range(d):
        summand += x[:, i]
        sum_squared += x[:, i]**2

    diag_dist = np.exp(((sum_squared) - summand**2/d)*np.log(0.001)/np.sqrt(d))
    func = 0.5*np.sin(0.5*math.pi + math.pi*((2*max_count+1) % 2) + math.pi*0.5*(4*max_count)*(summand) / d)

    return diag_dist*func

def checkerBoard(x):
    x = np.atleast_2d(x)
    d = x.shape[1]

    periodicTerm = 1
    for i in range(d):
        sgn = np.cos(x[:, i]*math.pi)/abs(np.cos(x[:, i]*math.pi))
        periodicTerm *= sgn*abs(np.cos(x[:, i]*math.pi))**(1/7.)
    return periodicTerm


def flatTop(x):
    return checkerBoard(x)*decay(x)


def rosenbrock(x):
    x = 4.8*np.atleast_2d(x) - 2.4
    d = x.shape[1]
    return scipy.optimize.rosen(x.T)


def salomon(x):
    x = 2*np.atleast_2d(x)-1
    d = x.shape[1]

    summand = 0
    for i in range(d):
        summand += x[:, i]**2
    summand = np.sqrt(summand)
    return 1 - np.cos(2*math.pi*summand)+0.1*summand


def schwefel(x):
    x = 1000*np.atleast_2d(x)-500
    d = x.shape[1]

    retValue = 418.9829*d
    for i in range(d):
        retValue -= x[:, i]*np.sin(np.sqrt(abs(x[:, i])))
    return retValue


def shekel(x):
    x = 10*np.atleast_2d(x)
    d = x.shape[1]

    m = 4
    a = np.zeros((m, d))
    c = np.ones(m)

    # i = 0 (center of domain)
    # i = 1 (upper corner)
    # i = 2 (odd low, even high)
    # i = 3 (odd high, even low)
    c[0] = 0.25
    c[1] = 0.5
    c[2] = 0.75
    c[3] = 1
    for j in range(d):
        a[0, j] = 5
        a[1, j] = 10
        if j % 2:
            a[2, j] = 9
            a[3, j] = 1
        else:
            a[2, j] = 1
            a[3, j] = 9

    summand = 0
    for i in range(m):
        subSummand = c[i]
        for j in range(d):
            subSummand += (x[:, j]-a[i, j])**2
        summand += (subSummand)**-1
    return summand


available_functions = {"ackley": ackley, "checkerBoard": checkerBoard,
                       "diagonal": diagonal, "flatTop": flatTop,
                       "rosenbrock": rosenbrock, "salomon": salomon,
                       "schwefel": schwefel, "shekel": shekel}
