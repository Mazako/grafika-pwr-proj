import pygame.image
from OpenGL.GL import *


class Texture:
    def __init__(self, filename):
        self.texture_id = glGenTextures(1)
        self.surface = pygame.image.load(filename)
        self.load()

    def load(self):
        w = self.surface.get_width()
        h = self.surface.get_height()

        pixel = pygame.image.tostring(self.surface, 'RGBA', 1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixel)
        glGenerateMipmap(GL_TEXTURE_2D)
