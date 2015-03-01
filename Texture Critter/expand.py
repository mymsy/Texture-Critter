'''
Created on Feb 3, 2015

@author: Mym
'''

from PIL import Image
import sys
import argparse

if __name__ == '__main__':
    # Minimum arguments - input (source) and output (expanded) filenames
    parser = argparse.ArgumentParser()
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
    
    # This is where stuff will happen
    expansion = source_image
    
    # Write the final image
    try:
        expansion.save(args.output_file)
    except IOError:
        print "Could not write output file", args.output_file
        exit(1)
        
    exit(0)
    