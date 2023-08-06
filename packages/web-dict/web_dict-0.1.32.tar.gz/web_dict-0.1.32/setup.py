from distutils.core import setup
from pathlib import Path

from setuptools import find_packages

setup(
    name='web_dict',  # How you named your package folder (MyLib)
    packages=find_packages(),  # Chose the same as "name"
    description='parser class for collinsdictionary.com and lexico.com',
    long_description=Path("readme.md").read_text(),
    long_description_content_type='text/markdown',
    version='0.1.32',  # Start with a small number and increase it with every change you make
    license='agpl-3.0',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    author='Kyle, Hwang',  # Type in your name
    author_email='upday7@163.com',  # Type in your E-Mail
    url='https://github.com/upday7/web_dict',  # Provide either the link to your github or to your website
    keywords=['dictionary', 'spanish', 'english', 'chinese', 'collins', 'oxford', 'lexico'],
    install_requires=[  # I get to this in a second
        'bs4',
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
