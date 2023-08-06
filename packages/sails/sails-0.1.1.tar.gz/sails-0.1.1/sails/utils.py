#!/usr/bin/python

# vim: set expandtab ts=4 sw=4:

import math
import numpy as np
from scipy import signal

__all__ = []


def fast_resample(X, ds_factor):
    """Fast resampling of a timeseries array. This function pads the
    time-dimension to the nearest power of 2 to ensure that the resampling can
    use efficient FFT routines. The padding is removed before the downsampled
    data are returned.

    """

    orig_size = X.shape[1]
    target_size = X.shape[1] // ds_factor

    tmp_size = int(2**math.ceil(math.log(X.shape[1], 2)))
    tmp_target_size = int(tmp_size // ds_factor)

    tmp_X = np.concatenate([X, np.zeros((X.shape[0], tmp_size - orig_size))], axis=1)
    tmp_X = signal.resample(tmp_X, tmp_target_size, axis=1)
    return tmp_X[:, 0:target_size]


__all__.append('fast_resample')
