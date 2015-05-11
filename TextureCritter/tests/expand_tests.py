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

'''Tests for module expand.py

Tests are written for the nose framework and should be run with 
TextureCritter as the working directory in order for the image paths to
work correctly.
'''

from expand import expand, compare
from texture import Texture, SquareShape
from PIL import Image
from math import sqrt

class TestExpandMethods:
    '''Tests for Expand methods'''
    def setUp(self):
        '''Setup - create a Texture
        
        gradient.png is a spiral gradient centred on (128,96) in
        a (256,192) image
        '''
        self.source = Texture(Image.open("tests/gradient.png"))
        self.target = Texture(Image.open("tests/colourpng.png"))
        self.shape = SquareShape(2)
    
    def tearDown(self):
        '''Teardown'''
        del self.source, self.target
    
    # REDACTED - takes too long
#     def testExpansion(self):
#         '''Test expansion function numeric output'''
#         # TODO fill this in when expand is done
#         result = expand(self.source, self.target, self.shape)
#         assert result.size == self.target.pic.size
#         assert result.mode == self.source.pic.mode

    def testCompare(self):
        '''Test pixel comparison'''
        cases = [((0, 0, 0), (0, 0, 0), 0),
                 ((0,0), (3,4), 5**2),
                 ((1,2,3), (4,5,6), 27),
                 ((1,1,1,1), (-1,-1,-1,-1), 4**2),
                 ((255, 255, 255), (255, 255, 255), 0),
                 ((0, 0, 0), (255, 255, 255), 3*255**2)
                 ]
        for c in cases:
            # threshold test for floating point roundoff
            assert(abs(compare(c[0], c[1]) - c[2]) < 1e-8)