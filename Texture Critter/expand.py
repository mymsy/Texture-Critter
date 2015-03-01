'''A program for playing with texture expansion 

Author: mym
'''

from PIL import Image
import sys
import argparse

from texture import Texture

if __name__ == '__main__':
    # use the first line of the docstring as the program description
    parser = argparse.ArgumentParser(description = __doc__.splitlines()[0])
    
    # Minimum arguments - input (source) and output (expanded) filenames
    parser.add_argument("input_file", help="the source texture file")
    parser.add_argument("output_file", help="the destination file")
    
    # TODO gonna need to read some options
        # targeted synthesis w/ target file (default off)
        # gaussian weighting (default flat)
        # neighbourhood size (default ?)
        # randomisation method (default none)

    args = parser.parse_args()

    # Read the source image
    try:
        source_image = Image.open(args.input_file)
    except IOError:
        print "Could not open input file", args.input_file
        exit(1)
    
    # Create the texture expander
    tex = Texture(source_image)
    
    # Perform the expansion
    expansion = tex.expand()
    
    # Write the final image
    try:
        expansion.save(args.output_file)
    except IOError:
        print "Could not write output file", args.output_file
        exit(1)
        
    exit(0)
    