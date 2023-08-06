from setuptools import setup
from BSG import __version__
setup(
	name = 'BSG',
	version = __version__,
	author = 'mvfki',
	url = 'https://github.com/mvfki/BullshitGenerator',
	description = 'Modulized version of BullshitGenerator. Original version see https://github.com/menzi11/BullshitGenerator',
	entry_points={'console_scripts': ['BSG = BSG.__main__:main']},
    packages = ['BSG'],
	python_requires = '>=3.4',
    package_data = {'BSG': ['default.json']}, 
    include_package_data = True
)
