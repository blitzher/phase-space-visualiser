import pygame as pg, numpy as np
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





" y = e^x -> y' = c*e^x - x - 1 "


" y' = e^(x-y)"
def dfun(x,y):
    return x+y


def main():
    running = True
    pg.init()
    pg.display.set_mode((opts['sw'], opts['sh']))
    plt = plot( (-3, 3), (-3, 3) )

    while running:
        plt.screen.fill(clrs['white'])

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            plt.handle(event)

        plt.draw_field(dfun, n=30)
        plt.show()                  # draw axis and grid

        #plt.draw_func(lambda x: np.log(1+np.exp(x)))
        #plt.draw_case(dfun, x0=0, y0=-1, n=100)

        plt.border()
        pg.display.flip()
    plt.save()

if __name__ == '__main__':
    main()
