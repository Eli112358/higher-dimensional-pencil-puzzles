from setuptools import setup

setup(
	name='higher-dimensional-pencil-puzzles',
	version='',
	packages=[''],
	package_dir={'': 'src'},
	url='https://github.com/Eli112358/higher-dimensional-pencil-puzzles',
	license='GNUv3',
	author='Eli112358',
	author_email='eli112358@users.noreply.github.com',
	description='Navigate, solve, and assist in setting pencil puzzles that escape "Flatland"',
	install_requires=[
		'numpy >=1.19.2',
		'pygame >=2.0.0',
	],
	python_requires='3.9',
	project_urls={
		'repository': 'https://github.com/Eli112358/higher-dimensional-pencil-puzzles',
		'web interface (planned)': 'http://eli112358.github.io/higher-dimensional-pencil-puzzles'
	},
)
