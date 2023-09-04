********************************************************************************
********************************************************************************
****                                                                        ****
****                        FFT CONVOLUTION                                 ****
****                         version 0.2.15                                  ****
****                                                                        ****
********************************************************************************
********************************************************************************

FFT Convolution is a QGis 3 plugin for raster smoothing and edge detection based on fftconvolve() SciPy function, as included in the gaussian_blur() function by MikeT (http://gis.stackexchange.com/a/10467). The edge detection is implemented by subtracting the smoothed raster from the original one.

Larger rasters may be processed using a windowed or tiled algorithm, which is faster than plain one for them, but may lead to some artifacts. These should be minimal and irrelevant for most tasks.

DOCUMENTATION

For minimal documentation, see documentation.html.

BUGTRACKER

https://github.com/PavelVeselsky/fft-convolution-filter/issues

NOT IMPLEMENTED YET

Version 0.2.15 allows user to process rasters in any CRS and also to reproject the raster in the process, but reprojection or processing rasters in geographic CRSs may lead to inaccuracies, especially when using tiled algorithm or edge detection.
Ungeoreferenced rasters are not supported at all.
WMS raster layers are not supported.
The plugin should be available in the Processing toolbar as well, but is not.
The plugin was tested mainly on Ubuntu Linux. Only a few features were tested on Windows and OS X. If you will encounter an issue on any of those systems, write me or file an issue in the bugtracker.

LICENSE

FFT Convolution plugin is a free software distributed under GNU General Public License version 3.0 as published by the Free Software Foundation. See LICENSE.txt for details.

ACKNOWLEDGEMENT

First I want to thank MikeT for the function that became a foundation stone of this plugin.

Second, to Giovanni Manghi for pointing to it in the Python Plugin Ideas page (http://hub.qgis.org/projects/quantum-gis/wiki/Python_Plugin_Ideas) and thus inspiring me to make this plugin.
