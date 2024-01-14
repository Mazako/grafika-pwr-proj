import math
from itertools import chain

import numpy as np

from sierpinski.engine.Texture import Texture
from sierpinski.pyramid.SierpinskiPyramid import SierpinskiPyramid


def distance(v1, v2):
    return math.sqrt(((v1[0] - v2[0]) ** 2) + ((v1[1] - v2[1]) ** 2) + ((v1[2] - v2[2]) ** 2))


def mid(v1, v2):
    return [(v1[0] + v2[0]) / 2, (v1[1] + v2[1]) / 2, (v1[2] + v2[2]) / 2]


def create(program_id, draw_type, level=0):
    pyramid_h = (2 * math.sqrt(6) / 3)
    triangle_center = math.fabs((math.sqrt(3) / 3) - 1)

    p1 = np.array([-1, 0, triangle_center - 1])
    p2 = np.array([1, 0, triangle_center - 1])
    p3 = np.array([0, 0, triangle_center - 1 + math.sqrt(3)])
    p4 = np.array([0, pyramid_h, 0])

    vertices = []
    colors = []
    normals = []
    uvs = []

    create_sierpinski(p1, p2, p3, p4, level, vertices, colors, normals, uvs)
    texture = Texture('../textures/texture.png')
    print('SIERPINSKI READY')

    return SierpinskiPyramid(program_id, draw_type, vertices, colors, normals, uvs, texture.texture_id)


def create_sierpinski(v1, v2, v3, v4, level, vertices, colors, normals, uvs):
    if level == 0:
        triangles = [
            [v1, v2, v3],
            [v1, v2, v4],
            [v2, v3, v4],
            [v1, v3, v4]
        ]
        n1 = calculate_normal(v1, v2, v3)
        n2 = calculate_normal(v1, v2, v4)
        n3 = calculate_normal(v2, v3, v4)
        n4 = calculate_normal(v1, v3, v4)
        normals_arr = [
            [n1, n1, n1],
            [n2, n2, n2],
            [n3, n3, n3],
            [n4, n4, n4]
        ]

        u1 = np.array([0, 0], np.float32)
        u2 = np.array([1, 1], np.float32)
        uv = [
            [u1, u2],
            [u1, u2],
            [u1, u2],
            [u1, u2],
            [u1, u2],
            [u1, u2],
            [u1, u2],
            [u1, u2],
        ]

        vertices.extend(list(chain(*triangles)))
        normals.extend(list(chain(*normals_arr)))
        uvs.extend(list(chain(*uv)))
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
        create_sierpinski(v1, mid_12, mid_13, mid_14, level - 1, vertices, colors, normals, uvs)
        create_sierpinski(mid_12, v2, mid_23, mid_24, level - 1, vertices, colors, normals, uvs)
        create_sierpinski(mid_13, mid_23, v3, mid_34, level - 1, vertices, colors, normals, uvs)
        create_sierpinski(mid_14, mid_24, mid_34, v4, level - 1, vertices, colors, normals, uvs)


def calculate_normal(a, b, c):
    v1 = np.array(b) - np.array(a)
    v2 = np.array(c) - np.array(a)
    cross = np.cross(v1, v2)
    normal = cross / np.linalg.norm(cross)
    if normal[1] > 0:
        return -normal
    return normal
