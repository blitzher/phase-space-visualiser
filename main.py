import pygame as pg
import math

sh, sw = (500, 500)
white = (255, 255, 255)
black = (0, 0, 0)

screen = pg.display.set_mode((sh, sw))
running = True

pg.init()

def axis(screen):
    pg.draw.line(screen, black, (0, sh/2), (sw, sh/2))
    pg.draw.line(screen, black, (sw/2, 0), (sw/2, sh))

" y = e^x -> y' = c*e^x - x - 1 "
" y' = x + y "

def dfun(x,y):
    return (x + y)*1/500

def field(screen, fun):
    n = 20
    for x in range(-250, 250, int(sw/n)):
        for y in range(-250, 250, int(sh/n)):
            slope = dfun(x,y) * 500/n

            end_point = int(x + 250 + 250/n), int(-y + 250 - slope)
            pg.draw.aaline(screen, black, (int(x+250),int(-y+250)), end_point)


while running:
    screen.fill(white)



    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    axis(screen)
    field(screen, dfun)

    pg.display.flip()
    pass
