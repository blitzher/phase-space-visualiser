import numpy as np


def _rnd(v):
    return int(round(v, 0))

def scale(val, a,b, c,d):
    "scale a value from area [a,b] to [c,d]"
    # if value is above or below [a,b], set it it to the respective limit

    if a == b:
        raise ValueError('cannot scale value from empty area')

    # if val < a: val = a
    # if val > b: val = b

    scaled = c + (d-c)/(b-a) * (val-a)
    return scaled

def cordinp(*args):
    if len(args) == 1:
        args = args[0]
    if len(args) != 2:
        raise TypeError("cordinp takes 2 arguments or a tuple of 2 arguments, but recieved %s,%s" % (args,len(args)))

    return args[0], args[1]


def _norm(array):
    if type(array) != np.array:
        array = np.array(array)
    return np.sqrt(np.sum( array ** 2) )

def normalize(array):
    if type(array) != np.array:
        array = np.array(array)
    vector_length = _norm(array)
    return array / vector_length

opts = {
    'sh' : 500,
    'sw' : 500
}

clrs = {
    'white' : [255, 255, 255],
    'dgrey' : [50 , 50 , 50 ],
    'black' : [0  , 0  , 0  ],
    'beige' : [245, 245, 220]
}