import numpy as np
from math import *
import pygame


class Rotation:
    def __init__(self, angle, axis):
        self.angle = angle
        self.axis = axis


def identity_matrix():
    return np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]], np.float32)


def translate_matrix(x, y, z):
    return np.array([[1, 0, 0, x],
                     [0, 1, 0, y],
                     [0, 0, 1, z],
                     [0, 0, 0, 1]], np.float32)


def scale_matrix(s):
    return np.array([[s, 0, 0, 0],
                     [0, s, 0, 0],
                     [0, 0, s, 0],
                     [0, 0, 0, 1]], np.float32)


def scale_matrix3(sx, sy, sz):
    return np.array([[sx, 0, 0, 0],
                     [0, sy, 0, 0],
                     [0, 0, sz, 0],
                     [0, 0, 0, 1]], np.float32)


def rotate_axis(angle, axis):
    c = cos(radians(angle))
    s = sin(radians(angle))
    axis = axis.normalize()
    ux2 = axis.x * axis.x
    uy2 = axis.y * axis.y
    uz2 = axis.z * axis.z
    return np.array(
        [[c + (1 - c) * ux2, (1 - c) * axis.y * axis.x - s * axis.z, (1 - c) * axis.z * axis.x + s * axis.y, 0],
         [(1 - c) * axis.y * axis.x + s * axis.z, c + (1 - c) * uy2, (1 - c) * axis.z * axis.y - s * axis.x, 0],
         [(1 - c) * axis.x * axis.z - s * axis.y, (1 - c) * axis.y * axis.z + s * axis.x, c + (1 - c) * uz2, 0],
         [0, 0, 0, 1]], np.float32)


def translate(matrix, x, y, z):
    trans = translate_matrix(x, y, z)
    return matrix @ trans


def scale(matrix, s):
    sc = scale_matrix(s)
    return matrix @ sc


def scale3(matrix, x, y, z):
    sc = scale_matrix3(x, y, z)
    return matrix @ sc


def rotate(matrix, angle, axis, local=True):
    rot = rotate_axis(angle, axis)
    if local:
        return matrix @ rot
    else:
        return rot @ matrix


def perspective_mat(angle_of_view, aspect_ratio, near_plane, far_plane):
    a = radians(angle_of_view)
    d = 1.0 / tan(a / 2)
    r = aspect_ratio
    b = (far_plane + near_plane) / (near_plane - far_plane)
    c = far_plane * near_plane / (near_plane - far_plane)
    return np.array([
        [d / r, 0, 0, 0],
        [0, d, 0, 0],
        [0, 0, b, c],
        [0, 0, -1, 0]], np.float32)
