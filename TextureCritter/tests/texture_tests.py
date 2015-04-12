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
    