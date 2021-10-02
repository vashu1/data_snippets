'''
Count number of colored areas in an bitmap.

Usage:
from images.components_v2 import get_image_colours_component_count

Counter() = get_image_colours_component_count(numpy.array([...], dtype = np.uint8).reshape((height,width)))

Takes 2D numpy array of uint8s, and returns Counter with colors data: Counter({color: count})
'''
import numpy as np
import numba
from numba.typed import Dict
from numba import types
from collections import Counter

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
    return Counter(_get_image_colours_component_count(bitmap))

@numba.jit(nopython=True, nogil=True, inline='always', cache=True)
def replace_component_if_merged(component_id, merge_components, merge_components_prev):
    """ Takes component_id and saved merges data, and replaces component_id with id of root component. """
    # numba does not know dict().get so we go it this way
    while component_id in merge_components or component_id in merge_components_prev:
        if component_id in merge_components:
            component_id = merge_components[component_id]
        else:
            component_id = merge_components_prev[component_id]
    return component_id

@numba.jit(nopython=True, nogil=True, inline='always', cache=True) #TODO drop all xcept always inline
def dict_uint32_uint32():
    """ Wrapper for Dict call. """
    return Dict.empty(key_type=types.uint32, value_type=types.uint32)

'''
Basic idea: we compare only 3 cells/pixels - the current and the left and upper ones.

(pixel) (pixel) ( pixel ) (pixel)
(pixel) (pixel) ( upper ) (pixel)
(pixel) (left ) (CURRENT) (pixel)
(pixel) (pixel) ( pixel ) (pixel)

If we see that upper|left pixel have different colour then current - we mark it with new
component id. If we see same colour - we extend existing component.

Problem with this approach occurs when it is necessary to merge components.

(white pixel) (black, id:4)
(black, id:5) (black, id:?) <- current pixel

When we meet situation like that we remember to merge 5 into 4 for two following rows.

We always pick minimum id to keep merges direction consistent:
with two merges 3->2 2->1 it is easy to see that 3 and 2 go into one 1.

Memory usage would be rather bad for very fragmented images, as there is one
element in "component_colours" dictionary for every component.

We can optimize it by keeping track of components in last 2 lines, but there
are lots of extra code that worsen readability and performance is 30% worse so
I decided to keep this version.

@numba.jit((types.Array(types.uint8, 2, 'C', readonly=True),), nopython=True, locals={'left_component': types.uint32, 'upper_component': types.uint32}, parallel=True, cache=True)

- Signature and locals are here to suppress some warnings, parallel helps with 
performance a little, cache saves time on compilation.

Simple @njit works almost as good.
'''
@numba.jit((types.Array(types.uint8, 2, 'C', readonly=True),), nopython=True, locals={'left_component': types.uint32, 'upper_component': types.uint32}, parallel=True, cache=True)
def _get_image_colours_component_count(bitmap2d):
    """Takes 2D numpy array with image bitmap and returns number of components per colour."""
    bitmap_height, bitmap_width = bitmap2d.shape
    bitmap = bitmap2d.reshape(bitmap2d.size) # we work with one-dimensional array, it makes iterating elements a little simpler
    components = np.zeros(2*bitmap_width, dtype=np.uint32) # we optimize for memory here(use only bitmap_width * 2 elements)
    component_colours = {} # keep {component_id: colour} pairs here, if component is merged then pair is deleted
    current_component_id =  0
    merge_components = dict_uint32_uint32()
    merge_components_prev = dict_uint32_uint32()
    for current_point in range(bitmap.size):
        upper_component  = left_component  = 0
        upper_same_color = left_same_color = False
        # fill in "upper_component" (upper cell's component id) and
        # "upper_same_color"(boolean flag - if upper cell's has same colour) variables
        if current_point >= bitmap_width:
            upper_point = current_point - bitmap_width
            upper_same_color = bitmap[upper_point] == bitmap[current_point] # bitmap access is not very efficient here(and on line for left_same_color) but numba inspect shows good code :(
            if upper_same_color:
                upper_component = components[upper_point % (2*bitmap_width)]
                upper_component = replace_component_if_merged(upper_component, merge_components, merge_components_prev)
        # fill in "left_component" and "left_same_color" variables
        if current_point % bitmap_width:
            left_point = current_point - 1
            left_same_color = bitmap[left_point] == bitmap[current_point]
            if left_same_color:
                left_component = components[left_point % (2*bitmap_width)]
                left_component = replace_component_if_merged(left_component, merge_components, merge_components_prev)
        else: # start of new row, so forget data about unreachable cells
            merge_components_prev = merge_components
            merge_components = dict_uint32_uint32()
        # set current cell component
        if upper_same_color and left_same_color and upper_component != left_component: # merge 2 same coloured components
            if upper_component < left_component: # we always merge max_component into min_component(see details in description)
                min_component, max_component = (upper_component, left_component)
            else:
                min_component, max_component = (left_component, upper_component)
            components[current_point % (2*bitmap_width)] = min_component
            merge_components[max_component] = min_component # remember merge to repeat it on following row
            if max_component in component_colours: # forget merged element colour
                del component_colours[max_component]
        elif upper_same_color or left_same_color: # extend neighbouring component to current cell
            components[current_point % (2*bitmap_width)] = upper_component if upper_same_color else left_component
        else: # new component starts here
            components[current_point % (2*bitmap_width)] = current_component_id
            component_colours[current_component_id] = bitmap[current_point]
            current_component_id += 1
    return np.array(list(component_colours.values()), dtype = np.uint32)
