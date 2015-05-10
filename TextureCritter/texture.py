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

'''Texture synthesis machinery

class Texture -- performs texture synthesis
class Shape -- defines the sampling shape for texture region comparison
'''

from PIL import Image

class Texture:
    '''A texture synthesis object
    
    Methods:
    
    Class variables:
    alpha_modes -- image modes implementing transparency
    pic -- the source image for expansion, converted to RGB(A) palette   
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
        self._bytes = bytearray(self.pic.tobytes())
        self.pixels = self._pixelList(self._bytes)

    def _pixelList(self, bytelist):
        '''Convert a list of bytes into an array of pixels.
        
        Arguments:
        bytelist -- list of bytes
        bpp -- number of bytes per pixel
        
        Returns: list of bpp-tuples, each corresponding to a pixel
        
        Preconditions: len(bytes) is a multiple of bpp
        '''
        assert len(bytelist) % self.bpp == 0
        pixlist = []
        for i in range(0, len(bytelist), self.bpp):
            pixlist.append(tuple(bytelist[i:i+self.bpp]))
        return pixlist
        
    def _locTest(self, point, shift = (0,0)):
        '''Test whether a pixel is within this image
        
        Arguments:
        point -- the pixel to be tested
        
        Returns: true if the pixel is within the image, false if not
        '''        
        return ((point[0] + shift[0] >= 0) 
                and (point[0] + shift[0] < self.pic.size[0]) 
                and (point[1] + shift[1] >= 0) 
                and (point[1] + shift[1] < self.pic.size[1]))
        
    def _index(self, pixel, shift = (0, 0)):
        '''Determine the index into flat vectors for a given pixel
        
        Arguments:
        pixel -- 2-tuple pixel location
        shift -- 2-tuple shift from location (def. (0,0)) 
        
        Returns -- integer location in flat lists
        '''
        # TODO consider using numpy for two-dim array rather than needing this
        return ((pixel[0] + shift[0]) 
                + (pixel[1] + shift[1]) * self.pic.size[0])
        
    def _goodList(self, centre, neighbourhood, valid):
        '''Create a list of initialised pixels from a Shape and a point
        
        Arguments:
        centre -- the centre of the region
        neighbourhood -- Shape surrounding the centre pixel 
        valid -- list of valid pixels
        
        Returns: list of pixels defined by given shifts from the centre which
            are both initialised and within the image
        '''
        ret = []
        for shift in neighbourhood.shift:
            point = (centre[0] + shift[0], centre[1] + shift[1])
            if (self._locTest(point) 
                and (valid[self._index(point)] != 0)):
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
        return self.pixels[self._index(loc, shift)]
    
    def setPixel(self, value, loc, shift = (0,0)):
        '''Set the pixel at given location and shift
        
        Arguments:
        value -- tuple containing channels of the pixel
        loc -- 2-tuple pixel location
        shift -- 2-tuple shift from location (def. (0,0))
        
        Preconditions: len(value) = self.bpp; loc + shift is inside the image
        '''
        assert self._locTest(loc, shift)
        assert len(value) == self.bpp
        self.pixels[self._index(loc,shift)] = value
    
    def toImage(self):
        '''Output this texture data into an Image
        
        Returns: an Image in the same encoding as the source containing
            this texture's data
        '''
        # flatten pixel list
        channels = []
        for p in self.pixels: 
            channels += list(p)
            
        # convert to byte buffer
        outbytes = buffer(bytearray(channels))
        
        # create Image
        return Image.frombytes(self.pic.mode, self.pic.size, outbytes)

    
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
        