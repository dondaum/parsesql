import logging

class LoggerMixin(object):

    FORMAT = '[%(asctime)s] [%(processName)-10s] [%(name)s] [%(levelname)s] -> %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)

    @property
    def logger(self):
        name = '.'.join([
            self.__module__,
            self.__class__.__name__
        ])
        return logging.getLogger(name)
