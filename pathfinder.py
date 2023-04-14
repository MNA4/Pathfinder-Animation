#Breadth-first Search Algorithm Implementation 

#imports
import pygame, math, sys, time, numpy
from pygame import gfxdraw
from pygame.locals import *

#functions
def expand(arr, path, screen, c = (200, 255, 255)):
    newpaths = ()
    if path[-1] == end:
        return True
    
    if path[-1][1] - 1 >= 0 and not arr[path[-1][0], path[-1][1] - 1]: #up
        newpaths += path + [(path[-1][0], path[-1][1] - 1)], 
    if path[-1][1] + 1 < arr.shape[1] and not arr[path[-1][0], path[-1][1] + 1]: #down
        newpaths += path + [(path[-1][0], path[-1][1] + 1)], 
    if path[-1][0] - 1 >= 0 and not arr[path[-1][0] - 1, path[-1][1]]: #left
        newpaths += path + [(path[-1][0] - 1, path[-1][1])], 
    if path[-1][0] + 1 < arr.shape[0] and not arr[path[-1][0] + 1, path[-1][1]]: #right
        newpaths += path + [(path[-1][0] + 1, path[-1][1])], 
        
    for p in newpaths:
        arr[p[-1]] = 2
        pygame.draw.rect(screen, c, (p[-1][0] * ZOOM, p[-1][1] * ZOOM, ZOOM, ZOOM))

    return newpaths


def lerp(a, b, t):
    return a + (b - a) * t

def lerp_color(color, color2, t):
    return [lerp(color[i], color2[i], t) for i in range(len(color))]

#constants
IMG = pygame.image.load('maze10.jpg')
ZOOM = 1
FPS = 500

# Render control
INSTENSITY = 1000
PATH_COLOR = (0, 255, 255, 200)
COLOR = (255,155,0)
COLOR2 = (200,0, 255)

WIDTH = IMG.get_width() * ZOOM
HEIGHT = IMG.get_height() * ZOOM
arr = []

#threshold image
arr2 = pygame.surfarray.array3d(IMG)
arr2 = arr2[..., 0]//3+arr2[..., 1]//3+arr2[..., 2]//3
arr = 1*(arr2<200)
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
firstrun = True

while 1:
    r = None
    start = None
    end = None
    for y in range(arr.shape[1]):
        for x in range(arr.shape[0]):
            currpos = (x * ZOOM, y * ZOOM, ZOOM, ZOOM)
            if arr[x,y] == 2:
                arr[x,y] = 0
                
            if arr[x,y] == 1:
                pygame.draw.rect(screen, (0, 0, 0), currpos)
                
            else:
                pygame.draw.rect(screen, (255, 255, 255), currpos)
    if firstrun:
        pygame.display.flip()
        pygame.display.set_caption('Select starting and ending point:')
        firstrun = False
    
    while end == None:
        e = pygame.event.wait()
        if e.type == pygame.MOUSEBUTTONDOWN:
            mousepos = e.pos[0] // ZOOM, e.pos[1] // ZOOM
            if arr[mousepos] == 0:
                if start == None:
                    start = mousepos
                    pygame.draw.circle(screen, (255, 255, 0), (start[0] * ZOOM + ZOOM / 2, start[1] * ZOOM + ZOOM / 2), 5)
                elif end == None:
                    end = mousepos
                    pygame.draw.circle(screen, (0, 255, 0), (end[0] * ZOOM + ZOOM / 2, end[1] * ZOOM + ZOOM / 2), 5)
                pygame.display.flip()
        elif e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
                
    paths = [[start], ]
    pygame.display.set_caption('Solving...')
    running = 1
    #main loop
    start_time = time.time()
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:                
                pygame.quit()
                sys.exit()
        
        newpaths = []
        for t in range(len(paths)):
            n = 1 - min(INSTENSITY / len(paths[t]), 1)
            l = expand(arr, paths[t], screen, lerp_color(COLOR, COLOR2, n))
            if l == True:
                r = paths[t]
                break
            newpaths += l
        paths = newpaths
        
        if r == None and len(paths) == 0:
            pygame.display.set_caption('Unable to find path...')
            running = False
            
        if r != None:
            end_time = time.time()
            print('time elapsed:', end_time - start_time, 'secs')
            pygame.display.set_caption('Solved!')
            for i in r:
                gfxdraw.box(screen, (i[0] * ZOOM-1, i[1] * ZOOM-1, ZOOM+1, ZOOM+1), PATH_COLOR)
                
            running = False
            
        pygame.draw.circle(screen, (255, 255, 0), (start[0] * ZOOM + ZOOM / 2, start[1] * ZOOM + ZOOM / 2), 5)
        pygame.draw.circle(screen, (0, 255, 0), (end[0] * ZOOM + ZOOM / 2, end[1] * ZOOM + ZOOM / 2), 5)
        pygame.display.flip()
        clock.tick(FPS)
pygame.quit()
