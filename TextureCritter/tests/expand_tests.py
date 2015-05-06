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

from expand import *

class TestExpandMethods:
    '''Tests for Expand methods'''
    def setUp(self):
        '''Setup - create a Texture
        
        gradient.png is a spiral gradient centered on (128,96) in
        a (256,192) image
        '''
        self.source = Texture(Image.open("tests/gradient.png"))
        self.target = Texture(Image.open("tests/colourpng.png"))
    
    def tearDown(self):
        '''Teardown'''
        del self.source, self.target
    
    def testExpansion(self):
        '''Test expansion function numeric output'''
        # TODO fill this in when expand is done
        result = expand(self.source, self.target)
        assert result.size == self.target.pic.size
        assert result.mode == self.source.pic.mode
