from __future__ import print_function

from setuptools import setup


version = '0.2.0'


setup(
    name='togif',
    version=version,
    py_modules=['togif'],
    install_requires=['imageio<2.5', 'imageio-ffmpeg', 'imgviz', 'tqdm'],
    author='Kentaro Wada',
    author_email='www.kentaro.wada@gmail.com',
    url='http://github.com/wkentaro/togif',
    entry_points={
        'console_scripts': ['togif=togif:main']
    },
)
