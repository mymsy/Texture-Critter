'''Texture synthesis machinery

class Texture -- texture synthesis object
'''

from PIL import Image

class Texture:
    '''A texture synthesis object
    
    Methods:
    expand -- expands the source into a larger texture
    
    Class variables:
    alpha_modes -- image modes implementing transparency   
    '''

    # image modes that support transparency
    alpha_modes = ["LA", "RGBA", "RGBa"]

    def __init__(self, image):
        '''Constructor
        
        Arguments:
        image -- Image to be used as the source for synthesis
        
        Postconditions: object is initialised with source image 
            (converted to RGB(A) mode) and a bytearray containing
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