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

Methods:
compare -- find (square of) colour-space distance between two pixels
compareRegion -- find weighted sum of colour-space distances between all
    pixels in two texture regions
expand -- expand one texture into another

Author: mym
'''

from __future__ import print_function
#from math import sqrt
import texture
#import random

def compare(pix1, pix2):
    '''Compare two pixels, returning square of the colour-space distance between
    
    Arguments:
    pix1 -- tuple containing the channels of the first pixel
    pix2 -- tuple containing the channels of the second pixel
    
    Return: square of colour space distance
    
    Preconditions: both pixels have the same number of channels
    '''
    assert len(pix1) == len(pix2)
    collect = 0
    for i in xrange(len(pix1)):
        collect += (pix1[i] - pix2[i])**2
    return collect

def compare3(pix1, pix2):
    '''Compare two 3-bit pixels, returning square of the colour-space distance between
    
    Arguments:
    pix1 -- 3-tuple containing the channels of the first pixel
    pix2 -- 3-tuple containing the channels of the second pixel
    
    Return: square of colour space distance
    '''
    return ((pix1[0] - pix2[0])**2 + (pix1[1] - pix2[1])**2 
            + (pix1[2] - pix2[2])**2) 

def compare4(pix1, pix2):
    '''Compare two 4-bit pixels, returning square of the colour-space distance between
    
    Arguments:
    pix1 -- 4-tuple containing the channels of the first pixel
    pix2 -- 4-tuple containing the channels of the second pixel
    
    Return: square of colour space distance
    '''
    return ((pix1[0] - pix2[0])**2 + (pix1[1] - pix2[1])**2 
            + (pix1[2] - pix2[2])**2 + (pix1[3] - pix2[3])**2) 

def compareRegion(tex1, tex2, cen1, cen2, region, comp):
    '''Compare regions of two Textures.
    Returns the weighted sum of colour-space distances between corresponding
    pixels, or Infinity if no pixels can be compared.
    
    Arguments:
    tex1, tex2 -- Textures to compare
    cen1, cen2 -- 2-tuple centres of comparison regions
    region -- list of 2-tuple shifts defining points for comparison
    comp -- pixel comparison function
    
    Returns: floating-point weighted sum of distances
    
    Preconditions: region is valid about cen in both textures (untested)
    '''
    # abort if nothing to compare (avoid divide-by-zero)
    if (len(region) == 0): return float('inf')
    
    # loop over shifts
    total = 0
    for shift in region:
        p1 = tex1.getPixel(cen1, shift)
        p2 = tex2.getPixel(cen2, shift)
        total += comp(p1, p2)
    
    # weight by number of points compared
    return float(total)/len(region)

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
        
    # choose appropriate pixel comparison function
    if (source.bpp == 3):
        comp = compare3
    elif (source.bpp == 4):
        comp = compare4
    else:
        comp = compare
            
    # lists of all pixels in source, target for flatter iteration
    slist = [(x,y) 
             for y in xrange(source.pic.size[1])
             for x in xrange(source.pic.size[0])]
    tlist = [(x,y)
             for y in xrange(target.pic.size[1])
             for x in xrange(target.pic.size[0])]

    # dereference to local outside the loop, for speed
    spoints = source.pic.size[0] * source.pic.size[1]
    targetGoodList = target.goodList
    sourceGoodList = source.goodList
    sourceGetPixel = source.getPixel

    # for each target pixel...    
    for tloc in tlist:
        # trim neighbourhood around this point
        nearer = targetGoodList(tloc, near.shift, target.valid)
        
        # clear list of choices
        # faster to preallocate than to use appends
        choices = [None] * spoints
        ci = 0
        
        # loop over all source pixels
        for sloc in slist:
            # trim above neighbourhood around this point
            nearest = sourceGoodList(sloc, nearer, source.valid)

            # weighted texture distance of remaning region
            weight = compareRegion(source, target, sloc, tloc, nearest, comp)
            
            # add tuple of weight and source pixel to choices
            choices[ci] = (weight, sourceGetPixel(sloc))
            ci += 1
            
        # pick minimum from the list
        # TODO this gives lexical sort; want stable sort on only first element
        # actually stable gives preference to input order, 
        # lexical gives preference to colour in RGB order
        # what order is actually desired? (probably random) 
        # TODO weighted random choice
        # sorting actually unnecessary, even for randomness
        newval = min(choices)[1]
        
        # set the pixel!
        target.setPixel(newval, tloc)
        target.setValid(tloc)
        
        # progress?
        if (tloc[0] == 0): print("\nrow ", tloc[1], end = "")
        print(".", end = "")
        
    # convert to an Image and return  
    return target.toImage()    

if __name__ == '__main__':
    # additional imports
    import argparse
    from PIL import Image

    # use the first line of the docstring as the program description
    parser = argparse.ArgumentParser(description = __doc__.splitlines()[0])
    
    # Minimum arguments - input (source) and output (expanded) filenames
    parser.add_argument("input_file", help="the source texture file")
    parser.add_argument("output_file", help="the destination file")
    
    # TODO gonna need to read some options
        # gaussian weighting (default flat)
        # randomisation method (default none)
        
    # targeted synthesis
    parser.add_argument("-target", dest="target_file", 
                        help="image for target of synthesis")
    # untargeted synthesis scale
    parser.add_argument("-scale", default = 2, type = int,
                        help="Scale factor for generated texture (ignored if targeted)")
    # neighbourhood size
    parser.add_argument("-nsize", default = 2, type = int,
                        help = "Size of neighbourhood used in comparisons")
    # activate profiler
    parser.add_argument("-prof", metavar = "filename", 
                        help = "run profiler and save results")

    args = parser.parse_args()

    # Read the source image
    try:
        source_image = Image.open(args.input_file)
        source = texture.Texture(source_image)
    except IOError:
        print("Could not open input image file", args.input_file)
        exit(1)
    
    # Create target image and neighbourhood
    # SquareShape for targeted (looks ahead), 
    # EllShape for untargeted (only looks at initialised)
    if (args.target_file != None):
        # read from file if one is specified
        try:
            target_image = Image.open(args.target_file)
            target = texture.Texture(target_image)
            shape = texture.SquareShape(args.nsize)
        except IOError:
            print("Could not open target image file", args.target_file)
            exit(1)
    else:
        # no target specified, create a blank one
        tsize = (args.scale * source_image.size[0],
                 args.scale * source_image.size[1])
        target = texture.EmptyTexture(tsize, source_image.mode)
        shape = texture.EllShape(args.nsize)
            
    # Perform the expansion
    if (args.prof == None):
        expansion = expand(source, target, shape)
    else:
        import cProfile
        cProfile.run("expansion = expand(source, target, shape)", args.prof)
    
    # Write the final image
    try:
        expansion.save(args.output_file)
    except IOError:
        print("Could not write output image file", args.output_file)
        exit(1)
        
    exit(0)
    