# MIT License

# Copyright (c) 2019 Sebastian Daum

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import unittest
from parsesql.main import executers


class BaseExecuterTest(unittest.TestCase):

    def test_if_baseexecuter_class_exists(self):
        """
        test if Baseexecuter class is available
        """
        klass = executers.BaseExecuter()
        self.assertEqual(klass.__class__.__name__, "BaseExecuter")


class SequentialExecuterTest(unittest.TestCase):

    def test_if_sequentialexecuter_class_exists(self):
        """
        test if SequentialExecuter class is available
        """
        klass = executers.SequentialExecuter()
        self.assertEqual(klass.__class__.__name__, "SequentialExecuter")

    def test_if_run_method_exist(self):
        """
        test if run methd is available
        """
        methods = dir(executers.SequentialExecuter())
        self.assertIn('run', methods)


class MultiProcessingExecuterTest(unittest.TestCase):

    def test_if_multiprocessing_class_exists(self):
        """fr
        test if MultiProcessing class is available
        """
        klass = executers.MultiProcessingExecuter()
        self.assertEqual(klass.__class__.__name__, "MultiProcessingExecuter")

    def test_if_run_method_exist(self):
        """
        test if run methd is available
        """
        methods = dir(executers.MultiProcessingExecuter())
        self.assertIn('run', methods)
