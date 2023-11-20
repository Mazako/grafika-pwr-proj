import os

import pygame
from pygame.constants import DOUBLEBUF, OPENGL, K_ESCAPE, KEYDOWN, K_SPACE

from sierpinski.engine.Camera import Camera
from sierpinski.pyramid.SierpinskiPyramidFactory import create
from sierpinski.utils.ProgramCompiler import *


class App:
    def __init__(self, screen_width, screen_height, screen_pos_x, screen_pos_y):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (screen_pos_x, screen_pos_y)
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        self.screen_width = screen_width
        self.screen_height = screen_height
        pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption('Sierpinski pyramid app')
        self.program_id = None
        self.fps = pygame.time.Clock()
        self.pyramid = None
        self.program_id = None
        self.camera = None

    def initialise_program(self):
        self.program_id = create_program('../shaders/vertex_shader.glsl', '../shaders/fragment_shader.glsl')
        self.camera = Camera(self.program_id, self.screen_width, self.screen_height)
        self.pyramid = create(self.program_id, GL_TRIANGLES, 4)
        glEnable(GL_DEPTH_TEST)

    def update(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.program_id)
        self.camera.update()
        self.pyramid.draw()

    def program_loop(self):
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        self.initialise_program()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.event.set_grab(True)
                        pygame.mouse.set_visible(False)
                    if event.key == K_SPACE:
                        pygame.event.set_grab(False)
                        pygame.mouse.set_visible(True)

            self.update()
            pygame.display.flip()
            self.fps.tick(60)
        pygame.quit()
