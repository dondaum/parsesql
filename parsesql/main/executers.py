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

from parsesql.util.logger_service import LoggerMixin
from multiprocessing import Pool, cpu_count
from typing import Callable


class BaseExecuter(object):
    pass


class SequentialExecuter(BaseExecuter, LoggerMixin):

    def __init__(self,
                 target_list: list = None,
                 klass=None,
                 klass_method_name: str = None,
                 func: Callable = None):

        self.target_list = target_list
        self.klass = klass
        self.klass_method_name = klass_method_name
        self.func = func

    def run(self):
        """
        run either a single callable or class method
        """
        if (self.klass and self.klass_method_name):
            return [getattr(self.klass(element), self.klass_method_name)() for
                    element in self.target_list]
        elif self.func:
            return [self.func(element) for element in self.target_list]
        else:
            self.logger.error(f'Error happend. You must either declare a '
                              f'function or a class with init param and '
                              f'a dependent method'
                              )


class MultiProcessingExecuter(BaseExecuter, LoggerMixin):

    def __init__(self,
                 target_list: list = None,
                 klass=None,
                 klass_method_name: str = None,
                 func: Callable = None,
                 cpu_cores: int = 1):

        self.target_list = target_list
        self.klass = klass
        self.klass_method_name = klass_method_name
        self.func = func
        self.cpu_cores = cpu_cores

    def determine_max_proc(self):
        return cpu_count()

    def determine_use_process(self):
        if self.cpu_cores >= self.determine_max_proc():
            return self.determine_max_proc() - 1
        else:
            return self.cpu_cores

    def _klass_run(self, file):
        """
        Helper run method for the process mapping and running
        """
        return getattr(self.klass(file), self.klass_method_name)()

    def run(self):
        """
        run either a single callable or class method
        """
        number_of_processcess = self.determine_use_process()
        p = Pool(number_of_processcess)

        if (self.klass and self.klass_method_name):
            return p.map(self._klass_run, self.target_list)
        elif self.func:
            return p.map(self.func, self.target_list)
        else:
            self.logger.error(f'Error happend. You must either declare a '
                              f'function or a class with init param and '
                              f'a dependent method'
                              )
