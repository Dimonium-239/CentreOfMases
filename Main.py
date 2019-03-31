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
        self.radius = int((1.5*mass))
        self.x = int(300+x)
        self.y = int(300+y)
        self.image = pygame.transform.scale(point_img, (self.radius, self.radius))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=(self.x, self.y))

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
        if info and self.x != 300:
            pygame.draw.rect(screen, (192, 192, 192), (self.rect.x+28, self.rect.y-2, 62, 34))
            pygame.draw.rect(screen, (105, 105, 105), (self.rect.x+30, self.rect.y, 58, 30))
            myfont = pygame.font.SysFont("calibri", 15)
            label = myfont.render("Mass: " + str(self.mass), 1, WHITE)
            labelx = myfont.render("X: " + str(self.rect.x-300+self.radius//2), 1, WHITE)
            labely = myfont.render("Y: " + str(self.rect.y-300+self.radius//2), 1, WHITE)
            screen.blit(label, (self.rect.x+33, self.rect.y+3))
            screen.blit(labelx, (self.rect.x+33, self.rect.y+12))
            screen.blit(labely, (self.rect.x+33, self.rect.y+21))


class MassPoint(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(centre_img, (10, 10))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 10

    def update(self, x, y):
        self.rect.x = x-5
        self.rect.y = y-5

    def showInfo(self, info):
        if info:
            pygame.draw.rect(screen, (192, 192, 192), (self.rect.x+28, self.rect.y-2, 62, 34))
            pygame.draw.rect(screen, (105, 105, 105), (self.rect.x+30, self.rect.y, 58, 30))
            myfont = pygame.font.SysFont("calibri", 15)
            labelx = myfont.render("X: " + str(self.rect.x-300+self.radius//2), 1, WHITE)
            labely = myfont.render("Y: " + str(self.rect.y-300+self.radius//2), 1, WHITE)
            screen.blit(labelx, (self.rect.x+33, self.rect.y+3))
            screen.blit(labely, (self.rect.x+33, self.rect.y+12))


def axis(surf):
    pygame.draw.line(surf, GREEN, [WIDTH-300, 0], [WIDTH-300, HEIGHT], 1)
    pygame.draw.line(surf, GREEN, [0, HEIGHT-300], [WIDTH, HEIGHT-300], 1)
    for i in range(0, WIDTH, 15):
        pygame.draw.line(surf, GREEN, [i, HEIGHT-297], [i, HEIGHT-303], 1)
        pygame.draw.line(surf, GREEN, [WIDTH-297, i], [WIDTH-303, i], 1)




point_arr = []
for i in range(6):
    if i == 0:
        point_arr.append(Point(0, 300, 0))
    point_arr.append(Point(10*i, 10*i, 10*i))

point_group = pygame.sprite.Group()

coord = massCenter(point_arr)
m1 = MassPoint()
mass_group = pygame.sprite.Group()
mass_group.add(m1)

x = y = 0
LEFT = 1
iterator = 0
infoterator = 0
massinfo = False
info = False

while RUNNING:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for i in range(len(point_arr)):
                if x-point_arr[i].radius <= point_arr[i].rect.x <= x and y-point_arr[i].radius <= point_arr[i].rect.y <= y:
                    iterator = i
        elif event.type == pygame.MOUSEBUTTONUP:
            iterator = 0
        elif event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            point_arr[iterator].rect.x = x-point_arr[iterator].radius/2
            point_arr[iterator].rect.y = y-point_arr[iterator].radius/2
            massinfo = False
            if x-m1.radius <= m1.rect.x <= x and y-m1.radius <= m1.rect.y <= y:
                massinfo = True
            for i in range(len(point_arr)):
                if x-point_arr[i].radius <= point_arr[i].rect.x <= x and y-point_arr[i].radius <= point_arr[i].rect.y <= y:
                    infoterator = i
                    info = True

    point_group.add(point_arr)
    point_group.update()
    coord = massCenter(point_arr)
    m1.update(coord[0], coord[1])
    screen.fill(BLACK)
    axis(screen)
    point_group.draw(screen)
    mass_group.draw(screen)
    m1.showInfo(massinfo)
    point_arr[infoterator].showInfo(info)
    pygame.display.flip()

pygame.quit()
