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
from compiler.ast import Function

'''Tests for module texture.py

Tests are written for the nose framework and should be run with 
TextureCritter as the working directory in order for the image paths to
work correctly.
'''

from texture import *
from PIL import Image
from random import randrange

# using sets to test because order does not matter

squareZero = {(0,0)}
squareOne = {(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), 
             (1, -1), (1, 0), (1, 1)}
squareTwo = {(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2), 
             (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2), 
             (0, -2), (0, -1), (0, 0), (0, 1), (0, 2), 
             (1, -2), (1, -1), (1, 0), (1, 1), (1, 2), 
             (2, -2), (2, -1), (2, 0), (2, 1), (2, 2)}
             
ellOne = {(-1, -1), (0, -1), (1, -1), (-1, 0)}
ellTwo = {(-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2), 
          (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), 
          (-2, 0), (-1, 0)}
             
def test_base_empty():
    '''Test that the base class does not define any shifts'''
    a = Shape()
    assert a.shift == []
    
def test_square_zero():
    '''Test that a zero-radius square contains only the origin'''
    a = SquareShape(0)    
    assert set(a.shift) == squareZero
    
def test_square_one():
    '''Test that radius-one square contains the correct points'''
    a = SquareShape(1)
    assert set(a.shift) == squareOne
    
def test_square_two():
    '''Test that radius-two square contains the correct points'''
    a = SquareShape(2)
    assert set(a.shift) == squareTwo

def test_ell_zero():
    '''Test that zero-radius L contains no points'''
    a = EllShape(0)
    assert a.shift == []

def test_ell_one():
    '''Test that radius-one L contains the correct points'''
    a = EllShape(1)
    assert set(a.shift) == ellOne
    
def test_ell_two():
    '''Test that radius-two L contains the correct points'''
    a = EllShape(2)
    assert set(a.shift) == ellTwo
    
def test_texture_creation_RGB():
    '''Test that RGB texture has proper mode conversion and size'''
    colourjpg = Image.open("tests/colourjpg.jpg")
    texRGB = Texture(colourjpg)
    assert texRGB.pic.mode == "RGB"
    assert texRGB.bpp == 3
    assert (len(texRGB._bytes) ==
            texRGB.bpp * texRGB.pic.size[0] * texRGB.pic.size[1])
    
def test_texture_creation_RGBA():
    '''Test that RGBA texture has proper mode conversion and size'''
    colourpng = Image.open("tests/colourpng.png")
    texRGBA = Texture(colourpng)
    assert texRGBA.pic.mode == "RGBA"
    assert texRGBA.bpp == 4
    assert (len(texRGBA._bytes) ==
            texRGBA.bpp * texRGBA.pic.size[0] * texRGBA.pic.size[1])
    
def test_texture_creation_BWA():
    '''Test that BW+A texture has proper mode conversion and size'''
    bwapng = Image.open("tests/bwapng.png")
    texBWA = Texture(bwapng)
    assert texBWA.pic.mode == "RGBA"
    assert texBWA.bpp == 4
    assert (len(texBWA._bytes) ==
            texBWA.bpp * texBWA.pic.size[0] * texBWA.pic.size[1])
    
def test_texture_creation_palette():
    '''Test that palette texture has proper mode conversion and size'''
    colourgif = Image.open("tests/colourgif.gif")
    texpal = Texture(colourgif)
    assert texpal.pic.mode == "RGBA"
    assert texpal.bpp == 4
    assert (len(texpal._bytes) ==
            texpal.bpp * texpal.pic.size[0] * texpal.pic.size[1])
    
class TestTexMethods:
    '''Tests for Texture methods'''
    def setUp(self):
        '''Setup - create a Texture
        
        gradient.png is a spiral gradient cented on (128,96) in
        a (256,192) image
        '''
        self.texture = Texture(Image.open("tests/gradient.png"))
    
    def tearDown(self):
        '''Teardown'''
        del self.texture
    
    def testPixList(self):
        '''Test pixel list function'''
        # generated at object creation
        assert (len(self.texture.pixels) * self.texture.bpp
                == len(self.texture._bytes))
        for p in self.texture.pixels:
            assert len(p) == self.texture.bpp
            
        # content
        flat = range(99)
        squish = [(i, i+1, i+2) for i in range(0,99,3)]
        assert self.texture._pixelList(flat) == squish
    
    def testLocationSelf(self):
        '''Test location validity function for self.pic.size'''
        x = self.texture.pic.size[0]
        y = self.texture.pic.size[1]
        assert self.texture._locTest((0,0))
        assert not self.texture._locTest((0,-1))
        assert not self.texture._locTest((-1,0))
        assert not self.texture._locTest((-1,-1))
        assert self.texture._locTest((x/2,y/2))
        assert not self.texture._locTest((x/2,y))
        assert not self.texture._locTest((x,y/2))
        assert self.texture._locTest((x-1,y-1))
        assert not self.texture._locTest((x,y-1))
        assert not self.texture._locTest((x-1,y))
        assert not self.texture._locTest((x,y))
        
    def testIndex(self):
        '''Test flat indexing function'''
        x = self.texture.pic.size[0]
        y = self.texture.pic.size[1]
        assert self.texture._index((0,0)) == 0
        assert self.texture._index((1,0)) == 1
        assert self.texture._index((0,1)) == x
        assert self.texture._index((x/2,y/2)) == x/2 + y/2 * x
        assert (self.texture._index((x-1,y-1)) + 1
                == self.texture.pic.size[0] * self.texture.pic.size[1])
        assert ((self.texture._index((x-1,y-1)) + 1) * self.texture.bpp 
                == len(self.texture._bytes))
        
    def testIndexShift(self):
        '''Test flat indexing function with shifts'''
        x = self.texture.pic.size[0]
        y = self.texture.pic.size[1]
        assert self.texture._index((0,0), (1,1)) == x + 1
        assert self.texture._index((0,1), (-1,0)) == x - 1
        assert self.texture._index((0,y/2), (x/2,0)) == x/2 + y/2 * x
        
    def testListValid(self):
        '''Test neighbourhood function for valid slices'''
        x = self.texture.pic.size[0]
        y = self.texture.pic.size[1]
        valid = [1] * x * y
        ell = EllShape(2)
        box = SquareShape(2)
        
        # valid slices
        assert self.texture._goodList((0,0), ell, valid) == []
        assert (set(self.texture._goodList((0,0), box, valid)) ==
                {(0, 0), (0, 1), (0, 2), 
                 (1, 0), (1, 1), (1, 2), 
                 (2, 0), (2, 1), (2, 2)})
        assert (set(self.texture._goodList((x-1,0), box, valid)) ==
                {(-2, 0), (-2, 1), (-2, 2), 
                 (-1, 0), (-1, 1), (-1, 2), 
                 (0, 0),  (0, 1),  (0, 2)})
        assert (set(self.texture._goodList((x-1,y-1), box, valid)) ==
                {(-2, -2), (-2, -1), (-2, 0), 
                 (-1, -2), (-1, -1), (-1, 0), 
                 (0, -2),  (0, -1),  (0, 0)})
        # just test the length, should get all points
        assert (len(self.texture._goodList((x/2,y/2), box, valid)) == 
                len(box.shift))
        assert (len(self.texture._goodList((x/2,y/2), ell, valid)) == 
                len(ell.shift))
        
    def testListInvalid(self):
        '''Test neighbourhood function for invalid slices'''
        x = self.texture.pic.size[0]
        y = self.texture.pic.size[1]
        invalid = [0] * x * y
        ell = EllShape(2)
        box = SquareShape(2)

        assert self.texture._goodList((0,0), ell, invalid) == []
        assert self.texture._goodList((0,0), box, invalid) == []
        assert self.texture._goodList((x-1,y-1), ell, invalid) == []
        assert self.texture._goodList((x-1,y-1), box, invalid) == []
        assert self.texture._goodList((x/2,y/2), ell, invalid) == []
        assert self.texture._goodList((x/2,y/2), box, invalid) == []
        
    def testListSemivalid(self):
        '''Test neighbourhood function for semi-valid slices'''
        x = self.texture.pic.size[0]
        y = self.texture.pic.size[1]
        
        # zero through row 95, 1 rows 96-191
        semivalid = [0] * x * (y/2) + [1] * x * (y/2)
        ell = EllShape(2)
        box = SquareShape(2)

        assert (set(self.texture._goodList((0, y/2), box, semivalid)) ==
                {(0, 0), (1, 0), (2, 0),
                 (0, 1), (1, 1), (2, 1),
                 (0, 2), (1, 2), (2, 2)})
        assert (set(self.texture._goodList((x/2,y/2), ell, semivalid)) ==
                {(-2, 0), (-1, 0)})
        assert (len(self.texture._goodList((x/2,y/2-1), box, semivalid)) == 10)
        assert (len(self.texture._goodList((x/2,y/2), box, semivalid)) == 15)
        assert (len(self.texture._goodList((x/2,y/2+1), box, semivalid)) == 20)
                        
    def testGetPixel(self):
        '''Test pixel getter function'''
        for _ in xrange(100):
            x = randrange(self.texture.pic.size[0])
            y = randrange(self.texture.pic.size[1])
            assert (self.texture.getPixel((x,y)) == 
                    self.texture.pic.getpixel((x,y)))
     
    def testSetPixel(self):
        '''Test pixel setter function'''
        throwaway = Texture(self.texture.pic)
        for _ in xrange(100):
            value = tuple([randrange(255) for _ in xrange(self.texture.bpp)])
            x = randrange(self.texture.pic.size[0])
            y = randrange(self.texture.pic.size[1])
            throwaway.setPixel(value, (x,y))
            assert (throwaway.getPixel((x,y)) == value) 

    def testToImage(self):
        '''Test Image output Function'''
        result = self.texture.toImage()
        assert result.size == self.texture.pic.size
        assert result.mode == self.texture.pic.mode
        for _ in xrange(100):
            x = randrange(self.texture.pic.size[0])
            y = randrange(self.texture.pic.size[1])
            assert (self.texture.getPixel((x,y)) == result.getpixel((x,y)))                     
        