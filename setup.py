from setuptools import find_packages, setup


setup(
	name='sudoku',
	version='0.1',
	description='Sudoku resolver',
	author='Omar Rampado',
	author_email='omar@ognibit.it',
	package_dir={'': 'src'},
	packages=find_packages(where='src'),
)