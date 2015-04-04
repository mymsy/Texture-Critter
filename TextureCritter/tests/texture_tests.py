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

'''Tests for module texture.py '''

#from PIL import Image

from TextureCritter.texture import *

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

#colourjpg = Image.open("tests\colourjpg.jpg")
             
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
    
# def test_texture_creation():
#     '''Test that texture is initialised with the proper mode conversion and size
#     
#     Should make more of these for weird initial modes
#     '''
#     a = Texture(colourjpg)
    