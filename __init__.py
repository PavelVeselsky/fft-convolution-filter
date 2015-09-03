# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FFTConvolution
                                 A QGIS plugin
 Smoothing and edge detection based on fftconvolve() SciPy function
                             -------------------
        begin                : 2015-08-27
        copyright            : (C) 2015 by Pavel Veselský
        email                : pavelveselsky@seznam.cz
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load FFTConvolution class from file FFTConvolution.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .fft_filter import FFTConvolution
    return FFTConvolution(iface)
