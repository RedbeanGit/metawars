# -*- coding: utf-8 -*-

import util

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"

import pygame
from pygame.locals import QUIT


class Display(object):
    def __init__(self):
        self.window = pygame.display.set_mode((500, 500))

    def load_images(self):
    	pass

    def update(self, level):
        self.window.fill((0, 0, 0))

        if level.texture:
        	self.window.blit(level.texture, (0, 0))

        pygame.display.update()

    def update_events(self):
    	for event in pygame.event.get():
    		if event.type == QUIT:
    			util.exit()