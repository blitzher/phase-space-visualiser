" main module "
from time import time as ctime
import pygame as pg
import numpy as np
from tools import opts, clrs
from plot import plot

#                   ..      .........   .u*"^" "^Rc
#                 oP""*Lo*#"""""""""""7d" .d*N.    $
#                @  u@""           .u*" o*"   #L    ?b
#              8  ^"                    £w*@me€      '"Nu
#           .P                                          $r
#         .@"                                  $L       $
#    .d#"                                  .dP d"   .d#
#   xP              .e                 .ud#"  dE.o@"(
#   $             s*"              .u@*""     '""\dP"
#   ?L  ..                    ..o@""        .$  uP
#    #c:$"*u.             .u@*""$          uR .@"
#     ?L$. '"""***Nc    x@""   @"         d" JP
#       @'          "b.'$.   @"         $" 8"
#                    @L    $"         d" 8\
#                    $$u.u$"         dF dF
#                    $ """   o      dP xR
#                    $      dFNu...@"  $
#                    "N..   ?B ^"""   :R        tony
#                      """"* RL       d>
#                              ^"*bo@"





# y = e^x -> y' = c*e^x - x - 1 "
# y' = e^(x-y)"

def dfun(x, y):
    " differential equation to be graphed "
    return np.cos(x) * np.sin(x) + 0*y

def fps(plt, last, curr):
    " draw the current frames per second to the screen "
    pos = opts.bw/2 + 40, opts.bw / 2
    msg = "FPS: %.2f" % (1/(curr - last))
    plt.center_text(msg, pos, plt.axis_font)

def main():
    " main function "
    running = True
    last = ctime()
    pg.init()
    pg.display.set_mode((opts['sw'], opts['sh']))
    plt = plot((-3, 3), (-3, 3))

    while running:
        plt.screen.fill(clrs['white'])

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            plt.handle(event)

        #plt.draw_field(dfun, n=30)
        plt.show()  # draw axis and grid

        plt.draw_func(lambda x: x**2 + 1, n=100)
        plt.draw_case(dfun, x0=0, y0=0, n=100)

        plt.border()
        fps(plt, last, ctime())
        last = ctime()
        pg.display.flip()
    plt.save()

if __name__ == '__main__':
    main()
