********************************************************************************
********************************************************************************
****                                                                        ****
****                        FFT CONVOLUTION                                 ****
****                         version 0.1.2                                  ****
****                                                                        ****
********************************************************************************
********************************************************************************

FFT Convolution is a plugin for raster smoothing and edge detection based on fftconvolve() SciPy function, as included in the gaussian_blur() function by MikeT (http://gis.stackexchange.com/a/10467). The edge detection is implemented by subtracting the smoothed raster from the original one.

Larger rasters may be processed using a windowed or tiled algorithm, which is faster than plain one for them, but may lead to some artifacts. These should be minimal and irrelevant for most tasks.

DOCUMENTATION

For minimal documentation, see documentation.html.

BUGTRACKER

https://github.com/PavelVeselsky/fft-convolution-filter/issues

NOT IMPLEMENTED YET

Version 0.1.1 allows user to process rasters in any CRS and also to reproject the raster in the process, but reprojection or processing rasters in geographic CRSs may lead to inaccuracies, especially when using tiled algorithm or edge detection.
Ungeoreferenced rasters are not supported at all.

LICENSE

FFT Convolution plugin is a free software distributed under GNU General Public License version 3.0 as published by the Free Software Foundation. See LICENSE.txt for details.

ACKNOWLEDGEMENT

First I want to thank MikeT for the function that became a foundation stone of this plugin.

Second, to Giovanni Manghi for pointing to it in the Python Plugin Ideas page (http://hub.qgis.org/projects/quantum-gis/wiki/Python_Plugin_Ideas) and thus inspiring me to make this plugin.
