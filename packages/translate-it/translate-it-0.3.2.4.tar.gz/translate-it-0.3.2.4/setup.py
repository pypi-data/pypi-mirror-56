import os

from codecs import open
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


requires = [
    'requests>=2.22.0',
    'lxml>=4.4.1',
    'cachelib',
    'appdirs'
]


about = {}
with open(os.path.join(here, 'translate_it', '__version__.py'),
          'r', 'utf-8') as f:
    exec(f.read(), about)

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()


setup(

    name=about['__name__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    python_requires='>=3.5',
    packages=find_packages(exclude=('tests', 'tests.*')),
    zip_safe=False,
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={
        'console_scripts': [
            'translate_it = translate_it.translate_it:command_line_runner'
        ]
    },
    install_requires=requires,
)
