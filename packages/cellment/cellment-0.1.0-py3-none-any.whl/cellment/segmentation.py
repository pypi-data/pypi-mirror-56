import numpy as np
import numba
from scipy import ndimage, interpolate
from pyclipper import SimplifyPolygon, PFT_POSITIVE


@numba.njit
def __normal_direction(x):
    out = np.empty_like(x)
    for k in range(len(x) - 1):
        r = x[k + 1] - x[k - 1]
        out[k] = (-r[1], r[0])
    r = x[0] - x[-2]
    out[-1] = (-r[1], r[0])
    return out


def normal(x):
    n = __normal_direction(x)
    return n / np.linalg.norm(n, axis=-1, keepdims=True)


def redistribute(x, size=None, distance=None, wrap=True):
    if size is None and distance is None:
        raise Exception('You must specify either size or distance.')
    if not wrap:
        raise NotImplementedError
    else:
        x = np.concatenate((x, x[:1]))
        L = np.cumsum(np.linalg.norm(np.diff(x, prepend=x[:1], axis=0), axis=-1))
        ix = np.arange(L.size)
        if distance is not None:
            size = int(L[-1] / distance)
        new_L = np.linspace(0, L[-1], size, endpoint=False)
        new_ix = np.interp(new_L, L, ix)
        new_x = interpolate.interp1d(ix, x, kind='linear', axis=0, copy=False, assume_sorted=True)(new_ix)
    return new_x


def circle_curve(x0, radius, distance):
    t = np.linspace(0, 2 * np.pi, int(2 * np.pi * radius / distance), endpoint=False)
    y = radius * np.array([np.sin(t), np.cos(t)]).T + np.asarray(x0)
    return y


def coords_inside_image(x, shape):
    out = x
    out = np.maximum(out, np.zeros_like(shape))
    out = np.minimum(out, np.asarray(shape) - 1)
    mask = (out == x).all(1)
    return out, mask


def expand(y, shape, direction=1):
    # Expand normally
    n = normal(y)
    y_new = y + direction * n
    # Crop outside image
    y_new, inside = coords_inside_image(y_new, shape)
    outside = ~inside
    # Get coordinates
    ix_new = tuple(yi for yi in y_new.T.astype(int))
    return ix_new, y_new, outside


def probability_of_movement(ix_new, outside):
    # TODO: weighted sum in probability
    prob = bg_cdf(im[ix_new])  # Background
    prob += smo_cdf(smo[ix_new])  # SMO
    prob[outside] = 0
    # Neighbour
    # TODO: Add neighbour direction
    prob = ndimage.gaussian_filter(prob, sigma_nb, mode='wrap')
    prob[outside] = 0
    return prob


def clean_curve(y, distance):
    # Simplify polygon
    simples = SimplifyPolygon(1e6 * y[:, ::-1], PFT_POSITIVE)[0]
    y = np.array(simples, dtype=float)[:, ::-1] / 1e6
    # Redistribute points in polygon
    y = redistribute(y, distance=distance)
    return y


def solment_iteration(y, im, smo, bg_cdf, smo_cdf, p_thres, sigma_nb, distance):
    ix_new, y_new, outside = expand(y, im.shape)
    prob = probability_of_movement(ix_new)
    cond = (prob > p_thres)  # Threshold for movement
    y[cond] = y_new[cond]
    y = clean_curve(y, distance)
    stop = ~cond.any()
    return y, stop
