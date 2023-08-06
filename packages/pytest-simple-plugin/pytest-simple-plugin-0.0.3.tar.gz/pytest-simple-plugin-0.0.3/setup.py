"""
:Description: setup.py
"""
import setuptools
from os import path

with open(path.join(path.dirname(__file__), 'readme.md')) as f:
    README = f.read()

setuptools.setup(
    name='pytest-simple-plugin',
    packages=['pytest_simple_plugin'],
    version='0.0.3',
    description='Simple pytest plugin',
    long_description=README,
    url='https://github.com/thaffenden/pytest-easy-api',
    author='Li Liu',
    author_email="liuli.930@qq.com",
    license='BSD License',
    install_requires=['pytest'],
    # plugin available to pytest
    entry_points={
        'pytest11': ['pytest_simple_plugin = pytest_simple_plugin.plugin_module']
    },
    classifiers=[
        "Framework :: Pytest",
    ],
    keywords=['testing', 'pytest'],
    python_requires='>=3',

)
