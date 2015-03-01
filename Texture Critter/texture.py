'''Texture synthesis machinery

class Texture -- texture synthesis object
'''

from PIL import Image

class Texture:
    '''A texture synthesis object
    
    '''


    def __init__(self, image):
        '''Constructor
        
        Arguments:
        image -- Image to be used as the source for synthesis
        
        Postconditions: object is initialised with source image 
        '''
        
        self.source = image
        
        
    def expand(self):
        '''Expands the source texture into larger output
        
        Return: an Image containing the expanded texture
        
        for now just return the source
        '''
        
        return self.source