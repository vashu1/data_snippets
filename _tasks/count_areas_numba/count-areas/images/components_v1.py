'''
!!! This code is not used, included only for reference. !!!

This naive implementation is based on algorithm for finding connected components in graph.

Performance is bad - it takes a couple of seconds to process 1M image, and numba improves it only 2x,
so "components_v2" with better performance was implemented.
'''
import numpy as np
from numba import njit

def get_image_components(bitmap): # returns components bitmap and dictionary of {component_id: color}
    """
    Takes 2D numpy array with image bitmap(shaped (height, width)) and returns number of components per colour.

    Just a wrapper for numba optimized function to validate parameters.
    """
    if not isinstance(bitmap, np.ndarray):
        raise TypeError('get_image_component_colours takes only "numpy.ndarray" as parameter.')
    if bitmap.ndim != 2:
        raise ValueError('get_image_component_colours takes 2 dimensional numpy array only.')
    if bitmap.dtype != np.dtype('uint8'): # easy to add other types, but it would need test changes
        raise ValueError('get_image_component_colours takes numpy array with uint8 type.')
    if bitmap.size > np.iinfo(np.uint32).max: # pretty unlikely to fire, if it does just change uint32 in module to uint64
        raise ValueError(f'get_image_component_colours can process only images with {np.iinfo(np.uint32).max} pixels.')
    bitmap_height, bitmap_width = bitmap.shape
    bitmap = bitmap.reshape(bitmap.size)
    return _get_image_components(bitmap, np.uint32(bitmap_height), np.uint32(bitmap_width))

@njit
def _get_image_components(bitmap, bitmap_height, bitmap_width): # returns components bitmap and dictionary of {component_id: color}
    components = np.zeros(bitmap.size, dtype=np.uint32)
    component_colours = {}
    current_component_id = np.uint32(1)
    for current_point in range(bitmap.size):
        if components[current_point] == 0: # point is not processed yet, add new component
            edge_points = list([current_point]) # first we add starting point
            while edge_points:
                edge_point = edge_points.pop()
                components[edge_point] = current_component_id # mark "edge_point" as belonging to component
                # and add its neighbours to "edge_points"
                edge_points.extend([point for point in point_neumann_neighbours(edge_point, bitmap_height, bitmap_width) if (not components[point]) and bitmap[edge_point] == bitmap[point]])
            component_colours[current_component_id] = bitmap[current_point] # remember color of component
            current_component_id += 1
    return components, component_colours

@njit
def point_neumann_neighbours(current_point, bitmap_height, bitmap_width):
    result = list()
    # left point
    if current_point > 0:
        if current_point % bitmap_width > 0:
            result.append(current_point - 1)
    # right point
    if current_point < bitmap_height * bitmap_width - 1:
        if current_point % bitmap_width < (bitmap_width - 1):
            result.append(current_point + 1)
    # upper and lower
    upper_point = current_point - bitmap_width
    if upper_point >= 0:
        result.append(upper_point)
    lower_point = current_point + bitmap_width
    if lower_point < bitmap_height * bitmap_width:
        result.append(lower_point)
    return result
