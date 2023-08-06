from flatpy.utils import unpack_2d
import numpy as np
import scipy
import scipy.special
import math


def gerber(_x):
    x, y = unpack_2d(_x)
    return ((2./4.) * np.exp(-((x-.25)**2)/0.09) +
            (3./4.) * np.exp(-((y-.25)**2)/0.09) +
            (3./4.) * np.exp(-((x-.75)**2)/0.01) +
            (4./4.) * np.exp(-((y-.75)**2)/0.01))


def gerber_rotated(_x):
    theta = math.pi/6.
    u, v = unpack_2d(_x)
    u = u + 0.0
    v = v - 0.4
    x = u*math.cos(theta) - v*math.sin(theta)
    y = u*math.sin(theta) + v*math.cos(theta)
    return ((2./4.) * np.exp(-((x-.25)**2)/0.09) +
            (3./4.) * np.exp(-((y-.25)**2)/0.09) +
            (3./4.) * np.exp(-((x-.75)**2)/0.01) +
            (4./4.) * np.exp(-((y-.75)**2)/0.01))


def local_bumps(x, y, amplitude=1./4., cx=0.5, cy=0.5):
    nx_off = cx - 0.1
    px_off = cx + 0.1
    ny_off = cy - 0.1
    py_off = cy + 0.1

    return (amplitude * np.exp(-((x - nx_off)**2+(y - ny_off)**2)/0.001) +
            amplitude * np.exp(-((x - px_off)**2+(y - py_off)**2)/0.001) +
            amplitude * np.exp(-((x - px_off)**2+(y - ny_off)**2)/0.001) +
            amplitude * np.exp(-((x - nx_off)**2+(y - py_off)**2)/0.001))


def gerber_bumpy(_x):
    x, y = unpack_2d(_x)
    return (gerber(_x) +
            (1/4.) * np.exp(-((x-0.25)**2+(y-0.25)**2)/0.09) +
            local_bumps(x, y, amplitude=1./8., cx=0.25, cy=0.25))


def gerber_smeared(_x):
    x, y = unpack_2d(_x)
    return ((1./2.) * np.exp(-((x-.25)**2)/0.09) +
            (3./4.) * np.exp(-((x-.75)**2)/0.01) +
            (1./1.) * np.exp(-((y-.75)**2)/0.01))


def goldstein_price(_x):
    x, y = unpack_2d(_x)
    xa = 4 * x - 2
    ya = 4 * y - 2

    term1 = 1 + (xa+ya+1)**2*(19-14*xa+3*(xa**2)-14*ya+6*xa*ya+3*(ya**2))
    term2 = 30 + (2*xa-3*ya)**2*(18-32*xa+12*(xa**2)+48*ya-36*xa*ya+27*(ya**2))

    return term1*term2


def hill(_x):
    x, y = unpack_2d(_x)
    return np.exp(- ((x - .55)**2 + (y-.75)**2)/.125) + 0.01*(x+y)


def hill_sided(_x):
    x, y = unpack_2d(_x)
    center_x = 0.5
    center_y = 0.5
    sigma_1 = 1.25
    sigma_2 = 0.05
    amplitude_1 = 3.0
    amplitude_2 = 1.
    eps = 0.01
    blend_rate = 20

    delta_x = x - center_x
    delta_y = y - center_y
    alpha_x = scipy.special.expit(blend_rate*delta_x)
    # alpha_y = scipy.special.expit(blend_rate*delta_y)

    common_numerator = delta_x**2 + delta_y**2
    offset = eps*(x+y)
    h1 = amplitude_1 * np.exp(-common_numerator/sigma_1) + offset
    h2 = amplitude_2 * np.exp(-common_numerator/sigma_2) + offset
    # h3 = alpha_y*h1 + (1 - alpha_y)*h2
    # return alpha_x*h1 + (1. - alpha_x)*h3
    return alpha_x*h1 + (1. - alpha_x)*h2


def himmelblau(_x):
    x, y = unpack_2d(_x)
    x = 12*x-6
    y = 12*y-6

    return (x**2 + y - 11)**2 + (x+y**2-7)**2


def hinge(_x):
    x, _ = unpack_2d(_x)
    # x = math.pi/4.*(x)
    # y = math.pi/4.*(y)
    # return np.cos(2*x) - np.cos(y)
    return np.abs(x-0.55)


def ranjan(_x):
    x, y = unpack_2d(_x)
    return x + y + x*y


def ridge(_x):
    x, y = unpack_2d(_x)
    theta = math.pi/3.
    sigx = .05
    sigy = .04
    a = np.cos(theta)**2/(2*sigx**2) + np.sin(theta)**2/(2*sigy**2)
    b = np.sin(2*theta)/(4*sigx**2) + np.sin(2*theta)/(4*sigy**2)
    c = np.sin(theta)**2/(2*sigx**2) + np.cos(theta)**2/(2*sigy**2)

    return 0.01*y + 0.5 * (np.exp(-((x-.75)**2)/0.01) +
                           np.exp(-((x)**2 + (y-1)**2)/0.1) +
                           np.exp(-((x)**2 + (y)**2)/0.005) -
                           np.exp(-(a*(x-.25)**2 + 2*b*(x-.25)*(y-.25) +
                                    c*(y-.25)**2)))


def ridge_rounded(_x):
    x, y = unpack_2d(_x)
    theta = math.pi/3.
    sigx = .05
    sigy = .04
    a = np.cos(theta)**2/(2*sigx**2) + np.sin(theta)**2/(2*sigy**2)
    b = np.sin(2*theta)/(4*sigx**2) + np.sin(2*theta)/(4*sigy**2)
    c = np.sin(theta)**2/(2*sigx**2) + np.cos(theta)**2/(2*sigy**2)

    return 0.01*y + 0.5 * (np.exp(-(((x-.75)**2)/0.01+((y-.5)**2)/0.4)) +
                           np.exp(-((x-.1)**2 + (y-1)**2)/0.1) +
                           np.exp(-((x-.1)**2 + (y-.1)**2)/0.005) -
                           np.exp(-(a*(x-.3)**2 + 2*b*(x-.3)*(y-.25) +
                                    c*(y-.25)**2)))


def strangulation(_x):
    x, y = unpack_2d(_x)
    return (0 -
            (0.2) * np.exp(-(np.power(x-0.25, 2) + np.power(y-0.25, 2))/0.001) -
            (0.2) * np.exp(-(np.power(x-0.25, 2) + np.power(y-0.75, 2))/0.001) -
            (0.2) * np.exp(-(np.power(x-0.75, 2) + np.power(y-0.25, 2))/0.001) -
            (0.2) * np.exp(-(np.power(x-0.75, 2) + np.power(y-0.75, 2))/0.001) +
            (1.0) * np.exp(-(np.power(x-0.50, 2) + np.power(y-0.50, 2))/0.125))


available_functions = {"gerber": gerber,
                       "gerber_rotated": gerber_rotated,
                       "gerber_bumpy": gerber_bumpy,
                       "gerber_smeared": gerber_smeared,
                       "goldstein_price": goldstein_price,
                       "hill": hill,
                       "hill_sided": hill_sided,
                       "himmelblau": himmelblau,
                       "hinge": hinge,
                       "ridge": ridge,
                       "ridge_rounded": ridge_rounded,
                       "strangulation": strangulation}
