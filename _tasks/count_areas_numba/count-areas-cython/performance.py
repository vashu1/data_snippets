import timeit
from images.components_v3 import get_image_colours_component_count
from images.test_components_v2 import generate_triangle_cells

image1M = generate_triangle_cells(16,16,64,64)

print(timeit.timeit(stmt=lambda: get_image_colours_component_count(image1M), number=1))
print(timeit.timeit(stmt=lambda: get_image_colours_component_count(image1M), number=1))
print(timeit.timeit(stmt=lambda: get_image_colours_component_count(image1M), number=1))