********************************************************************************
********************************************************************************
****                                                                        ****
****                        FFT CONVOLUTION                                 ****
****                          version 0.1                                   ****
****                                                                        ****
********************************************************************************
********************************************************************************

FFT Convolution is a plugin for raster smoothing and edge detection based on fftconvolve() SciPy function, as included in the gaussian_blur() function by MikeT (http://gis.stackexchange.com/a/10467). The edge detection is implemented by subtracting the smoothed raster from the original one.

Larger rasters may be processed using a windowed or tiled algorithm, which is faster than plain one for them, but may lead to some artifacts. These should be minimal and irrelevant for most tasks.

BUGTRACKER

https://github.com/PavelVeselsky/fft-convolution-filter/issues

KNOWN ISSUES

Version 0.1 allows user to process rasters in any CRS and also to reproject the raster in the process, but reprojection or processing rasters in geographic CRSs may lead to inaccuracies, especially when using tiled algorithm or edge detection.
Ungeoreferenced rasters are not supported at all.

LICENSE

FFT Convolution plugin is a free software distributed under GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
