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
from multiprocessing import cpu_count


def square_number(value: int) -> int:
    return value * value


class TMath():
    def __init__(self, value):
        self.value = value

    def square_number(self) -> int:
        return self.value * self.value


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

    def test_function_passing(self):
        """
        test a callable can be passed and executed
        """
        consumer_list = [1, 2, 3, 4]
        method = square_number
        exe = executers.SequentialExecuter(target_list=consumer_list,
                                           func=method)
        self.assertEqual(True, callable(exe.func))

    def test_run_method_with_single_callable(self):
        """
        test if run method runs the callable with the target list as input
        """
        consumer_list = [1, 2, 3, 4]
        exp_res = [1, 4, 9, 16]
        method = square_number
        exe = executers.SequentialExecuter(target_list=consumer_list,
                                           func=method)
        res = exe.run()
        self.assertEqual(res, exp_res)

    def test_run_method_with_class_callable(self):
        """
        test if run method runs a class and method name with the target list
        as input
        """
        consumer_list = [1, 2, 3, 4]
        exp_res = [1, 4, 9, 16]

        exe = executers.SequentialExecuter(target_list=consumer_list,
                                           klass=TMath,
                                           klass_method_name="square_number")
        res = exe.run()
        self.assertEqual(res, exp_res)

    def test_no_run_if_no_param(self):
        """
        test if no run can be executed
        """
        consumer_list = [1, 2, 3, 4]

        exe = executers.SequentialExecuter(target_list=consumer_list)
        res = exe.run()
        self.assertEqual(res, None)


class MultiProcessingExecuterTest(unittest.TestCase):

    def test_if_multiprocessing_class_exists(self):
        """
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

    def test_cpu_count(self):
        """
        test if cpu count method return cpu count
        """
        expected = cpu_count()
        klass = executers.MultiProcessingExecuter()
        self.assertEqual(expected, klass.determine_max_proc())

    def test_used_cpu(self):
        """
        test if cpu count method return cpu count
        """
        max_cpu = cpu_count()
        klass = executers.MultiProcessingExecuter(cpu_cores=max_cpu)
        self.assertEqual(max_cpu - 1, klass.determine_use_process())

    def test_run_method_with_single_callable(self):
        """
        test if run method runs the callable with the target list as input
        """
        consumer_list = [1, 2, 3, 4]
        exp_res = [1, 4, 9, 16]
        method = square_number
        exe = executers.MultiProcessingExecuter(target_list=consumer_list,
                                                func=method,
                                                cpu_cores=2)
        res = exe.run()
        self.assertEqual(res, exp_res)

    def test_run_method_with_class_callable(self):
        """
        test if run method runs a class and method name with the target list
        as input
        """
        consumer_list = [1, 2, 3, 4]
        exp_res = [1, 4, 9, 16]

        exe = executers.MultiProcessingExecuter(
            target_list=consumer_list,
            klass=TMath,
            klass_method_name="square_number",
            cpu_cores=2
        )
        res = exe.run()
        self.assertEqual(res, exp_res)

    def test_no_run_if_no_param(self):
        """
        test if no run can be executed
        """
        consumer_list = [1, 2, 3, 4]

        exe = executers.MultiProcessingExecuter(target_list=consumer_list,
                                                klass=TMath)
        res = exe.run()
        self.assertEqual(res, None)
