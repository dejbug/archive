import os, logging

from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET


FORMAT = '%(asctime)s [%(levelname)s] (%(relmod)s:%(lineno)s:%(funcName)s) : %(message)s'
logging.basicConfig(format = FORMAT)


logger = logging.getLogger()

setLevel = logger.setLevel

debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
critical = logger.critical
exception = logger.exception


def setDebugLevel(on = True):
	if on:
		logger.setLevel(logging.NOTSET)
	else:
		logger.setLevel(logging.WARNING)


def setRoot(__file__ = ""):
	old_factory = logging.getLogRecordFactory()

	def record_factory(*args, **kwargs):
	    record = old_factory(*args, **kwargs)
	    root = os.path.dirname(__file__)
	    relpath = os.path.relpath(record.pathname, root)
	    record.relmod = os.path.splitext(relpath)[0]
	    return record

	logging.setLogRecordFactory(record_factory)


setRoot()
