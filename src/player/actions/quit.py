'''
Created on 2013-05-02

@author: brian
'''
import pygame
from pygame.locals import *


class Quit:

    def __init__(self, player):
        self.player = player
        self.quit = None
        self.finished = False
        self.player.log.append('Quit? (Y/N)')


    def nextStep(self):

        if(self.finished):
            if(self.quit):
                self.player.world.quit()
            else:
                return True
                

        e = pygame.event.poll()

        if(e is None):
            return False
    
        if e.type == KEYDOWN:
            
            if(e.key == K_y):
                self.quit = True
                self.finished = True
                return False
            elif(e.key == K_n):
                self.player.log.append('Pass')
                return True    