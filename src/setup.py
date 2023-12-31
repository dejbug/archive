from distutils.core import setup

import os, glob

def getPyModules(relative = False):
	nn = glob.glob('src/*.py') + glob.glob('src/lib/*.py')
	nn = (n for n in nn if n != 'src/setup.py')
	if relative:
		nn = (os.path.relpath(n, 'src') for n in nn)
	nn = (os.path.splitext(n)[0] for n in nn)
	# print(list(nn))
	return list(nn)

setup(
	name = 'archive',
	version = '0.0.1',
	url = 'https://dejbug.de/python/archive',
	author_email = 'dejbug@users.noreply.github.com',
	author = 'Dejan Budimir',
	# package_dir = {'': 'src'},
	py_modules = getPyModules()
)
