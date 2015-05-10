# Copyright 2015 Myriam Johnson
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''A program for playing with texture expansion. 

Author: mym
'''

from PIL import Image
from math import sqrt
import argparse

from texture import *

def compare(pix1, pix2):
    '''Compare two pixels, returning the colour-space distance between
    
    Arguments:
    pix1 -- tuple containing the channels of the first pixel
    pix2 -- tuple containing the channels of the second pixel
    
    Return: floating-point colour space distance
    
    Preconditions: both pixels have the same number of channels
    '''
    assert len(pix1) == len(pix2)
    collect = 0
    for pair in zip(pix1, pix2):
        collect += (pair[0] - pair[1])**2
    return sqrt(collect)

def expand(source, target, near):
    '''Expands the source texture into larger output
    
    Arguments:
    source -- Source Texture used to be expanded
    target -- Target Texture to guide expansion
    near -- Shape used for comparisons
    
    Return: an Image containing the expanded texture
    '''
    
    # make sure the target has the same mode as the source
    if (target.pic.mode != source.pic.mode):
        target.pic = target.pic.convert(source.pic.mode)
        
    # for i in source pixels, j in target pixels
    # truncate shape list according to _goodList for each
    # sum compares over each remaining in goodlist
    # push (sum/len(goodlist), source pixel) into a list
    # sort list, pick first

    # convert to an Image and return  
    return target.toImage()    

if __name__ == '__main__':
    # use the first line of the docstring as the program description
    parser = argparse.ArgumentParser(description = __doc__.splitlines()[0])
    
    # Minimum arguments - input (source) and output (expanded) filenames
    parser.add_argument("input_file", help="the source texture file")
    parser.add_argument("output_file", help="the destination file")
    
    # TODO gonna need to read some options
        # targeted synthesis default off (starting with it necessary)
        # gaussian weighting (default flat)
        # neighbourhood size (default ?)
        # randomisation method (default none)
    parser.add_argument("target_file", help="image for target of synthesis")

    args = parser.parse_args()

    # Read the source image
    try:
        source_image = Image.open(args.input_file)
    except IOError:
        print "Could not open input image file", args.input_file
        exit(1)
    
    # Read the target image
    try:
        target_image = Image.open(args.target_file)
    except IOError:
        print "Could not open target image file", args.target_file
        exit(1)
    
    # Create the texture expander
    source = Texture(source_image)
    target = Texture(target_image)
    shape = SquareShape(2)
    
    # Perform the expansion
    expansion = expand(source, target, shape)
    
    # Write the final image
    try:
        expansion.save(args.output_file)
    except IOError:
        print "Could not write output image file", args.output_file
        exit(1)
        
    exit(0)
    