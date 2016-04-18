""" Computational Art """

import random
from PIL import Image
import math 
from math import pi
from random import randint

def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    The functions included in the lists of lambda functions below are:
        Base functions: f = x, y = x
        Parts (where x and y are functions that are build with recursion): 
        f = cos(pi*x), f = sin(pi*x), f = x*y, f = avg(x,y), f = = abs(x),
        f = abs(x)^abs(x)
    The if statements (which are not necessary structure-wise with 
    lambda functions) create variance in branch lengths.
    """
    depth = random.randint(min_depth, max_depth)            #the depth of the function is randomly chosen between the min/max depths


    base = [lambda x, y, t: x, lambda x, y, t: y, lambda x, y, t: t]              
    parts = [lambda x, y, t: math.cos(pi*x), lambda x, y, t: math.sin(pi*x), lambda x, y, t: x*y, lambda x, y, t: 0.5*(x + y), 
            lambda x, y, t: math.sin(0.5*pi*x), lambda x, y, t: abs(x), lambda x, y, t: abs(x), lambda x, y, t: math.sin(0.5*pi*y),
            lambda x, y, t: abs(x)**abs(y)]
    multi_part = [lambda x, y, t: x*y, lambda x, y, t: 0.5*(x + y), lambda x, y, t: abs(x)**(y)]
   
   #vary depth if multiple strands branch out
    if depth == 0:
    	function = random.choice(base)
    	return function
    else:
    	z = random.choice(parts)

        x = build_random_function(depth - 1, depth-1)
        y = build_random_function(max_depth-1, max_depth-1)
        function = lambda x,y,t : z(x,y,t) 
        return function
            


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.6, 0, 1, 0, 10)
        6.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    val = float(val)  #must be a float to work correctly
    scale = (val - (input_interval_start)) / (input_interval_end - input_interval_start)
    new = scale * (output_interval_end - output_interval_start) + output_interval_start
    return new
    


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(8,10)
    green_function = build_random_function(9,10)
    blue_function = build_random_function(8,10)

    # Create image and loop over all pixels
    t_index = 0
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for t in range(-10,10):
        for i in range(x_size):
            for j in range(y_size):
                x = remap_interval(i, 0, x_size, -1, 1)
                y = remap_interval(j, 0, y_size, -1, 1)
                pixels[i, j] = (
                        color_map(red_function(x,y,t/10)),
                        color_map(green_function(x,y,t/10)),
                        color_map(blue_function(x,y,t/10))
                        )
        im.save(filename%t_index)
        t_index += 1



if __name__ == '__main__':
    import doctest
    doctest.testmod()
    generate_art("myframe%03d.png")
  
"""To expand upon this code, I implemented lambda functions. I also tried adding time,
however, each of the images looks the same as the previous when the code is run. t does 
not seem to be impacting the outcome."""
