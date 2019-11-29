"""
main class for the 

"""
from tools import *
from pygame import display, draw as pgdraw, image as pgimage, font as pgfont
from pygame.rect import Rect as rect
import numpy as np

class plot:
    """ plot class for all your plotting needs, when it comes to first order DE's
    see help(plot.__init__) for more information
    """

    def __init__(self, x, y, axis = True, grid = True):
        """ initialise a plot object, with an
        x-range from x[0] to x[1] and a
        y-range from y[0] to y[1].

        optional arguments axis and grid to set wether or not
        the axis / grid should be shown by default.
        the attributes are free to be get or set.
        
        plot( (lower x, upper x), (lower y, upper y), axis = True, grid = True ) -> plot

        to show the axis, grid and legend, use
        plot.show()

        to show functions and DE phase space, use
        plot.draw_func( f(x) )
        plot.draw_field( y'(x,y) )

        """

        self.lo_x, self.hi_x = x
        self.lo_y, self.hi_y = y

        self.screen = display.get_surface()

        self.axis_font = pgfont.SysFont('Cambria', 15, True)

        self.axis = axis 
        self.grid = grid
        self.dragging = False

    def center_text(self, msg, pos, font, colour = 'black'):
        """ display a message to the screen, centered at pos
        pass colour from tools.clrs or rgb value
        
        plot.center_text( message, position, font, colour = 'black')
        """
        if colour in clrs: colour = clrs[colour]

        text_size = font.size(str(msg))
        text_centered = (pos[0] - text_size[0] / 2, pos[1] - text_size[1] / 2)
        self.screen.blit(font.render(str(msg), True, colour), text_centered)

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
        """ draw x and y axis, and keep them on screen always 
        with a distance of opts['aw']

        plot.draw_axis() -> None
        """

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

        x_ax1 = limit(x_ax1, (None, opts['aw']),              lambda x,y: x < y)
        x_ax1 = limit(x_ax1, (None, opts['sh'] - opts['aw']), lambda x,y: x > y)
        x_ax2 = limit(x_ax2, (None, opts['aw']),              lambda x,y: x < y)
        x_ax2 = limit(x_ax2, (None, opts['sh'] - opts['aw']), lambda x,y: x > y)

        y_ax1 = self.to_screen(0, self.lo_y)
        y_ax2 = self.to_screen(0, self.hi_y)

        y_ax1 = limit(y_ax1, (opts['aw'], None),              lambda x,y: x < y)
        y_ax1 = limit(y_ax1, (opts['sh'] - opts['aw'], None), lambda x,y: x > y)
        y_ax2 = limit(y_ax2, (opts['aw'], None),              lambda x,y: x < y)
        y_ax2 = limit(y_ax2, (opts['sh'] - opts['aw'], None), lambda x,y: x > y)

        for x in range(floor(self.lo_x), ceil(self.hi_x)):
            pos = self.to_screen(x, 0)

            pos = limit(pos, (None, opts['aw']),              lambda x,y: x < y)
            pos = limit(pos, (None, opts['sh'] - opts['aw']), lambda x,y: x > y)

            pos1, pos2 = (pos - np.array((0, 10))), (pos + np.array((0,10)))

            pgdraw.line(self.screen, clrs['black'], pos1, pos2)
            self.center_text(x, pos + np.array((10, -10)), self.axis_font)
        
        for y in range(floor(self.lo_y), ceil(self.hi_y)):
            pos = self.to_screen(0, y)

            pos = limit(pos, (opts['aw'], None),              lambda x,y: x < y)
            pos = limit(pos, (opts['sh'] - opts['aw'], None), lambda x,y: x > y)

            pos1, pos2 = (pos - np.array((10, 0))), (pos + np.array((10, 0)))

            pgdraw.line(self.screen, clrs['black'], pos1, pos2)
            self.center_text(y, pos + np.array((10, -10)), self.axis_font)

        pgdraw.line(self.screen, clrs['black'], x_ax1, x_ax2)
        pgdraw.line(self.screen, clrs['black'], y_ax1, y_ax2)

    def draw_grid(self):
        """ draw a grid at each integer x and y value """
        for x in range(floor(self.lo_x), ceil(self.hi_x)):
            bot, top = (x, self.lo_y), (x, self.hi_y)
            pgdraw.line(self.screen, clrs['lgrey'], self.to_screen(bot), self.to_screen(top))

        for y in range(floor(self.lo_y), ceil(self.hi_y)):
            lft, rgt = (self.lo_x, y), (self.hi_x, y)
            #print(lft, rgt)
            pgdraw.line(self.screen, clrs['lgrey'], self.to_screen(lft), self.to_screen(rgt))

    def draw_case(self, df, x0=0, y0=0, n = 20, colour = 'red'):
        """ draw a line from a starting position, with n line segments
        pass colour from tools.clrs or rgb value

        plot.draw_case( y'(x, y), x0 = 0, y0 = 0, n = 20, colour = 'red' ) -> None
        """
        assert type(df) == type(lambda x: None), " must pass a function as df argument!"

        if colour in clrs: colour = clrs[colour] # see if passed colour is in clrs

        def case(x): # generate an approximating function
            xs = []
            ys = []

            xspace = np.linspace(x0, x, num = n)
            h = xspace[1]-xspace[0] # step size

            for c,dx in enumerate(xspace):
                if c == 0:                    # assume starting position
                    xs.append(x0)
                    ys.append(y0)
                    continue

                xs.append(dx)
                dy = df(xs[c-1], ys[c-1]) * h # follow slope
                ys.append(ys[c-1] + dy)       # to get new y 
            return ys[-1]
        
        line = [ self.to_screen(x, case(x)) for x in np.linspace(self.lo_x, self.hi_x, num = n)]
        pgdraw.aalines(self.screen, colour, False, line)

    def draw_func(self, fun, n = 20, colour = 'blue'):
        """ draw an arbitrary function with n line segments
        pass colour from tools.clrs or rgb value

        plot.draw_func( f(x), n = 20, colour = 'blue' ) -> None
        
        """
        if colour in clrs: colour = clrs[colour]

        line = [ self.to_screen(x, fun(x)) for x in np.linspace(self.lo_x, self.hi_x, num = n)]
        pgdraw.aalines(self.screen, colour, False, line)

    def draw_field(self, df, n = 20, colour = 'black'):
        """ draw the vector field for an arbitrary first order
        differential equation.
        pass colour from tools.clrs or rgb value
        
        plot.draw_field( y'(x,y), n = 20, colour = 'black' ) -> None
        """

        if colour in clrs: colour = clrs[colour]

        dx,dy = self.hi_x - self.lo_x, self.hi_y - self.lo_y

        vector_length = max(dx, dy) / (2*n)

        for x in np.linspace(self.lo_x, self.hi_x, num = n):
            for y in np.linspace(self.lo_y, self.hi_y, num = n):

                slope_vector = normalize( (1, df(x,y)) )
                
                start_point = np.array((x, y))  - slope_vector * vector_length / 2
                end_point =   np.array((x, y))  + slope_vector * vector_length / 2

                pgdraw.line(self.screen, colour, self.to_screen(start_point), self.to_screen(end_point))

    def border(self, w = opts['bw'], clr1 = 'beige', clr2 = 'dgrey'):
        """ draw the border of the window
        pass clr1 from tools.clrs or rgb value for rectangle colour
        pass clr2 from tools.clrs or rgb value for line colour
        
        plot.border( w = opts['bw'], clr1 = 'beige', clr2 = 'dgrey' ) -> None
        """

        if clr1 in clrs: clr1 = clrs[clr1]
        if clr2 in clrs: clr2 = clrs[clr2]

        # draw beige borders
        pgdraw.rect(self.screen, clr1, rect((0,0), (w, opts['sh']) )   )                # left square
        pgdraw.rect(self.screen, clr1, rect((opts['sw']-w, 0), (w, opts['sh']) )   )    # right square

        pgdraw.rect(self.screen, clr1, rect((0, 0), (opts['sw'], w) )   )               # top square
        pgdraw.rect(self.screen, clr1, rect((0, opts['sh']-w), (opts['sw'], w) )   )    # bottom square

        # draw dark outline
        pgdraw.line(self.screen, clr2, (w, w), (w, opts['sh']-w))                       # left border
        pgdraw.line(self.screen, clr2, (opts['sw']-w, w), (opts['sw']-w, opts['sh']-w)) # right border

        pgdraw.line(self.screen, clr2, (w, w), (opts['sw']-w, w))                       # top border
        pgdraw.line(self.screen, clr2, (w, opts['sh']-w), (opts['sw']-w, opts['sh']-w)) # bottom border
        pass

    def handle(self, event):
        """ pygame implementation of event handling 
        to be called every frame, with passed pygame.event.get()

        for event in pygame.event.get():
            plot.handle(event) -> None
        """
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
            dx, dy = - np.array(event.rel) * 1 / 25 # TODO: find a better way to figure out the distance of drag
            if dx != 0:
                self.lo_x += dx
                self.hi_x += dx
            if dy != 0:
                self.lo_y -= dy
                self.hi_y -= dy

    def show(self):
        """ show all of the pure plot objects
        including grid and axis, and upcoming legend

        plot.show() -> None
        """

        if self.grid:
            self.draw_grid()
        if self.axis:
            self.draw_axis()

    def save(self, filename = 'plot.png'):
        """ save an image of the plot using pygame.image.save
        
        plot.save( filename = 'plot.png' ) -> None
        """
        pgimage.save(self.screen, filename)

if __name__ == '__main__':
    from main import main
    main()