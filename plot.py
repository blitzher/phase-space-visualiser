"""
main class for the 

"""
from tools import *
from pygame import display, draw as pgdraw, image as pgimage
from pygame.rect import Rect as rect
import numpy as np

class plot:
    def __init__(self, x, y, axis = True, grid = True):

        self.lo_x, self.hi_x = x
        self.lo_y, self.hi_y = y

        self.screen = display.get_surface()

        self.axis = axis
        self.grid = grid
        self.dragging = False

    def show_axis(self):
        self.axis = True
    def hide_axis(self):
        self.axis = False

    def to_screen(self, *cords):
        """takes a world point (x,y) and translates it
        to screen coordinates, i.e. according to axis
        plot.to_screen(x, y)   -> (x, y)
        plot.to_screen((x, y)) -> (x, y)
        """
        x,y = cordinp(*cords)

        x = scale(x, self.lo_x, self.hi_x, 0, opts['sw'])
        y = scale(y, self.hi_y, self.lo_y, 0, opts['sh']) # invert y axis

        return np.array( (int(x),int(y)) )

    def to_world(self, *cords):
        """takes a screen point (x,y) and translates it
        to world coordinates, i.e. according to axis
        plot.to_world(x, y)   -> (x , y)
        plot.to_world((x, y)) -> (x , y)
        """
        x,y = cordinp(*cords)

        x = scale(x, 0, opts['sw'], self.lo_x, self.hi_x)
        y = scale(y, 0, opts['sh'], self.hi_y, self.lo_y) # invert y axis

        return np.array((x,y))

    def draw_axis(self):
        x_ax1 = self.to_screen(self.lo_x, 0)
        x_ax2 = self.to_screen(self.hi_x, 0)

        y_ax1 = self.to_screen(0, self.lo_y)
        y_ax2 = self.to_screen(0, self.hi_y)

        pgdraw.line(self.screen, clrs['black'], x_ax1, x_ax2)
        pgdraw.line(self.screen, clrs['black'], y_ax1, y_ax2)

    def draw_grid(self):
        pass

    def draw_func(self, fun, n = 20):
        line = [ self.to_screen(x, fun(x)) for x in np.linspace(self.lo_x, self.hi_x, num = n)]
        pgdraw.aalines(self.screen, clrs['black'], False, line)

    def draw_field(self, fun, n = 20):

        dx,dy = self.hi_x - self.lo_x, self.hi_y - self.lo_y

        vector_length = max(dx, dy) / (2*n)

        for x in np.linspace(self.lo_x, self.hi_x, num = n):
            for y in np.linspace(self.lo_y, self.hi_y, num = n):

                slope_vector = normalize( (1, fun(x,y)) )
                
                start_point = np.array((x, y))  - slope_vector * vector_length / 2
                end_point =   np.array((x, y))  + slope_vector * vector_length / 2

                pgdraw.line(self.screen, clrs['black'], self.to_screen(start_point), self.to_screen(end_point))

    def border(self):
        w = 15
        # draw beige borders
        pgdraw.rect(self.screen, clrs['beige'], rect((0,0), (w, opts['sh']) )   )             # left square
        pgdraw.rect(self.screen, clrs['beige'], rect((opts['sw']-w, 0), (w, opts['sh']) )   ) # right square

        pgdraw.rect(self.screen, clrs['beige'], rect((0, 0), (opts['sw'], w) )   )            # top square
        pgdraw.rect(self.screen, clrs['beige'], rect((0, opts['sh']-w), (opts['sw'], w) )   ) # bottom square

        # draw dark outline
        pgdraw.line(self.screen, clrs['dgrey'], (w, w), (w, opts['sh']-w))                       # left border
        pgdraw.line(self.screen, clrs['dgrey'], (opts['sw']-w, w), (opts['sw']-w, opts['sh']-w)) # right border

        pgdraw.line(self.screen, clrs['dgrey'], (w, w), (opts['sw']-w, w))                       # top border
        pgdraw.line(self.screen, clrs['dgrey'], (w, opts['sh']-w), (opts['sw']-w, opts['sh']-w)) # bottom border
        pass

    def handle(self, event):
        if event.type == 5 and event.button == 1:
            self.dragging = True
        if event.type == 6 and event.button == 1:
            self.dragging = False

        # if event.type == 5 and event.button == 5:
        #     self.lo_x -= 1
        #     self.hi_x += 1
        #     self.lo_y -= 1
        #     self.hi_x += 1
        # if event.type == 5 and event.button == 4:
        #     self.lo_x += 1
        #     self.hi_x -= 1
        #     self.lo_y += 1
        #     self.hi_x -= 1

        print(event)

        if self.dragging and hasattr(event, 'rel'):
            dx, dy = - np.array(event.rel) * 1 / 25
            if dx != 0:
                self.lo_x += dx
                self.hi_x += dx
            if dy != 0:
                self.lo_y -= dy
                self.hi_y -= dy
            


    def show(self):

        if self.axis:
            self.draw_axis()
        if self.grid:
            self.draw_grid()

    def save(self, filename = 'plot.png'):
        pgimage.save(self.screen, filename)

if __name__ == '__main__':
    from main import main
    main()