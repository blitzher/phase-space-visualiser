"""
main class for the 

"""
from tools import *
from pygame import display, draw as pgdraw, image as pgimage, font as pgfont
from pygame.rect import Rect as rect
import numpy as np

class plot:
    def __init__(self, x, y, axis = True, grid = True):

        self.lo_x, self.hi_x = x
        self.lo_y, self.hi_y = y

        self.screen = display.get_surface()

        self.axis_font = pgfont.SysFont('Cambria', 15, True)

        self.axis = axis
        self.grid = grid
        self.dragging = False

    def show_axis(self):
        self.axis = True
    def hide_axis(self):
        self.axis = False

    def center_text(self, msg, pos, font, colour = 'black'):
        " display a message to the screen, centered at pos "
        text_size = font.size(str(msg))
        text_centered = (pos[0] - text_size[0] / 2, pos[1] - text_size[1] / 2)
        self.screen.blit(font.render(str(msg), True, clrs[colour]), text_centered)

    def to_screen(self, *cords):
        """takes a world point (x,y) and translates it
        to screen coordinates, i.e. according to axis
        plot.to_screen(x, y)   -> (x, y)
        plot.to_screen((x, y)) -> (x, y)
        """
        x,y = cordinp(*cords)

        x = scale(x, self.lo_x, self.hi_x, opts['bw'], opts['sw'] - opts['bw'])
        y = scale(y, self.hi_y, self.lo_y, opts['bw'], opts['sh'] - opts['bw']) # invert y axis

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

        def limit(ar1, ar2, func):
            " limit the values of ar1 by values of ar2 by func "
            assert len(ar1) == len(ar2), " cannot limit arrays of different sizes"
            for c in range(len(ar1)):
                if not ar2[c]: continue
                if func(ar1[c], ar2[c]):
                    ar1[c] = ar2[c]
            return ar1


        x_ax1 = self.to_screen(self.lo_x, 0)
        x_ax2 = self.to_screen(self.hi_x, 0)

        x_ax1 = limit(x_ax1, (None, 50),              lambda x,y: x < y)
        x_ax1 = limit(x_ax1, (None, opts['sh'] - 50), lambda x,y: x > y)
        x_ax2 = limit(x_ax2, (None, 50),              lambda x,y: x < y)
        x_ax2 = limit(x_ax2, (None, opts['sh'] - 50), lambda x,y: x > y)

        y_ax1 = self.to_screen(0, self.lo_y)
        y_ax2 = self.to_screen(0, self.hi_y)

        y_ax1 = limit(y_ax1, (50, None),              lambda x,y: x < y)
        y_ax1 = limit(y_ax1, (opts['sh'] - 50, None), lambda x,y: x > y)
        y_ax2 = limit(y_ax2, (50, None),              lambda x,y: x < y)
        y_ax2 = limit(y_ax2, (opts['sh'] - 50, None), lambda x,y: x > y)

        for x in range(floor(self.lo_x), ceil(self.hi_x)):
            pos = self.to_screen(x, 0)

            pos = limit(pos, (None, 50),              lambda x,y: x < y)
            pos = limit(pos, (None, opts['sh'] - 50), lambda x,y: x > y)

            pos1, pos2 = (pos - np.array((0, 10))), (pos + np.array((0,10)))

            pgdraw.line(self.screen, clrs['black'], pos1, pos2)
            self.center_text(x, pos + np.array((10, -10)), self.axis_font)
        
        for y in range(floor(self.lo_y), ceil(self.hi_y)):
            pos = self.to_screen(0, y)

            pos = limit(pos, (50, None),              lambda x,y: x < y)
            pos = limit(pos, (opts['sh'] - 50, None), lambda x,y: x > y)

            pos1, pos2 = (pos - np.array((10, 0))), (pos + np.array((10, 0)))

            pgdraw.line(self.screen, clrs['black'], pos1, pos2)
            self.center_text(y, pos + np.array((10, -10)), self.axis_font)

        pgdraw.line(self.screen, clrs['black'], x_ax1, x_ax2)
        pgdraw.line(self.screen, clrs['black'], y_ax1, y_ax2)

    def draw_grid(self):
        for x in range(floor(self.lo_x), ceil(self.hi_x)):
            bot, top = (x, self.lo_y), (x, self.hi_y)
            pgdraw.line(self.screen, clrs['lgrey'], self.to_screen(bot), self.to_screen(top))

        for y in range(floor(self.lo_y), ceil(self.hi_y)):
            lft, rgt = (self.lo_x, y), (self.hi_x, y)
            #print(lft, rgt)
            pgdraw.line(self.screen, clrs['lgrey'], self.to_screen(lft), self.to_screen(rgt))

    def draw_case(self, df, x0=0, y0=0, n = 20):

        def case(x):
            xs = []
            ys = []

            xspace = np.linspace(x0, x, num = n)
            h = xspace[1]-xspace[0]

            for c,dx in enumerate(np.linspace(x0, x, num = n)):
                if c == 0:
                    xs.append(x0)
                    ys.append(y0)
                    continue

                xs.append(dx)
                dy = ys[c-1] + df(xs[c-1], ys[c-1]) * h
                ys.append(dy)
            return ys[-1]


        #case = lambda x: y0 + sum(( df(np.linspace(x0, x, num = n), np.linspace(y0, x, num=n)) ) )
        line = [ self.to_screen(x, case(x)) for x in np.linspace(self.lo_x, self.hi_x, num = n)]
        pgdraw.aalines(self.screen, clrs['red'], False, line)


    def draw_func(self, fun, n = 20):
        line = [ self.to_screen(x, fun(x)) for x in np.linspace(self.lo_x, self.hi_x, num = n)]
        pgdraw.aalines(self.screen, clrs['blue'], False, line)

    def draw_field(self, fun, n = 20):

        dx,dy = self.hi_x - self.lo_x, self.hi_y - self.lo_y

        vector_length = max(dx, dy) / (2*n)

        for x in np.linspace(self.lo_x, self.hi_x, num = n):
            for y in np.linspace(self.lo_y, self.hi_y, num = n):

                slope_vector = normalize( (1, fun(x,y)) )
                
                start_point = np.array((x, y))  - slope_vector * vector_length / 2
                end_point =   np.array((x, y))  + slope_vector * vector_length / 2

                pgdraw.line(self.screen, clrs['black'], self.to_screen(start_point), self.to_screen(end_point))

    def border(self, w = opts['bw']):
        # draw beige borders
        pgdraw.rect(self.screen, clrs['beige'], rect((0,0), (w, opts['sh']) )   )                # left square
        pgdraw.rect(self.screen, clrs['beige'], rect((opts['sw']-w, 0), (w, opts['sh']) )   )    # right square

        pgdraw.rect(self.screen, clrs['beige'], rect((0, 0), (opts['sw'], w) )   )               # top square
        pgdraw.rect(self.screen, clrs['beige'], rect((0, opts['sh']-w), (opts['sw'], w) )   )    # bottom square

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

        if event.type == 5 and event.button == 5:
            self.lo_x = int_interp(self.lo_x, self.hi_x, -.25)
            self.hi_x = int_interp(self.lo_x, self.hi_x, 1.25)
            self.lo_y = int_interp(self.lo_y, self.hi_y, -.25)
            self.hi_x = int_interp(self.lo_y, self.hi_y, 1.25)
        if event.type == 5 and event.button == 4:
            self.lo_x = int_interp(self.lo_x, self.hi_x,  .25)
            self.hi_x = int_interp(self.lo_x, self.hi_x,  .75)
            self.lo_y = int_interp(self.lo_y, self.hi_y,  .25)
            self.hi_x = int_interp(self.lo_y, self.hi_y,  .75)

        if self.dragging and hasattr(event, 'rel'):
            dx, dy = - np.array(event.rel) * 1 / 25
            if dx != 0:
                self.lo_x += dx
                self.hi_x += dx
            if dy != 0:
                self.lo_y -= dy
                self.hi_y -= dy
            


    def show(self):

        if self.grid:
            self.draw_grid()
        if self.axis:
            self.draw_axis()

    def save(self, filename = 'plot.png'):
        pgimage.save(self.screen, filename)

if __name__ == '__main__':
    from main import main
    main()