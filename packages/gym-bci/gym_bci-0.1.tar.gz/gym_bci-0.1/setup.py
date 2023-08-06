import os
from setuptools import setup
#from distutils.core import setup

# with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
#    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

version_str = open(os.path.join('gym_bci', '_version.txt'), 'r').read().strip()

setup(
    name='gym_bci',
    version=version_str,
    packages=['gym_bci'],

    author='Yeison Cardona',
    author_email='yeisoneng@gmail.com',
    maintainer='Yeison Cardona',
    maintainer_email='yeisoneng@gmail.com',

    # url='http://yeisoncardona.com/',
    download_url='https://bitbucket.org/gcpds/gym_bci/downloads/',

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
    description="GCPDS: gym-bci",
    #    long_description = README,

    classifiers=[

    ],

)
