# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fft_filter_dialog_base.ui'
#
# Created: Fri Aug 28 09:36:08 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_FFTConvolutionDialogBase(object):
    def setupUi(self, FFTConvolutionDialogBase):
        FFTConvolutionDialogBase.setObjectName(_fromUtf8("FFTConvolutionDialogBase"))
        FFTConvolutionDialogBase.resize(325, 450)
        self.button_box = QtGui.QDialogButtonBox(FFTConvolutionDialogBase)
        self.button_box.setGeometry(QtCore.QRect(0, 400, 301, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setObjectName(_fromUtf8("button_box"))
        self.input_label = QtGui.QLabel(FFTConvolutionDialogBase)
        self.input_label.setGeometry(QtCore.QRect(10, 20, 101, 17))
        self.input_label.setObjectName(_fromUtf8("input_label"))
        self.input_layer = gui.QgsMapLayerComboBox(FFTConvolutionDialogBase)
        self.input_layer.setGeometry(QtCore.QRect(108, 10, 201, 27))
        self.input_layer.setObjectName(_fromUtf8("input_layer"))
        self.output_label = QtGui.QLabel(FFTConvolutionDialogBase)
        self.output_label.setGeometry(QtCore.QRect(10, 60, 101, 17))
        self.output_label.setObjectName(_fromUtf8("output_label"))
        self.output_file = QtGui.QLineEdit(FFTConvolutionDialogBase)
        self.output_file.setGeometry(QtCore.QRect(108, 50, 201, 27))
        self.output_file.setObjectName(_fromUtf8("output_file"))
        self.size_label = QtGui.QLabel(FFTConvolutionDialogBase)
        self.size_label.setGeometry(QtCore.QRect(160, 100, 41, 17))
        self.size_label.setObjectName(_fromUtf8("size_label"))
        self.size = QtGui.QLineEdit(FFTConvolutionDialogBase)
        self.size.setGeometry(QtCore.QRect(250, 90, 61, 27))
        self.size.setObjectName(_fromUtf8("size"))
        self.filter_type = QtGui.QLabel(FFTConvolutionDialogBase)
        self.filter_type.setGeometry(QtCore.QRect(10, 100, 141, 17))
        self.filter_type.setObjectName(_fromUtf8("filter_type"))
        self.edge_detection = QtGui.QRadioButton(FFTConvolutionDialogBase)
        self.edge_detection.setGeometry(QtCore.QRect(160, 130, 141, 22))
        self.edge_detection.setObjectName(_fromUtf8("edge_detection"))
        self.smoothing = QtGui.QRadioButton(FFTConvolutionDialogBase)
        self.smoothing.setGeometry(QtCore.QRect(10, 130, 116, 22))
        self.smoothing.setChecked(True)
        self.smoothing.setObjectName(_fromUtf8("smoothing"))
        self.optional = QtGui.QLabel(FFTConvolutionDialogBase)
        self.optional.setGeometry(QtCore.QRect(100, 170, 66, 17))
        self.optional.setObjectName(_fromUtf8("optional"))
        self.crs_label = QtGui.QLabel(FFTConvolutionDialogBase)
        self.crs_label.setGeometry(QtCore.QRect(10, 210, 41, 17))
        self.crs_label.setObjectName(_fromUtf8("crs_label"))
        self.CRS = gui.QgsProjectionSelectionWidget(FFTConvolutionDialogBase)
        self.CRS.setGeometry(QtCore.QRect(67, 200, 241, 27))
        self.CRS.setObjectName(_fromUtf8("CRS"))
        self.window = QtGui.QCheckBox(FFTConvolutionDialogBase)
        self.window.setEnabled(True)
        self.window.setGeometry(QtCore.QRect(10, 240, 301, 22))
        self.window.setObjectName(_fromUtf8("window"))
        self.rowlabel = QtGui.QLabel(FFTConvolutionDialogBase)
        self.rowlabel.setGeometry(QtCore.QRect(10, 280, 131, 17))
        self.rowlabel.setObjectName(_fromUtf8("rowlabel"))
        self.window_rows = QtGui.QLineEdit(FFTConvolutionDialogBase)
        self.window_rows.setEnabled(False)
        self.window_rows.setGeometry(QtCore.QRect(180, 270, 40, 27))
        self.window_rows.setObjectName(_fromUtf8("window_rows"))
        self.collabel = QtGui.QLabel(FFTConvolutionDialogBase)
        self.collabel.setGeometry(QtCore.QRect(10, 320, 121, 17))
        self.collabel.setObjectName(_fromUtf8("collabel"))
        self.window_cols = QtGui.QLineEdit(FFTConvolutionDialogBase)
        self.window_cols.setEnabled(False)
        self.window_cols.setGeometry(QtCore.QRect(180, 310, 40, 27))
        self.window_cols.setObjectName(_fromUtf8("window_cols"))
        self.CheckLoad = QtGui.QCheckBox(FFTConvolutionDialogBase)
        self.CheckLoad.setGeometry(QtCore.QRect(10, 360, 291, 22))
        self.CheckLoad.setChecked(True)
        self.CheckLoad.setObjectName(_fromUtf8("CheckLoad"))

        self.retranslateUi(FFTConvolutionDialogBase)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("accepted()")), FFTConvolutionDialogBase.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("rejected()")), FFTConvolutionDialogBase.reject)
        QtCore.QObject.connect(self.window, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.window_rows.setEnabled)
        QtCore.QObject.connect(self.window, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.window_cols.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(FFTConvolutionDialogBase)

    def retranslateUi(self, FFTConvolutionDialogBase):
        FFTConvolutionDialogBase.setWindowTitle(_translate("FFTConvolutionDialogBase", "FFT COnvolution Filters", None))
        self.input_label.setText(_translate("FFTConvolutionDialogBase", "Input Layer", None))
        self.output_label.setText(_translate("FFTConvolutionDialogBase", "Output File", None))
        self.size_label.setText(_translate("FFTConvolutionDialogBase", "Size", None))
        self.filter_type.setText(_translate("FFTConvolutionDialogBase", "Filter Type", None))
        self.edge_detection.setText(_translate("FFTConvolutionDialogBase", "Edge Detection", None))
        self.smoothing.setText(_translate("FFTConvolutionDialogBase", "Smoothing", None))
        self.optional.setText(_translate("FFTConvolutionDialogBase", "Optional", None))
        self.crs_label.setText(_translate("FFTConvolutionDialogBase", "CRS", None))
        self.window.setText(_translate("FFTConvolutionDialogBase", "Apply windowed algorithm", None))
        self.rowlabel.setText(_translate("FFTConvolutionDialogBase", "Window Rows", None))
        self.collabel.setText(_translate("FFTConvolutionDialogBase", "Window Columns", None))
        self.CheckLoad.setText(_translate("FFTConvolutionDialogBase", "Load Output Layer to Map", None))

from qgis import gui
