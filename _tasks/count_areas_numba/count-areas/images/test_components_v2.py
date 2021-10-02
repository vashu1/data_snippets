"""
Unit tests for components_v2.py
"""
import unittest
from unittest.mock import Mock
import numpy as np
from .components_v2 import get_image_colours_component_count
from collections import Counter
import os
import timeit

def generate_triangle_cells(ny, nx, height, width):
    '''
    Generates 2 * ny * nx triangle cells, width*height size, filled with different single byte colours. I.e.
    >>> generate_triangle_cells(1,1,3,3)
    array([[0., 1., 1.],
           [0., 0., 1.],
           [0., 0., 0.]])
    '''
    data = np.zeros(nx*ny*width*height, dtype=np. uint8).reshape((ny*height,nx*width))
    for cell_x in range(nx):
        for cell_y in range(ny):
            for x in range(width):
                for y in range(height):
                    data[cell_y*height + y][cell_x*width + x] = np.uint8(2 * (cell_y + cell_x * ny) + (1 if x >= y else 0))
    return data

class TestComponentsV2(unittest.TestCase):
    def test_bad_values(self):
        # wrong type
        with self.assertRaises(TypeError):
            get_image_colours_component_count(None)
        # not 2d array
        array_1d = np.zeros(0, dtype = np.uint8)
        with self.assertRaises(ValueError):
            get_image_colours_component_count(array_1d)
        # not uint8 elements
        uint16_array = np.zeros(0, dtype = np.uint16).reshape((0,0))
        with self.assertRaises(ValueError):
            get_image_colours_component_count(uint16_array)
        # size that would not fit in uint32
        toobig_mock = Mock(spec=np.ndarray)
        toobig_mock.ndim = 2
        toobig_mock.dtype = np.dtype('uint8')
        toobig_mock.size = int(10e10)
        with self.assertRaises(ValueError):
            get_image_colours_component_count(toobig_mock)

    def test_empty(self):
        empty_value = np.zeros(0, dtype = np.uint8).reshape((0,0))
        self.assertEqual(get_image_colours_component_count(empty_value), Counter())

    def test_single(self):
        single_value = np.ones(4, dtype = np.uint8).reshape((2,2))
        self.assertEqual(get_image_colours_component_count(single_value), Counter([1]))

    def test_simple(self):
        cells2_value = generate_triangle_cells(1,1,5,5) # 2 triangle cells
        self.assertEqual(get_image_colours_component_count(cells2_value), Counter(range(2)))

    def test_simple2(self):
        cells9_value = np.array(range(9), dtype = np.uint8).reshape((3,3))
        self.assertEqual(get_image_colours_component_count(cells9_value), Counter(range(9)))

    def test_repetitions(self):
        cells16_value = np.append(generate_triangle_cells(2,2,5,5), generate_triangle_cells(2,2,5,5)).reshape((20,10))
        self.assertEqual(get_image_colours_component_count(cells16_value), Counter(list(range(8))*2))

    def test_sample_bin_file(self):
        with open(os.path.dirname(os.path.realpath(__file__)) + '/resources/sample.bin','rb') as file:
            bitmap = np.frombuffer(file.read(), dtype = np.uint8).reshape((256,256))
            self.assertEqual(get_image_colours_component_count(bitmap), Counter({0: 3, 200: 2, 255: 2}))

    def test_large_image(self):
        image1M = generate_triangle_cells(16,16,64,64) # 16 * 16 * 2 = 512 cells, each 4KB
        self.assertEqual(get_image_colours_component_count(image1M), Counter(Counter(list(range(256))*2)))

if __name__ == '__main__':
    unittest.main()