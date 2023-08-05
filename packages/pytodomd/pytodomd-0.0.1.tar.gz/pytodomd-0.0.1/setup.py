from setuptools import setup

setup(
    name='pytodomd',
    version='0.0.1',
    description='',
    author='Maciej Lorenc',
    author_email='lorencmaciek@gmail.com',
    packages=['pytodomd'],
    install_requires=[
        'click'
    ],
    zip_safe=False,
    entry_points='''
        [console_scripts]
        pytodomd=pytodomd.cli:main
    ''',
)
