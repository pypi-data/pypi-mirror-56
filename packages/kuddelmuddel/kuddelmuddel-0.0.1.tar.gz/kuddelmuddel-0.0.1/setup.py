# -*- coding: utf-8 -*-

from distutils.core import setup

console_scripts = """
[console_scripts]
sacremoses=sacremoses.cli:cli
"""


setup(
    name='kuddelmuddel',
    version='0.0.1',
    packages=['kuddelmuddel',],
    url = 'https://github.com/alvations/kuddelmuddel',
    description='Translation Memory Munger',
    license="MIT",
    install_requires = ['six', 'click', 'joblib', 'tqdm'],
    entry_points=console_scripts,
)
