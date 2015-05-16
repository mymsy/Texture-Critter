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

'''Texture synthesis helper classes

class Texture -- provides functions for working with a base PIL.Image
class EmptyTexture (subclasses Texture) -- a Texture variation that starts
    empty, with all pixels marked as uninitialised

class Shape -- generic base class to define the sampling shape for texture 
    region comparison
class SquareShape (subclasses Shape) -- defines a square Shape of given radius
class EllShape (subclasses Shape) -- defines an L-shaped Shape (rows above
    and columns to the left on the same row) of given radius
'''

from PIL import Image
import itertools

class Texture:
    '''A texture synthesis object
    
    Methods:
    goodList -- filter a list of shifts about a point to only those within the
        Texture
    getPixel -- get the pixel at a given location
    setPixel -- set the pixel at given location to given value
    setValid -- set the pixel at given location as valid
    toImage -- output this Texture as an Image
    
    Class variables:
    alpha_modes -- image modes implementing transparency
    pic -- the source image for expansion, converted to RGB(A) palette
    bpp -- number of bits used for each pixel, 3 or 4
    pixels -- list of bpp-tuple pixels
    valid -- list of booleans giving whether a pixel is considered initialised    
    '''

    # image modes that support transparency
    # this includes palette images, because Pillow does not report 
    # in that case
    alpha_modes = ["LA", "RGBA", "RGBa", "P"]

    def __init__(self, image):
        '''Constructor
        
        Arguments:
        image -- Image to be used as the source for this texture
        
        Postconditions: object is initialised with source image 
            converted to RGB(A) mode and a bytearray containing
            the image data 
        '''
        
        # will be using bytearrays over individual-pixel access, for speed

        if (image.mode in Texture.alpha_modes):  
            # alpha channel included
            self.pic = image.convert("RGBA")
            self.bpp = 4
        else:
            # no alpha channel
            self.pic = image.convert("RGB")
            self.bpp = 3
        self.pixels = self._pixelList(bytearray(self.pic.tobytes()))

        # two-dim list of x by y
        # y size on the inside for addressing as [x][y]
        self.valid = [[True] * self.pic.size[1] 
                      for _ in xrange(self.pic.size[0])]

    def _pixelList(self, bytelist):
        '''Convert a list of bytes into an array of pixels.
        
        Arguments:
        bytelist -- list of bytes
        
        Returns: list of bpp-tuples, each corresponding to a pixel
        
        Preconditions: len(bytes) is bpp * image size
        '''
        assert len(bytelist) == self.bpp * self.pic.size[0] * self.pic.size[1]
        
        # generate empty two-dim list of x by y
        pixlist = [[None] * self.pic.size[1] for _ in xrange(self.pic.size[0])]
        
        # flat position counter
        i = 0
        for y in xrange(self.pic.size[1]):
            for x in xrange(self.pic.size[0]):
                pixlist[x][y] = tuple(bytelist[i:i+self.bpp])
                i += self.bpp
        return pixlist
        
    def _locTest(self, point, shift = (0,0)):
        '''Test whether a pixel is within this image
        
        Arguments:
        point -- 2-tuple pixel location to be tested
        shift -- 2-tuple shift from loation (def. (0,0))
        
        Returns: true if the pixel is within the image, false if not
        '''        
        return ((point[0] + shift[0] >= 0) 
                and (point[0] + shift[0] < self.pic.size[0]) 
                and (point[1] + shift[1] >= 0) 
                and (point[1] + shift[1] < self.pic.size[1]))
                
    def goodList(self, centre, neighbourhood, valid):
        '''Trim a list of shifts about a centre point
        
        Arguments:
        centre -- 2-tuple location of the centre of the region
        neighbourhood -- list of 2-tuple shifts surrounding the centre pixel 
        valid -- list mapping integer locations to validity
        
        Returns: list of shifts from the centre which
            are both initialised and within the image
        '''
        ret = []
        for shift in neighbourhood:
            point = (centre[0] + shift[0], centre[1] + shift[1])
            if (self._locTest(point) 
                and valid[point[0]][point[1]]):
                ret.append(shift)
        return ret
    
    def getPixel(self, loc, shift = (0, 0)):
        '''Get the pixel at given location and shift
        
        Arguments:
        loc -- 2-tuple pixel location
        shift -- 2-tuple shift from location (def. (0,0)) 
        
        Returns: tuple containing the channels of the pixel
        
        Preconditions: loc + shift is inside the image
        '''
        assert self._locTest(loc, shift)
        return self.pixels[loc[0] + shift[0]][loc[1] + shift[1]]
    
    def setPixel(self, value, loc, shift = (0,0)):
        '''Set the pixel at given location and shift
        
        Arguments:
        value -- tuple containing channels of the pixel
        loc -- 2-tuple pixel location
        shift -- 2-tuple shift from location (def. (0,0))
        
        Preconditions: len(value) = self.bpp; loc + shift is inside the image
        Postconditions: pixel at loc + shift is set to value
        '''
        assert self._locTest(loc, shift)
        assert len(value) == self.bpp
        self.pixels[loc[0] + shift[0]][loc[1] + shift[1]] = value
        
    def setValid(self, loc):
        '''Set valid flag for pixel at a given location
        
        Arguments:
        loc -- 2-tuple pixel location
        
        Preconditions: loc is inside the image
        Postcondition: valid flag for pixel at loc is set to 1 
        '''
        self.valid[loc[0]][loc[1]] = True
    
    def toImage(self):
        '''Output this texture data into an Image
        
        Returns: an Image in the same encoding as the source containing
            this texture's data
        '''
        # flatten two-dim pixel to one-dim
        pixlist = [None] * self.pic.size[0] * self.pic.size[1]
        sx = self.pic.size[0]
        for x in xrange(self.pic.size[0]):
            for y in xrange(self.pic.size[1]):
                pixlist[x + y * sx] = self.pixels[x][y]
        # flatten pixel tuples to bytes
        channels = itertools.chain.from_iterable(pixlist)
                    
        # convert to byte buffer
        outbytes = buffer(bytearray(channels))
                
        # create Image
        return Image.frombytes(self.pic.mode, self.pic.size, outbytes)

class EmptyTexture(Texture):
    '''Empty texture synthesis object for untargeted synthesis.
    
    Inherits from Texture. No new methods or variables.
    '''
    
    def __init__(self, size, mode):
        '''Constructor
        
        Creates this EmptyTexture with blank target and all pixels 
        uninitialised. A blank image is created as backing, in either
        RGB or RGBA mode
        
        Arguments:
        size -- 2-tuple (width, height) size for the Texture
        mode -- string mode of the new Texture, RGB or RGBA 
        '''
        
        if (mode in Texture.alpha_modes):  
            # alpha channel included
            self.bpp = 4
            colour = (0, 0, 0, 0)  
        else:
            # no alpha channel
            self.bpp = 3
            colour = (0, 0, 0)
        self.pic = Image.new(mode, size)
        
        # two-dim lists of x by y
        # y size on the inside for addressing as [x][y]
        self.pixels = [[colour] * size[1] for _ in xrange(size[0])]
        self.valid = [[False] * size[1] for _ in xrange(size[0])]

class Shape:
    '''Defines a region for texture comparison.
        
    This entails is a mapping from scalar index to (row, column) shift,
    which is used to develop a list of pixels relative to a 'centre' pixel
    under consideration.
    
    Base Shape is left empty; use a subclass to get a specific shape.  
        
    Class Variables:
        shift -- array of vertex shifts
    '''
    
    def __init__(self):
        '''Constructor
        
        Creates this Shape with an empty list of shifts
        '''
        self.shift = []
        
class SquareShape(Shape):
    '''Defines a square Shape of given radius.
    
    Subclasses Shape for a square of edge length 2*radius+1. This
    is appropriate for targeted synthesis, where pixels in the target
    which have not yet been visited already have approximate values.
    '''
    
    def __init__(self, radius):
        '''Constructor
        
        Creates this SquareShape with every shift in the square from
        (-radius,-radius) to (radius,radius).
        
        Arguments:
            radius - the radius of the Shape, in pixels
            
        Postconditions: self.shift contains the appropriate shifts
        '''
        self.shift = [(i,j) 
                      for i in range(-radius, radius+1) 
                      for j in range(-radius, radius+1)] 

class EllShape(Shape):
    '''Defines a half-square Shape of given radius.
    
    Subclasses Shape for a half-square of the rows above (0,0)
    and columns to the left on the same row. This is appropriate for untargeted 
    synthesis, where these will be the pixels defined before the current 
    pixel.
    '''
    
    def __init__(self,radius):
        '''Constructor
        
        Creates this EllShape with every shift in the half-square 
        >= (-radius,-radius) and < (0,0).
        
        Arguments:
            radius - the radius of the Shape, in pixels
            
        Postconditions: self.shift contains the appropriate shifts
        '''
        
        # comparison is j < 0 (prior row) 
        # or j == 0 and i < 0 (same row prior column)
        self.shift = [(i,j)
                      for j in range(-radius, 1)
                      for i in range(-radius, radius+1)
                      if ((j < 0) or (j == 0 and i < 0))]
        