import numpy as np


def _rnd(v):
    " round a number to the nearest integer "
    return int(round(v, 0))

def int_interp(a, b, amount):
    " interpolate a value between [a,b] by amount "
    dist = b-a
    return a + dist * amount

def scale(val, a,b, c,d):
    "scale a value from area [a,b] to [c,d]"
    # if value is above or below [a,b], set it it to the respective limit

    if a == b:
        raise ValueError('cannot scale value from empty area')

    scaled = c + (d-c)/(b-a) * (val-a)
    return scaled

def hex_to_rgb(hexs):
    assert len(hexs) == 6, "could not convert '%s' to rgb" % hexs
    hexv = (hexs[i*2:i*2+2] for i in range(int(len(hexs)/2)))
    rgb = ( int('0x' + hx, 0) for hx in hexv )
    return tuple(rgb)
    

def floor(val):
    return int(val - (val % 1)) if int(val) != val else int(val)
def ceil(val):
    return int(val - (val % 1) + 1) if int(val) != val else int(val)

def cordinp(*args):
    " unpacks cordinate input from tuple or seperate variables "
    if len(args) == 1:
        args = args[0]
    if len(args) != 2:
        raise TypeError("cordinp takes 2 arguments or a tuple of 2 arguments, but recieved %s,%s" % (args,len(args)))

    return args[0], args[1]


def _norm(array):
    " find the norm of an array "
    if type(array) != np.array:
        array = np.array(array)
    return np.sqrt(np.sum( array ** 2) )

def normalize(array):
    " normalize an array to have length 1 "
    if type(array) != np.array:
        array = np.array(array)
    vector_length = _norm(array)
    return array / vector_length

opts = {        # global options
    'sh' : 500, # screen height
    'sw' : 500, # screen width
    'bw' : 10   # border width
}

clrs = {        # colours used 
    'white' : [248, 248, 255],
    'dgrey' : [50 , 50 , 50 ],
    'lgrey' : [180, 180, 180],
    'black' : [0  , 0  , 0  ],
    'beige' : [245, 245, 220],
    'red'   : [255, 0  , 0  ],
    'green' : [0  , 255, 0  ],
    'blue'  : [0  , 0  , 255],
    'yellow': [255, 255, 0  ]
}