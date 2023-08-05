DRIZZLIB
========

This is a [HEALPIx] to [WCS] FITS conversion python package.
You can extract a rectangular subset of the [HEALPIx] image into the [WCS]
format with the frame, projection and resolution of your choosing.

It's work on python `3`


[HEALPIx]:   http://healpix.jpl.nasa.gov
[WCS]:       http://fits.gsfc.nasa.gov/fits_wcs.html
[drizzling]: http://en.wikipedia.org/wiki/Drizzle_(image_processing)
[pip]:       http://www.pip-installer.org


HOW TO INSTALL
==============

Using pip
---------

This is the simplest way to install `drizzlib` if you do not want to edit its
source and just use it as-is.

    pip install numpy
    pip install drizzlib

You need to install `numpy` first because we're linking to some of its C
extensions _during_ the setup of drizzlib.
If you know of a way to avoid this, please tell us how.


From sources
------------

### Downloading

Get the source files with Git or by downloading the archive, then go to this
directory.


### Installing dependencies

`drizzlib` requires several python packages ()such as `numpy`, `astropy`, or
`healpy`) defined in *requirements.txt* in order to install them with [pip].
You can use a virtual environment or not depending on your needs.


#### Using a virtual environment

Create the virtual environment, then install dependencies:

```
python3 -m venv /path/to/venv
source /path/to/venv/bin/activate
pip install -r requirements.txt
```


#### Without a virtual environment

As a user:

```
pip install --user -r requirements.txt
```

Or as a root:

```
pip install -r requirements.txt
```

### Install

#### Using a virtual environment

```
python setup.py install
```

#### Without a virtual environment

As a user:

```
python setup.py install --usecd r
```

Or as root:

```
sudo python setup.py install
```


### Install for development

You can use pip to install the package and yet keep it editable :

```
pip install --editable .
```


Troubleshooting
---------------

- `The following required packages can not be built: freetype, png`
  Older versions of healpy require old matplotlib that requires freetype :
  `sudo apt-get install pkg-config libfreetype*`

- `fatal error: Python.h`
  You need python's development packages, too :
  `sudo apt-get install python-dev`

- `no lapack/blas resources found`
  On Debian-based systems, install the following system packages :
  `sudo apt-get install gfortran libopenblas-dev liblapack-dev`

- `UnicodeEncodeError`
  Make sure the directory in which you uncompressed drizzlib does not contain
  non-ascii characters in its path.


HOW TO USE
==========

As a library
------------

See `doc/TUTORIAL.md` for a more extensive example.

``` python
from drizzlib import healpix2wcs

# Reads `my_healpix.fits`, extracts a subset of its data described by the
# header in `wcs_config.fits`, and writes the result into `my_wcs.fits`.
healpix2wcs('my_healpix.fits', header='wcs_config.fits', output='my_wcs.fits')
```


As a binary
-----------

In the shell, run :

```
$ bin/healpix2wcs -h
```

or, if you installed the package, simply :

```
$ healpix2wcs -h
```

It will show you how to use it, which is like this:

```
$ healpix2wcs [-h] [-f] <healpix> <header> <out>
```


HOW TO DISTRIBUTE
=================

Bump the `VERSION`, and then run :

```
$ python setup.py sdist
```

It will create a source distribution tarball in the `dist` directory.
It uses `MANIFEST.in` to exclude files we want to exclude.


GUIDELINES
==========

Versioning
----------

We use [semantic versioning](http://semver.org/).

Code formatting
---------------

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/).

Documentation
-------------

Write your documentation in
[Markdown](https://daringfireball.net/projects/markdown/).


CHANGELOG
=========

2.1.2
---
- Call create_wcs_header as a function, not as a variable

2.1.1
---
- Fix bug with the function create_wcs_header

2.1
---
- [healpix2wcs] split in several parts the function
- Add a warning to extract linear map

2.0
---
- new version using python3
- possibility to extract files with several columns

1.2.6.3
-------
- reduce logs in order to fix a bug with large images.

1.2.6.2
-------
- fix bug of inverted crpix1 and crpix2 

1.2.6.1
-------

- fix bug if not car projection

1.2.6
-----
- fix bug in the order of the x,y image size
- add optimization with CAR projection

1.2.5
-----

- add several projections

1.2.4
-----

- Improve partial healpix computation

1.2.3
-----

- minor changes

1.2.2
-----

- Fix bug for the computation of sigma healpix map

1.2.1
-----

- Fix pip dependencies in the setup script.


1.2.0
-----

- Set up python 3 compatibility. (hopefully)
- Add an `is_sigma` parameter for noise maps in `healpix2wcs`.


1.0.1
-----

- Fix the source distribution.


1.0.0
-----

- Initial release of `healpix2wcs`.
- Fix all of the bugs©.


0.5.0
-----

- Basic `wcs2healpix`.


0.4.0
-----

- Add a `healpix2wcs` executable.
- [healpix2wcs] Fix some more bugs.
- [healpix2wcs] Ignore `BLANK` values in input HEALPix.


0.3.0
-----

- Embark a Sutherland-Hodgman clipping algorithm written in C, to optimize further.


0.2.0
-----

- Optimize a lot thanks to the `line_profiler`.


0.1.0
-----

- [healpix2wcs] Initial project skeleton files.
- [healpix2wcs] Non-optimized conversion using `healpy`.


THE SCIENCE
===========

Related Papers
--------------

TODO: @Deborah, reference your paper(s) here.


Healpix
-------

Learn more about the awesome HEALPix pixelation here :
http://healpix.sourceforge.net/


Drizzling
---------

Learn more about [drizzling].

Here are some polygon clipping algorithms:

- We're using: http://en.wikipedia.org/wiki/Sutherland%E2%80%93Hodgman_algorithm
- Faster: http://en.wikipedia.org/wiki/Cohen%E2%80%93Sutherland_algorithm
- Even faster : http://en.wikipedia.org/wiki/Liang%E2%80%93Barsky_algorithm


