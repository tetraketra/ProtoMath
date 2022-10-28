from time import time, sleep
from math import log10, copysign, dist
import numpy as np
import mouse_input as mi

start_time = time()
fps = 24; period = 1 / fps
origin = np.array([0.0, 0.0])
r = 0.4; rubber = np.array([r, r])


class body():
    def __init__(self, mass, rubber, friction):
        self.pos = np.array([0.0, 0.0])
        self.vel = np.array([0.0, 0.0])
        self.mass = mass
        self.rubber = rubber
        self.friction = friction
        
    def update(self, bump_acc):
        global origin, gravity, period

        #1: create rubber-banding force, [dist from origin x,y]^rubber
        force = np.sign(self.pos) * np.abs(self.pos) ** self.rubber
        force = force / self.mass
        print(self.vel)

        #2a: update velocity with rubber-banding force
        #self.vel = np.subtract(self.vel, force * period)
        self.vel = np.subtract(self.vel, force * period)

        #2c: reduce velocity according to friction
        self.vel = self.vel * (1 - self.friction)
        
        #2c: update velocity with bumping force
        #self.vel = np.add(self.vel, bump_acc * period) #up for exactness
        self.vel = np.subtract(self.vel, bump_acc * period) #down for lagging behind real accel data

        #3: update position
        self.pos = np.add(self.pos, self.vel * period)

def func_with_sign(func, val):
    sign = copysign(1, val)
    return 0 if val == 0 else sign * func(abs(val))



#ONLY NEEDED FOR PYGAME IMPLEMENTATION#
import pygame
from pygame.locals import *
pygame.init()
window = pygame.display.set_mode((600, 600))
#ONLY NEEDED FOR PYGAME IMPLEMENTATION#



point = body(mass = 5, rubber = 2.7, friction = 0.14)

while True:
    #ONLY NEEDED FOR MOUSE ACCEL BUMP IMPLEMENTATION#
    mi.update_tracker(3)
    movement_data = mi.tracker
    scaled_acc = np.array([func_with_sign(log10, x) for x in movement_data["vel2"]]) * 500
    #ONLY NEEDED FOR MOUSE ACCEL BUMP IMPLEMENTATION#

    #Point gravity physics with damping for center of object.
    point.update(scaled_acc) 

    #ONLY NEEDED FOR PYGAME IMPLEMENTATION#
    pygame.event.get()
    image_canvas = pygame.image.load("canvas.png").convert_alpha()
    image_face = pygame.image.load("face.png").convert()
    window.blit(image_face, (point.pos[0], point.pos[1], 600, 600))
    window.blit(image_canvas, (0, 0, 600, 600))

    pygame.display.update()
    #ONLY NEEDED FOR PYGAME IMPLEMENTATION#

    #Sleep until next frame.
    sleep(period - ((time() - start_time) % period)) 

