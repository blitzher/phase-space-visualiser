" main module "
import pygame as pg
from tools import opts, clrs
from plot import plot


#                   ..      .........   .u*"^" "^Rc
#                 oP""*Lo*#"""""""""""7d" .d*N.    $
#                @  u@""           .u*" o*"   #L    ?b
#             .8  ^"                    £w*@me€      '"Nu
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


def dfun(x, y):
    " differential equation to be graphed "
    return y*(1-y)+0*x

def fps(plt, last, curr):
    " draw the current frames per second to the screen "
    pos = opts.bw/2 + 40, opts.bw / 2
    msg = "FPS: %.2f" % (1/(curr - last))
    plt.center_text(msg, pos, plt.axis_font)

def main():
    " main function "
    running = True
    pg.init()
    pg.display.set_mode((opts['sw'], opts['sh']))
    plt = plot((-10, 10), (-0.5, 1.6))

    plt.grid = False

    while running:
        plt.screen.fill(clrs['white'])

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            plt.handle(event)

        plt.show(x_axis=False)  # draw axis and grid

        plt.draw_pline(dfun, x=1, n = 5)

        plt.border()
        pg.display.flip()
    plt.save()

if __name__ == '__main__':
    main()
