from distutils.core import setup
# setup( name='archive', version='0.0.1', py_modules=['archive', 'lib/*.py'] )

setup(
	name='archive',
	version='0.0.1',
	url='https://dejbug.de/python/archive',
	author_email='dejbug@users.noreply.github.com',
	author='Dejan Budimir',
	package_dir = {'': 'src'},
	# py_modules=['archive.py', 'lib/*.py']
	py_modules=['archive', 'lib/archive', 'lib/net', 'lib/cache', 'lib/abs']
)