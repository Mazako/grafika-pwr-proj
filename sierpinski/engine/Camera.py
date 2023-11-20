import numpy as np
import pygame
from OpenGL.GLU import *
from math import *
from .Uniform import *
import glm

from ..utils.Translations import perspective_mat


class Camera:
    def __init__(self, program_id, w, h):
        self.eye = pygame.math.Vector3(0, 1, 5)
        self.up = pygame.math.Vector3(0, 1, 0)
        self.right = pygame.math.Vector3(1, 0, 0)
        self.forward = pygame.math.Vector3(0, 0, -1)
        self.look = self.eye + self.forward

        self.yaw = -90
        self.pitch = 0

        self.projection_mat = perspective_mat(60, w / h, 0.01, 1000000)
        self.projection = Uniform(program_id, 'mat4', self.projection_mat, 'projection_matrix')
        self.program_id = program_id
        self.screen_width = w
        self.screen_height = h
        self.mouse_sensitivity_x = 0.04
        self.mouse_sensitivity_y = 0.04
        self.key_sensitivity = 0.08
        self.last_mouse = (0, 0)


    def rotate(self, yaw, pitch):
        self.yaw += yaw
        self.pitch += pitch

        if self.pitch > 89.0:
            self.pitch = 89.0
        if self.pitch < -89.0:
            self.pitch = -89.0

        self.forward.x = cos(radians(self.yaw)) * cos(radians(self.pitch))
        self.forward.y = sin(radians(self.pitch))
        self.forward.z = sin(radians(self.yaw)) * cos(radians(self.pitch))
        self.forward = self.forward.normalize()
        self.right = self.forward.cross(pygame.Vector3(0, 1, 0)).normalize()
        self.up = self.right.cross(self.forward).normalize()

    def update(self):
        if pygame.mouse.get_visible():
            return
        mouse_pos = pygame.mouse.get_pos()
        mouse_change = self.last_mouse - pygame.math.Vector2(mouse_pos)
        pygame.mouse.set_pos(self.screen_width / 2, self.screen_height / 2)
        self.rotate(-mouse_change.x * self.mouse_sensitivity_x, mouse_change.y * self.mouse_sensitivity_y)
        self.last_mouse = pygame.mouse.get_pos()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            self.eye -= self.forward * self.key_sensitivity
        elif keys[pygame.K_w]:
            self.eye += self.forward * self.key_sensitivity
        elif keys[pygame.K_a]:
            self.eye -= self.right * self.key_sensitivity
        elif keys[pygame.K_d]:
            self.eye += self.right * self.key_sensitivity

        self.projection.load()
        self.look = self.eye + self.forward
        view = glm.lookAt(
            glm.vec3(self.eye.x, self.eye.y, self.eye.z),
            glm.vec3(self.look.x, self.look.y, self.look.z),
            glm.vec3(self.up.x, self.up.y, self.up.z)
        )
        view = np.array(view.to_tuple(), np.float32).transpose()
        look_at = Uniform(self.program_id,'mat4', view, 'camera_transformation')
        look_at.load()

