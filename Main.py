import math
import random
import os
import time

from pygame import *
import pygame


WIDTH = 600
HEIGHT = 600
DISPLAY = (WIDTH, HEIGHT)
FPS = 30
RUNNING = True

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

POINT_RADIUS = 5

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption("Dude")
clock = pygame.time.Clock()
point_img = pygame.image.load(os.path.join(os.path.dirname(__file__), 'img/point.png')).convert()
centre_img = pygame.image.load(os.path.join(os.path.dirname(__file__), 'img/centre.png')).convert()

def massCenter(point_arr):
    x = y = m = 0
    for i in range(len(point_arr)):
        m += point_arr[i].mass
        x += point_arr[i].mass*(point_arr[i].rect.x+int(1.5*point_arr[i].mass/2))
        y += point_arr[i].mass*(point_arr[i].rect.y+int(1.5*point_arr[i].mass/2))
    x_mid = int(x/m)
    y_mid = int(y/m)
    coord = (x_mid, y_mid)
    return coord


class Point(pygame.sprite.Sprite):
    def __init__(self, x, y, mass):
        pygame.sprite.Sprite.__init__(self)
        self.mass = mass
        self.radius = int(1.5*mass)
        self.x = int(x)
        self.y = int(y)
        self.image = pygame.transform.scale(point_img, (self.radius, self.radius))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        speed_y = speed_x = int(0.7*self.mass)
        key_stat = pygame.key.get_pressed()
        if key_stat[pygame.K_LEFT]:
            self.rect.x -= speed_x
        if key_stat[pygame.K_RIGHT]:
            self.rect.x += speed_x
        if key_stat[pygame.K_UP]:
            self.rect.y -= speed_y
        if key_stat[pygame.K_DOWN]:
            self.rect.y += speed_y

    def showInfo(self, info):
        if info and self.x != -1:
            pygame.draw.rect(screen, (192, 192, 192), (self.rect.x+28, self.rect.y-2, 62, 34))
            pygame.draw.rect(screen, (105, 105, 105), (self.rect.x+30, self.rect.y, 58, 30))
            myfont = pygame.font.SysFont("calibri", 15)
            label = myfont.render("Mass: " + str(self.mass), 1, WHITE)
            screen.blit(label, (self.rect.x+33, self.rect.y+3))


class MassPoint(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(centre_img, (10, 10))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y


point_arr = []
#p1 = Point(100, 100, 5)
#p2 = Point(100, 70, 4)
#p3 = Point(20, 20, 40)
#p4 = Point(160, 120, 6)
for i in range(5):
    if i == 0:
        point_arr.append(Point(-1, -1, 0))
    point_arr.append(Point(300+30*i, 300-30*i, 5*0.7*i))

point_group = pygame.sprite.Group()

coord = massCenter(point_arr)
m1 = MassPoint()
mass_group = pygame.sprite.Group()
mass_group.add(m1)

x = y = 0
LEFT = 1
iterator = 0
infoterator = 0
info = False

while RUNNING:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for i in range(len(point_arr)):
                if x-point_arr[i].radius <= point_arr[i].rect.x <= x+point_arr[i].radius and y-point_arr[i].radius <= point_arr[i].rect.y <= y+point_arr[i].radius:
                    iterator = i
        elif event.type == pygame.MOUSEBUTTONUP:
            iterator = 0
        elif event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            point_arr[iterator].rect.x = x
            point_arr[iterator].rect.y = y
            for i in range(len(point_arr)):
                if x - point_arr[i].radius <= point_arr[i].rect.x <= x + point_arr[i].radius and y - point_arr[i].radius <= point_arr[i].rect.y <= y + point_arr[i].radius:
                    infoterator = i
                    info = True

    point_group.add(point_arr)
    point_group.update()
    coord = massCenter(point_arr)
    m1.update(coord[0], coord[1])
    screen.fill(BLACK)
    point_group.draw(screen)
    mass_group.draw(screen)
    point_arr[infoterator].showInfo(info)
    pygame.display.flip()

pygame.quit()