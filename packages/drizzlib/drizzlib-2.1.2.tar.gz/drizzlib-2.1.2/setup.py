import numpy  # <- forces us to install numpy BEFORE drizzlib. Help?

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

# Read the version number from the VERSION file
from os.path import abspath, dirname, join

with open(join(dirname(abspath(__file__)), 'VERSION'), 'r') as version_file:
    version = version_file.read().strip()

# Set up our C extension
optimized_module = Extension(
    'optimized',
    sources=[
        'src/optimized.c',
    ],
    include_dirs=[numpy.get_include()]
)

setup(
    name='drizzlib',
    version=version,
    author='Deborah Paradis',
    author_email='deborah.paradis@irap.omp.eu',
    maintainer='Jean-Michel Glorian',
    maintainer_email='jean-michel.glorian@irap.omp.eu',
    url='https://gitlab.irap.omp.eu/cade/drizzlib-python',
    license='CECILL v2.1',
    description="Drizzlib is a drizzling module to convert from HEALPIX to "
                "WCS FITS files.",
    ext_modules=[optimized_module],
    # Redundancy with requirements.txt because ... pip T_T
    install_requires=['numpy>=1.16.4', 'matplotlib==3.0.3', 'astropy>=3.2.1', 'scipy>=1.3.0', 'healpy>=1.12.9',
                      'reproject>=0.4', 'six>=1.12.0'],
    requires=['numpy', 'matplotlib', 'astropy', 'scipy', 'healpy', 'reproject', 'six'],
    ###
    packages=['drizzlib'],
    package_dir={'drizzlib': 'lib'},
    provides=['drizzlib'],
    scripts=['bin/healpix2wcs']

)
