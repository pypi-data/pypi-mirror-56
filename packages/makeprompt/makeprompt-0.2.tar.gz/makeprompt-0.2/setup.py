import os
from setuptools import setup, find_packages

version = '0.2'

here = os.path.dirname(__file__)

with open(os.path.join(here, 'README.rst')) as fp:
    longdesc = fp.read()

# with open(os.path.join(here, 'CHANGELOG.rst')) as fp:
#     longdesc += "\n\n" + fp.read()


setup(
    name='makeprompt',
    version=version,
    packages=find_packages(),
    url='https://github.com/rshk/makeprompt',
    license='BSD License',
    author='Samuele Santi',
    author_email='samuele@samuelesanti.com',
    description='Generate customised shell prompts (for ZSH)',
    long_description=longdesc,
    install_requires=[],
    # tests_require=tests_require,
    # test_suite='tests',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    entry_points={
        'console_scripts': ['makeprompt=makeprompt.cli:main'],
    },
    package_data={'': ['README.rst', 'CHANGELOG.rst']},
    include_package_data=True,
    zip_safe=False)
