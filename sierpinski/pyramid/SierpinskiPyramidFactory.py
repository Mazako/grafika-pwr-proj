import math
from itertools import chain
import numpy as np
from sierpinski.pyramid.SierpinskiPyramid import SierpinskiPyramid


def distance(v1, v2):
    return math.sqrt(((v1[0] - v2[0]) ** 2) + ((v1[1] - v2[1]) ** 2) + ((v1[2] - v2[2]) ** 2))


def mid(v1, v2):
    return [(v1[0] + v2[0]) / 2, (v1[1] + v2[1]) / 2, (v1[2] + v2[2]) / 2]


def create(program_id, draw_type, level=0):
    p1 = [-1, 0, -1]
    p2 = [1, 0, -1]
    p3 = [0, 0, -1 + math.sqrt(3)]
    p4 = [0, (2 * math.sqrt(6) / 3), -1 + (math.sqrt(3) / 3)]
    coordinates = [p1, p2, p3, p4]
    print(coordinates)
    print(distance(p1, p2))
    print(distance(p2, p3))
    print(distance(p1, p3))
    print(distance(p1, p4))
    print(distance(p2, p4))
    print(distance(p3, p4))
    vertices = []
    colors = []
    create_sierpinski(p1, p2, p3, p4, level, vertices, colors)
    print(colors)
    return SierpinskiPyramid(program_id, draw_type, vertices, colors)


def create_sierpinski(v1, v2, v3, v4, level, vertices, colors):
    if level == 0:
        triangles = [
            [v1, v2, v3],
            [v1, v2, v4],
            [v2, v3, v4],
            [v1, v3, v4]
        ]

        vertices.extend(list(chain(*triangles)))
        for _ in range(4):
            rand_color = np.random.uniform(0.0, 1.0, 3).tolist()
            colors.append(rand_color * 3)
    else:
        mid_12 = mid(v1, v2)
        mid_13 = mid(v1, v3)
        mid_14 = mid(v1, v4)
        mid_23 = mid(v2, v3)
        mid_24 = mid(v2, v4)
        mid_34 = mid(v3, v4)
        create_sierpinski(v1, mid_12, mid_13, mid_14, level - 1, vertices, colors)
        create_sierpinski(mid_12, v2, mid_23, mid_24, level - 1, vertices, colors)
        create_sierpinski(mid_13, mid_23, v3, mid_34, level - 1, vertices, colors)
        create_sierpinski(mid_14, mid_24, mid_34, v4, level - 1, vertices, colors)
