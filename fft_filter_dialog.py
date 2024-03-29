# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FFTConvolutionDialog
                                 A QGIS plugin
 Smoothing and edge detection based on fftconvolve() SciPy function
                             -------------------
        begin                : 2015-08-27
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Pavel Veselský
        email                : pavelveselsky@seznam.cz
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.PyQt import QtGui, QtWidgets, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'fft_filter_dialog_base.ui'))


class FFTConvolutionDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(FFTConvolutionDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        self.setupUi(self)
