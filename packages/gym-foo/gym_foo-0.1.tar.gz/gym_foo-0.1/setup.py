import os
from setuptools import setup
#from distutils.core import setup

# with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
#    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

version_str = open(os.path.join('gym_foo', '_version.txt'), 'r').read().strip()

setup(
    name='gym_foo',
    version=version_str,
    packages=['gym_foo'],

    author='Yeison Cardona',
    author_email='yeisoneng@gmail.com',
    maintainer='Yeison Cardona',
    maintainer_email='yeisoneng@gmail.com',

    # url='http://yeisoncardona.com/',
    download_url='https://bitbucket.org/gcpds/gym_foo/downloads/',

    install_requires=[
        'gym',
        # 'pyserial',
        # 'scipy>=1.3.1',
        # 'numpy',
        # 'psutil',
        # 'mne',
        # 'requests',
        # 'tornado',
        # 'systemd_service',
    ],

    include_package_data=True,
    license='BSD License',
    description="GCPDS: gym-foo",
    #    long_description = README,

    classifiers=[

    ],

)
