----------------------------------------
Glymur: a Python interface for JPEG 2000
----------------------------------------

**Glymur** is an interface to the OpenJPEG library
which allows one to read and write JPEG 2000 files from Python.  
Glymur supports both reading and writing of JPEG 2000 images, but writing
JPEG 2000 images is currently limited to images that can fit in memory.
**Glymur** can read images using OpenJPEG library versions as far back as 1.3,
but it is strongly recommended to use at least version 2.1.2.

In regards to metadata, most JP2 boxes are properly interpreted.
Certain optional JP2 boxes can also be written, including XML boxes and
XMP UUIDs.  There is incomplete support for reading JPX metadata.

Glymur will look to use **lxml** when processing boxes with XML content, but can
fall back upon the standard library's **ElementTree** if **lxml** is not
available.

Glymur works on Python versions 2.7, 3.5, 3.6, 3.7, and 3.8.

For more information about OpenJPEG, please consult http://www.openjpeg.org.

Glymur Installation
===================
The easiest way to install Glymur is via Anaconda using conda-forge ::

    $ conda create -n testglymur -c conda-forge python glymur
    $ conda activate testglymur
