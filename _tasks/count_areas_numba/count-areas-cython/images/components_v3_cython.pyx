'''
slower than numba - 0.10 against 0.6

HELPS:
memoryview for numpy array 
cdef unsigned char [:] bitmap = bitmap_numpy # memoryview

typing of most of variables
    - but not of upper_point(search 'WTF'), left_point for some reason, even though body becomes white in annotated html

@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
@cython.overflowcheck.fold(False)
@cython.cdivision(True)
'''

cimport cython

import numpy as np
cimport numpy as np

# memoryviews
# http://docs.cython.org/en/latest/src/userguide/memoryviews.html

from libcpp.map cimport map
from libcpp.vector cimport vector
from cython.operator cimport dereference, postincrement
from libc.stdlib cimport malloc, free

'''
cdef extern from "<vector>" namespace "std":
    cdef cppclass vector[T]:
        cppclass iterator:
            T operator*()
            iterator operator++()
            bint operator==(iterator)
            bint operator!=(iterator)
        vector()
        void push_back(T&)
        T& operator[](int)
        T& at(int)
        iterator begin()
        iterator end()
'''

DTYPE8 = np.uint8
ctypedef np.uint8_t DTYPE8_t

DTYPE32 = np.uint32
ctypedef np.uint32_t DTYPE32_t

STUFF = "Hi" # hack to avoid import error

cpdef DTYPE32_t replace_component_if_merged(unsigned int component_id, map[unsigned int, unsigned int] merge_components):# nogil:
    """ Takes component_id and saved merges data, and replaces component_id with id of root component. """
    while merge_components.find(component_id) != merge_components.end():
        component_id = dereference(merge_components.find(component_id)).second
    return component_id

# DOCS https://cython.readthedocs.io/en/latest/index.html

'''
profiling.                  https://stackoverflow.com/questions/19537673/slow-division-in-cython
add @cython.profile(True)

python3 -m cProfile -s cumulative performance.py
'''

# nogil https://cython.readthedocs.io/en/latest/src/userguide/parallelism.html

# hack for https://github.com/dask/distributed/issues/1978
# ValueError: buffer source array is read-only.   for bytes read from file
def _memoryview_safe(x):
    """Make array safe to run in a Cython memoryview-based kernel. These
    kernels typically break down with the error ``ValueError: buffer source
    array is read-only`` when running in dask distributed.
    """
    if not x.flags.writeable:
        if not x.flags.owndata:
            x = x.copy(order='C')
        x.setflags(write=True)
    return x

# https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html
@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
@cython.overflowcheck.fold(False)
@cython.cdivision(True)
#@cython.profile(True)
cpdef np.ndarray[DTYPE32_t, ndim=1] _get_image_colours_component_count(np.ndarray[DTYPE8_t, ndim=1] bitmap_numpy, DTYPE32_t bitmap_height_, DTYPE32_t bitmap_width_):
#cpdef np.ndarray[DTYPE32_t,ndim=1] _get_image_colours_component_count(unsigned char [:] bitmap, unsigned int bitmap_height, unsigned int bitmap_width): # nogil:
    """Takes 2D numpy array with image bitmap and returns number of components per colour."""
    #cdef np.ndarray[DTYPE32_t,ndim=1] components = np.zeros((2*bitmap_width), dtype = DTYPE32) # we optimize for memory here(use only bitmap_width * 2 elements)
    #cdef unsigned int *bitmap = <unsigned int *> malloc(bitmap_height*bitmap_width * sizeof(unsigned int))
    #for current_point_ in range(bitmap_numpy.size):
    #    bitmap[current_point_] = bitmap_numpy[current_point_]
    cdef unsigned char [:] bitmap = _memoryview_safe(bitmap_numpy) # memoryview
    cdef unsigned int bitmap_height = bitmap_height_
    cdef unsigned int bitmap_width  = bitmap_width_
    cdef unsigned int *components = <unsigned int *> malloc(2*bitmap_width * sizeof(unsigned int)) #TODO finally free https://cython.readthedocs.io/en/latest/src/tutorial/memory_allocation.html
    cdef map[unsigned int, unsigned int] component_colours # keep {component_id: colour} pairs here, if component is merged then pair is deleted
    cdef unsigned int current_component_id = 0
    cdef map[unsigned int, unsigned int] merge_components
    cdef unsigned int min_component, max_component
    cdef unsigned int upper_component, left_component
    cdef unsigned int upper_same_color, left_same_color, upper_point, left_point #WTF #commenting out upper_point, left_point helps speed 1.5x
    cdef unsigned int current_point = 0
    cdef unsigned int bitmap_size = bitmap_width * bitmap_height
    while current_point < bitmap_size:
    #for current_point in range(bitmap_numpy.size):
        upper_component  = left_component  = 0
        upper_same_color = left_same_color = 0
        # fill in "upper_component" (upper cell's component id) and
        # "upper_same_color"(boolean flag - if upper cell's has same colour) variables
        if current_point >= bitmap_width:
            upper_point = current_point - bitmap_width
            upper_same_color = bitmap[upper_point] == bitmap[current_point]
            if upper_same_color:
                upper_component = components[upper_point % (2*bitmap_width)]
                #upper_component = replace_component_if_merged(upper_component, merge_components) #UNTODO
                while merge_components.find(upper_component) != merge_components.end():
                    upper_component = dereference(merge_components.find(upper_component)).second
        # fill in "left_component" and "left_same_color" variables
        if current_point % bitmap_width:
            left_point = current_point - 1
            left_same_color = bitmap[left_point] == bitmap[current_point]
            if left_same_color:
                left_component = components[left_point % (2*bitmap_width)]
                #left_component = replace_component_if_merged(left_component, merge_components)
                while merge_components.find(left_component) != merge_components.end():
                    left_component = dereference(merge_components.find(left_component)).second
        else: # start of new row, so forget data about unreachable cells
            pass # no clean for now
            #merge_components_prev = merge_components
            #merge_components = dict_uint32_uint32()
        # set current cell component
        if upper_same_color and left_same_color and upper_component != left_component: # merge 2 same coloured component
            if upper_component < left_component: # we always merge max_component into min_component(see details in description)
                min_component = upper_component
                max_component = left_component
            else:
                min_component = left_component
                max_component = upper_component
            components[current_point % (2*bitmap_width)] = min_component
            merge_components[max_component] = min_component # remember merge to repeat it on following row
            if component_colours.find(max_component) != component_colours.end(): # forget merged element colour
                component_colours.erase(max_component)
        elif upper_same_color or left_same_color: # extend neighbouring component to current cell
            components[current_point % (2*bitmap_width)] = upper_component if upper_same_color else left_component
        else: # new component starts here
            components[current_point % (2*bitmap_width)] = current_component_id
            component_colours[current_component_id] = bitmap[current_point]
            current_component_id += 1
        current_point += 1
    # copy colour to result
    '''
    cdef vector[unsigned int] *result = new vector[unsigned int]()
    cdef map[DTYPE32_t,DTYPE32_t].iterator it = component_colours.begin()
    while(it != component_colours.end()):
        result.push_back(dereference(it).second)
        postincrement(it)
    '''
    cdef np.ndarray[DTYPE32_t,ndim=1] result = np.zeros((len(component_colours)), dtype = DTYPE32)
    cdef map[DTYPE32_t,DTYPE32_t].iterator it = component_colours.begin()
    cdef unsigned int indx = 0
    while(it != component_colours.end()):
        result[indx] = dereference(it).second
        postincrement(it)
        indx += 1
    free(components) # must use finally. https://cython.readthedocs.io/en/latest/src/tutorial/memory_allocation.html
    return result

'''
cimport cython

import numpy as np
cimport numpy as np

from libcpp.map cimport map
from cython.operator cimport dereference, postincrement

DTYPE8 = np.uint8
ctypedef np.uint8_t DTYPE8_t

DTYPE32 = np.uint32
ctypedef np.uint32_t DTYPE32_t

STUFF = "Hi"

cpdef DTYPE32_t replace_component_if_merged(DTYPE32_t component_id, map[DTYPE32_t, DTYPE32_t] merge_components):
    """ Takes component_id and saved merges data, and replaces component_id with id of root component. """
    while merge_components.find(component_id) != merge_components.end():
        component_id = dereference(merge_components.find(component_id)).second
    return component_id

@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cpdef np.ndarray[DTYPE32_t, ndim=1] _get_image_colours_component_count(np.ndarray[DTYPE8_t, ndim=1] bitmap, DTYPE32_t bitmap_height, DTYPE32_t bitmap_width):
    """Takes 2D numpy array with image bitmap and returns number of components per colour."""
    cdef np.ndarray[DTYPE32_t,ndim=1] components = np.zeros((2*bitmap_width), dtype = DTYPE32) # we optimize for memory here(use only bitmap_width * 2 elements)
    cdef map[DTYPE32_t, DTYPE32_t] component_colours # keep {component_id: colour} pairs here, if component is merged then pair is deleted
    cdef DTYPE32_t current_component_id = 0
    cdef map[DTYPE32_t, DTYPE32_t] merge_components
    cdef DTYPE32_t min_component, max_component
    cdef DTYPE32_t upper_component, left_component
    cdef DTYPE32_t upper_same_color, left_same_color
    #cdef DTYPE32_t current_point = 0, bitmap_size = bitmap.size
    #while current_point < bitmap_size:
    for current_point in range(bitmap.size):
        upper_component  = left_component  = 0
        upper_same_color = left_same_color = 0
        # fill in "upper_component" (upper cell's component id) and
        # "upper_same_color"(boolean flag - if upper cell's has same colour) variables
        if current_point >= bitmap_width:
            upper_point = current_point - bitmap_width
            upper_same_color = bitmap[upper_point] == bitmap[current_point] # bitmap access is not very efficient here(and on line for left_same_color) but numba inspect shows good code :(
            if upper_same_color:
                upper_component = components[upper_point % (2*bitmap_width)]
                upper_component = replace_component_if_merged(upper_component, merge_components)
        # fill in "left_component" and "left_same_color" variables
        if current_point % bitmap_width:
            left_point = current_point - 1
            left_same_color = bitmap[left_point] == bitmap[current_point]
            if left_same_color:
                left_component = components[left_point % (2*bitmap_width)]
                left_component = replace_component_if_merged(left_component, merge_components)
        else: # start of new row, so forget data about unreachable cells
            pass # no clean for now
            #merge_components_prev = merge_components
            #merge_components = dict_uint32_uint32()
        # set current cell component
        if upper_same_color and left_same_color and upper_component != left_component: # merge 2 same coloured component
            if upper_component < left_component: # we always merge max_component into min_component(see details in description)
                min_component = upper_component
                max_component = left_component
            else:
                min_component = left_component
                max_component = upper_component
            components[current_point % (2*bitmap_width)] = min_component
            merge_components[max_component] = min_component # remember merge to repeat it on following row
            if component_colours.find(max_component) != component_colours.end(): # forget merged element colour
                component_colours.erase(max_component)
        elif upper_same_color or left_same_color: # extend neighbouring component to current cell
            components[current_point % (2*bitmap_width)] = upper_component if upper_same_color else left_component
        else: # new component starts here
            components[current_point % (2*bitmap_width)] = current_component_id
            component_colours[current_component_id] = bitmap[current_point]
            current_component_id += 1
        current_point += 1
    # copy colour to result
    cdef np.ndarray[DTYPE32_t,ndim=1] result = np.zeros((len(component_colours)), dtype = DTYPE32)
    cdef map[DTYPE32_t,DTYPE32_t].iterator it = component_colours.begin()
    cdef DTYPE32_t indx = 0
    while(it != component_colours.end()):
        result[indx] = dereference(it).second
        postincrement(it)
        indx += 1
    return result
'''
