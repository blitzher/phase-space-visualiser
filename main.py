import pygame as pg, numpy as np
import pygame
sh, sw = (500, 500)
white = (255, 255, 255)
black = (0, 0, 0)
pygame.draw.line
screen = pg.display.set_mode((sh, sw))
running = True
           
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
#                    $$u.u$"         dF dF      tony        
#                    $ """   o      dP xR                   
#                    $      dFNu...@"  $                    
#                    "N..   ?B ^"""   :R                    
#                      """"* RL       d>                    
#                              ^"*bo@"                     


pg.init()

def normalize(array):
    vector_length = np.linalg.norm(array)
    return array / vector_length
1
def axis(screen):
    pg.draw.line(screen, black, (0, sh/2), (sw, sh/2))
    pg.draw.line(screen, black, (sw/2, 0), (sw/2, sh))

" y = e^x -> y' = c*e^x - x - 1 "
" y' = x + y "

def dfun(x,y):
    return (y)*5/500


def draw_func(screen, fun):
    pass

def draw_field(screen, fun):
    n = 20
    for x in range(0, sw, int(sw/n)):
        for y in range(0, sh, int(sh/n)):

            vector_length = max(sw, sh)/(2*n)

            slope_vector = normalize((1, -fun(x-sw/2,-y+sw/2) ))

            start_point = np.array((x, y))  - slope_vector * vector_length / 2
            end_point =   np.array((x, y))  + slope_vector * vector_length / 2

            pg.draw.aaline(screen, black, start_point, end_point, 2)


while running:
    screen.fill(white)



    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    axis(screen)
    draw_field(screen, dfun)

    pg.display.flip()
    pass
