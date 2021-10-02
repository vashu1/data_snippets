import numpy as np
from collections import Counter

from images.components_v3_cython import _get_image_colours_component_count
''' OR we can import pix this way

import pyximport
pyximport.install()
'''

def get_image_colours_component_count(bitmap):
    """
    Takes 2D numpy array with image bitmap(shaped (height, width)) and returns number of components per colour.

    Just a wrapper for numba optimized function to validate parameters.

    Input: 2D numpy array(shaped (height, width)) of uint8s.
    Returns: Counter with colors data: Counter({color: count})
    """
    if not isinstance(bitmap, np.ndarray):
        raise TypeError('get_image_component_colours takes only "numpy.ndarray" as parameter.')
    if bitmap.ndim != 2:
        raise ValueError('get_image_component_colours takes 2 dimensional numpy array only.')
    if bitmap.dtype != np.dtype('uint8'): # easy to add other types, but it would need test changes
        raise ValueError('get_image_component_colours takes numpy array with uint8 type.')
    # we use uint32 to store number of components
    # max number of components == number of pixels, so max number of pixels is MAX_INT32
    # pretty unlikely to fire, if it does just change uint32 in module to uint64
    if bitmap.size > np.iinfo(np.uint32).max:
        raise ValueError(f'get_image_component_colours can process only images with {np.iinfo(np.uint32).max} pixels.')
    bitmap_height, bitmap_width = bitmap.shape
    bitmap1d = bitmap.reshape((bitmap.size))
    return Counter(_get_image_colours_component_count(bitmap1d, np.uint32(bitmap_height), np.uint32(bitmap_width)))
