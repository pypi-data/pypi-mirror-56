#emacs: -*- mode: python-mode; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*- 
#ex: set sts=4 ts=4 sw=4 noet:
"""

 COPYRIGHT: Yaroslav Halchenko 2014

 LICENSE: MIT

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.
"""

__author__ = 'yoh'
__license__ = 'MIT'

from collections import OrderedDict
from .simple_s3 import pipeline as s3_pipeline


def pipeline():
    return s3_pipeline(
        bucket='datalad-test1-manydirs-versioned',
        # prefix=prefix,
        # directory=OrderedDict(
        # [
        #     # test deciding on a subdir
        #     ('d1/sd2$', {
        #         'template': 'test_s3',
        #         'template_func': 'pipeline',}),
        #     # any ssd directory
        #     ('.*ssd$', {}),  # will inherit original/hardcoded
        #     # the others shouldn't be directories
        # ]),
        directory_crawl_cfg_fields=[]  # do not pass any of them, we need just prefix
    )