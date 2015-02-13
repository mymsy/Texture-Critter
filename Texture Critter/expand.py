'''
Created on Feb 3, 2015

@author: Mym
'''

from PIL import Image
import sys

if __name__ == '__main__':
    # Minimum arguments - input (source) and output (expanded) filenames
    if len(sys.argv) < 3:
        print "Usage:", sys.argv[0], "input output"

    infile = sys.argv[1]
    outfile = sys.argv[2]

    # TODO gonna need to read some options

    # Read the source image
    try:
        source_image = Image.open(infile)
    except IOError:
        print "Could not open input file", infile
        exit(0)
    
    # This is where stuff will happen
    expansion = source_image
    
    # Write the final image
    try:
        expansion.save(outfile)
    except IOError:
        print "Could not write output file", outfile
        exit(0)