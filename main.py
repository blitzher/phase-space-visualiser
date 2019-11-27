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
" y' = x + y "

def dfun(x,y):
    return x+y








def main():
    running = True
    pg.init()
    pg.display.set_mode((opts['sw'], opts['sh']))
    plt = plot( (-1, 1), (-1, 1) )

    while running:
        plt.screen.fill(clrs['white'])

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            plt.handle(event)

        plt.show()    
        plt.draw_field(dfun, n=10)

        for c in np.linspace(-4, 4, num = 9):
            plt.draw_func(lambda x: c*np.exp(x) - x - 1)

        plt.border()
        pg.display.flip()
    plt.save()

if __name__ == '__main__':
    main()
