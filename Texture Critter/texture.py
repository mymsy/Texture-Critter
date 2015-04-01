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
    expand -- expands the source into a larger texture
    
    Class variables:
    alpha_modes -- image modes implementing transparency
    source -- the source image for expansion, converted to RGB(A) palette   
    '''

    # image modes that support transparency
    alpha_modes = ["LA", "RGBA", "RGBa"]

    def __init__(self, image):
        '''Constructor
        
        Arguments:
        image -- Image to be used as the source for synthesis
        
        Postconditions: object is initialised with source image 
            converted to RGB(A) mode and a bytearray containing
            the image data 
        '''
        
        # will be using bytearrays over individual-pixel access, for speed
        if (image.mode in Texture.alpha_modes) or (image.mode == "P"  
                and image.palette.mode in Texture.alpha_modes):
            # alpha channel included
            self.source = image.convert("RGBA")
            self._bpp = 4
        else:
            # no alpha channel
            self.source = image.convert("RGB")
            self._bpp = 3
        self._bytes = bytearray(self.source.tobytes())
        
        
    def expand(self):
        '''Expands the source texture into larger output
        
        Return: an Image containing the expanded texture
        
        For now just return the source
        '''
        
        # create an image from a bytearray
        # for now it's just the one we started with
        return Image.frombytes(self.source.mode, self.source.size, buffer(self._bytes))
    
class Shape:
    '''Defines a region for texture comparison.
        
    This entails is a mapping from scalar index to (row, column) shift,
    which is used to develop a list of pixels relative to a 'center' pixel
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
    
    Subclasses Shape for a half-square of the rows above (0,0) and
    columns to the left on the same row. This is appropriate for 
    untargeted synthesis, where these will be the pixels defined before 
    the current pixel.
    '''
    
    def __init__(self,radius):
        '''Constructor
        
        Creates this EllShape with every shift in the half-square 
        >= (-radius,-radius) and < (0,0).
        
        Arguments:
            radius - the radius of the Shape, in pixels
            
        Postconditions: self.shift contains the appropriate shifts
        '''
        
        # comparison is lexical and i stops at 0
        self.shift = [(i,j)
                      for i in range(-radius, 1)
                      for j in range(-radius, radius+1)
                      if (i,j) < (0,0)]