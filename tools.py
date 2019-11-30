""" helper tools and functions for plot.py """
import numpy as np

class Info:
    " helper class for storing info for easy access "
    def __init__(self, info):
        """ pass a dict, and access it's keys using
        _info.key
        """
        self.info = info
        for key in info:
            setattr(self, key, info[key])

    def __getitem__(self, key):
        return self.info[key]

    def add(self, key, val):
        " add an item to exisiting _info "
        self.info[key] = val
        setattr(self, key, val)


def _rnd(value):
    " round a number to the nearest integer "
    return int(round(value, 0))

def int_interp(a, b, amount):
    " interpolate a value between [a,b] by amount "
    dist = b-a
    return a + dist * amount

def flip(array):
    " flip the y value of an array "
    return np.array((array[0], -array[1]))


def scale(val, a, b, c, d):
    "scale a value from area [a,b] to [c,d]"
    if a == b:
        raise ValueError('cannot scale value from empty area')

    scaled = c + (d-c)/(b-a) * (val-a)
    return scaled

def _hex_to_rgb(hexs):
    hexv = (hexs[i*2:i*2+2] for i in range(int(len(hexs)/2)))
    rgb = (int('0x' + hx, 0) for hx in hexv)
    return tuple(rgb)


def floor(val):
    " round a value down to nearest integer, closer to 0"
    return int(val - (val % 1)) if int(val) != val else int(val)
def ceil(val):
    " round a value up to nearest integer, further from 0"
    return int(val - (val % 1) + 1) if int(val) != val else int(val)

def cordinp(*args):
    " unpacks cordinate input from tuple or seperate variables "
    if len(args) == 1:
        args = args[0]
    if len(args) != 2:
        raise TypeError("""
                cordinp takes 2 arguments or a tuple of 2 arguments,
                but recieved %s,%s""" % (args, len(args)))

    return args[0], args[1]


def _norm(array):
    " find the norm of an array "
    if not isinstance(array, np.array):
        array = np.array(array)
    return np.sqrt(np.sum(array ** 2))

def normalize(array):
    " normalize an array to have length 1 "
    if not isinstance(array, np.array):
        array = np.array(array)
    vector_length = _norm(array)
    return array / vector_length

opts = Info({  # global options
    'sh' : 720, # screen height
    'sw' : 1280, # screen width
    'bw' : 10,  # border width
    'aw' : 50   #  axis  width
})

# pylint: disable=bad-whitespace
clrs = Info({  # global colours
    'white' : [240, 240, 250],
    'dgrey' : [50 , 50 , 50 ],
    'lgrey' : [180, 180, 180],
    'black' : [0  , 0  , 0  ],
    'beige' : [245, 245, 220],
    'red'   : [255, 0  , 0  ],
    'green' : [0  , 255, 0  ],
    'blue'  : [0  , 0  , 255],
    'yellow': [255, 255, 0  ],
    'purple': [255, 0  , 255]
})
