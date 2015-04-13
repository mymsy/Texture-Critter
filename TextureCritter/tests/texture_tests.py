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

'''Tests for module texture.py

Tests are written for the nose framework and should be run with 
TextureCritter as the working directory in order for the image paths to
work correctly.
'''

from texture import *

# using sets to test because order does not matter

squareZero = {(0,0)}
squareOne = {(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), 
             (1, -1), (1, 0), (1, 1)}
squareTwo = {(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2), 
             (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2), 
             (0, -2), (0, -1), (0, 0), (0, 1), (0, 2), 
             (1, -2), (1, -1), (1, 0), (1, 1), (1, 2), 
             (2, -2), (2, -1), (2, 0), (2, 1), (2, 2)}
             
ellOne = {(-1, -1), (-1, 0), (-1, 1), (0, -1)}
ellTwo = {(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2), 
          (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2), 
          (0, -2), (0, -1)}
             
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
    assert texRGB.source.mode == "RGB"
    assert texRGB._bpp == 3
    assert (len(texRGB._bytes) ==
            texRGB._bpp * texRGB.source.size[0] * texRGB.source.size[1])
    
def test_texture_creation_RGBA():
    '''Test that RGBA texture has proper mode conversion and size'''
    colourpng = Image.open("tests/colourpng.png")
    texRGBA = Texture(colourpng)
    assert texRGBA.source.mode == "RGBA"
    assert texRGBA._bpp == 4
    assert (len(texRGBA._bytes) ==
            texRGBA._bpp * texRGBA.source.size[0] * texRGBA.source.size[1])
    
def test_texture_creation_BWA():
    '''Test that BW+A texture has proper mode conversion and size'''
    bwapng = Image.open("tests/bwapng.png")
    texBWA = Texture(bwapng)
    assert texBWA.source.mode == "RGBA"
    assert texBWA._bpp == 4
    assert (len(texBWA._bytes) ==
            texBWA._bpp * texBWA.source.size[0] * texBWA.source.size[1])
    
def test_texture_creation_palette():
    '''Test that palette texture has proper mode conversion and size'''
    colourgif = Image.open("tests/colourgif.gif")
    texpal = Texture(colourgif)
    assert texpal.source.mode == "RGBA"
    assert texpal._bpp == 4
    assert (len(texpal._bytes) ==
            texpal._bpp * texpal.source.size[0] * texpal.source.size[1])
    
class TestTexMethods:
    '''Tests for Texture methods'''
    def setUp(self):
        '''Setup - create a Texture
        
        gradient.png is a spiral gradient centered on (128,96) in
        a (256,192) image
        '''
        self.texture = Texture(Image.open("tests/gradient.png"))
        self.target = Image.open("tests/colourpng.png")
        pass
    
    def tearDown(self):
        '''Teardown'''
        del self.texture, self.target
    
    def testLocationSelf(self):
        '''Test location validity function for self.source.size'''
        x = self.texture.source.size[0]
        y = self.texture.source.size[1]
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
        
    def testLocationOther(self):
        '''Test location validity function for given size'''
        x = 128
        y = 1024
        assert self.texture._locTest((0,0), (x,y))
        assert not self.texture._locTest((0,-1), (x,y))
        assert not self.texture._locTest((-1,0), (x,y))
        assert not self.texture._locTest((-1,-1), (x,y))
        assert self.texture._locTest((x/2,y/2), (x,y))
        assert not self.texture._locTest((x/2,y), (x,y))
        assert not self.texture._locTest((x,y/2), (x,y))
        assert self.texture._locTest((x-1,y-1), (x,y))
        assert not self.texture._locTest((x,y-1), (x,y))
        assert not self.texture._locTest((x-1,y), (x,y))
        assert not self.texture._locTest((x,y), (x,y))
        
    def testIndexSelf(self):
        '''Test flat indexing function for self.source.size'''
        x = self.texture.source.size[0]
        y = self.texture.source.size[1]
        assert self.texture._index((0,0)) == 0
        assert self.texture._index((1,0)) == y
        assert self.texture._index((x/2,y/2)) == x/2 * y + y/2
        assert (self.texture._index((x-1,y-1)) + 1
                == self.texture.source.size[0] * self.texture.source.size[1])
        assert ((self.texture._index((x-1,y-1)) + 1) * self.texture._bpp 
                == len(self.texture._bytes))
        
    def testIndexOther(self):
        '''Test flat indexing function for given size'''
        x = 128
        y = 1024
        assert self.texture._index((0,0), (x,y)) == 0
        assert self.texture._index((1,0), (x,y)) == y
        assert self.texture._index((x/2,y/2), (x,y)) == x/2 * y + y/2
        assert (self.texture._index((x-1,y-1), (x,y)) + 1
                == x*y)
        
    def testListValid(self):
        '''Test neighbourhood function for valid slices'''
        x = self.texture.source.size[0]
        y = self.texture.source.size[1]
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
                {(x-3, 0), (x-3, 1), (x-3, 2), 
                 (x-2, 0), (x-2, 1), (x-2, 2), 
                 (x-1, 0), (x-1, 1), (x-1, 2)})
        assert (set(self.texture._goodList((x-1,y-1), box, valid)) ==
                {(x-3, y-3), (x-3, y-2), (x-3, y-1), 
                 (x-2, y-3), (x-2, y-2), (x-2, y-1), 
                 (x-1, y-3), (x-1, y-2), (x-1, y-1)})
        # just test the length, should get all points
        assert (len(self.texture._goodList((x/2,y/2), box, valid)) == 
                len(box.shift))
        assert (len(self.texture._goodList((x/2,y/2), ell, valid)) == 
                len(ell.shift))
        
    def testListInvalid(self):
        '''Test neighbourhood function for invalid slices'''
        x = self.texture.source.size[0]
        y = self.texture.source.size[1]
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
        x = self.texture.source.size[0]
        y = self.texture.source.size[1]
        
        # zero through column 127, 1 column 128-255
        semivalid = [0] * (x/2) * y + [1] * (x/2) * y
        ell = EllShape(2)
        box = SquareShape(2)

        assert (set(self.texture._goodList((x/2,0), box, semivalid)) ==
                {(x/2, 0),   (x/2, 1),   (x/2, 2), 
                 (x/2+1, 0), (x/2+1, 1), (x/2+1, 2), 
                 (x/2+2, 0), (x/2+2, 1), (x/2+2, 2)})
        assert (set(self.texture._goodList((x/2,y/2), ell, semivalid)) ==
                {(x/2, y/2-2), (x/2, y/2-1)})
        assert (len(self.texture._goodList((x/2-1,y/2), box, semivalid)) == 10)
        assert (len(self.texture._goodList((x/2,y/2), box, semivalid)) == 15)
        assert (len(self.texture._goodList((x/2+1,y/2), box, semivalid)) == 20)
        
    def testExpansion(self):
        '''Test expansion function numeric output'''
        # TODO fill this in when expand is done
        result = self.texture.expand(self.target)
        assert result.size == self.target.size
        assert result.mode == self.texture.source.mode
        