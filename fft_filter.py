# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FFTConvolution
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
from __future__ import absolute_import
from builtins import range
from builtins import object
from qgis.PyQt.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QFileInfo
from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox
from qgis.PyQt.QtGui import QIcon
#from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QFileInfo
#from PyQt4.QtGui import QAction, QIcon, QFileDialog, QMessageBox

# Initialize Qt resources from file resources.py
#import resources
from . import resources

# Import the code for the dialog
#from fft_filter_dialog import FFTConvolutionDialog
from .fft_filter_dialog import FFTConvolutionDialog
import os.path
from qgis.core import *
import qgis.utils
from qgis.gui import *
import rasterio
import rasterio.env
from rasterio.warp import calculate_default_transform, reproject, Resampling
import numpy as np
from scipy.signal import fftconvolve
import math
import re

#class FFTConvolution:
class FFTConvolution(object):
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'FFTConvolution_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = FFTConvolutionDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&FFT COnvolution Filters')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'FFTConvolution')
        self.toolbar.setObjectName(u'FFTConvolution')
        
        self.dlg.output_file.clear()
        self.dlg.output_file_button.clicked.connect(self.select_output_file)

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('FFTConvolution', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToRasterMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/FFTConvolution/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'FFT Convolution filters'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginRasterMenu(
                self.tr(u'&FFT COnvolution Filters'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def select_output_file(self):
        #filename = QFileDialog.getSaveFileName(self.dlg, "Select output file ","", '*.tif')
        filename, __ = QFileDialog.getSaveFileName(self.dlg, "Select output file ","", '*.tif')
        #filename, __, __ = QFileDialog.getSaveFileName(self.dlg, "Select output file ","", '*.tif')
        self.dlg.output_file.setText(filename)


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            if self.dlg.smoothing.isChecked():
                edge = False
            else:
                edge = True
            #call the function linking to real work
            #the input is translated from the GUI input to correct format here
            self.fft_convolution(
                in_layer=self.dlg.input_layer.currentLayer(),
                out_path=self.dlg.output_file.text(),
                size=self.dlg.size.text(),
                edge=edge,
                new_crs=self.dlg.crs.crs(),
                tiled=self.dlg.window.isChecked(),
                tilerows=self.dlg.window_rows.text(),
                tilecols=self.dlg.window_cols.text(),
                add_layer=self.dlg.check_add.isChecked()
            )

    #this function parses the arguments, calls the appropriate functions and displays the new layer if needed
    def fft_convolution( self, in_layer, out_path, size=10, edge=False, new_crs=None, 
                         tiled=False, tilerows=0, tilecols=0, add_layer=True ):
        #if the file has no extension, add '.tif'
        ext = os.path.splitext(out_path)[-1].lower()
        if ext == '':
            out_path = out_path + '.tif'
        #if the file already exists, ask the user
        if os.path.isfile(out_path):
            reply = QMessageBox.question(
                None,'File exists!','File exists - overwite it?',
                QMessageBox.Yes, QMessageBox.No
            )
            if reply == QMessageBox.No:
                return False
        #we need the CRS as EPSG code, or None if invalid
        if new_crs.isValid():
            new_crs = new_crs.authid()
        else:
            new_crs = None
        #preprocessing the input layer's path
        in_path = in_layer.dataProvider().dataSourceUri()
        #QMessageBox.information(None, "DEBUG:", str(in_path))
        if in_path.find('=') > -1:
            QMessageBox.information(None, "Sorry!", "WMS support wasn't implemented yet!")
            return False
        #the main computation
        layer = self.gaussian_filter(
            in_path = in_path,
            out_path=out_path,
            size = int(re.sub(r"\D", "", size)),
            edge=edge, 
            tiled = tiled,
            tilerows = tilerows,
            tilecols = tilecols, 
            new_crs = new_crs
        )
        if add_layer:
            #QgsMapLayerRegistry.instance().addMapLayers([layer])
            QgsProject.instance().addMapLayers([layer])
            qgis.utils.iface.mapCanvas().refresh()

    #returns number of array dimensions
    def __array_rank(self, arr):
        return len(arr.shape)

    #loads the newly created layer
    def __load_layer(self, path):
        fileName = path
        fileInfo = QFileInfo(fileName)
        baseName = fileInfo.baseName()
        rlayer = QgsRasterLayer(fileName, baseName)
        if not rlayer.isValid():
            raise Exception("Computation finished, but layer failed to load. Inspect the path zou specified for the output layer.")
        return rlayer

    #pads the window to process its original extend accurately
    def __extend_window(self, window,size,height,width):
        minrow = max(window[0][0]-size,0)
        maxrow = min(window[0][1]+size,height)
        mincol = max(window[1][0]-size,0)
        maxcol = min(window[1][1]+size,width)
        return ((minrow,maxrow),(mincol,maxcol))

    #creates a window generator, in the same format as it is returned by block_windows method
    def __generate_windows(self, height, width, tilerows, tilecols):
        rownum = int(math.ceil(float(height)/tilerows))
        colnum = int(math.ceil(float(width)/tilecols))
        for i in range(rownum):
            #last row's and column's dimensions are computed by modulo - they are smaller than regular tiles
            if i == rownum-1:
                rowsize = height%tilerows
            else:
                rowsize = tilerows
            for j in range(colnum):
                if j == colnum-1:
                    colsize = width%tilecols
                else:
                    colsize = tilecols
                cell = ((i,j),((i*tilerows,i*tilerows+rowsize),(j*tilecols,j*tilecols+colsize)))
                yield cell

    #like __generate_windows(), but returns an array
    def __generate_window_array(self, height, width, tilerows, tilecols):
        rownum = int(math.ceil(float(height)/tilerows))
        colnum = int(math.ceil(float(width)/tilecols))
        windows = np.asarray(np.zeros((height, width),dtype=object))
        for i in range(rownum):
            #last row's and column's dimensions are computed by modulo - they are smaller than regular tiles
            if i == rownum-1:
                rowsize = height%tilerows
            else:
                rowsize = tilerows
            for j in range(colnum):
                if j == colnum-1:
                    colsize = width%tilecols
                else:
                    colsize = tilecols
                windows[i][j]=((i*tilerows,i*tilerows+rowsize),(j*tilecols,j*tilecols+colsize))
        return windows

    #processes the window parameters
    #returns the windows as a generator or an array (specified in the generator parameter)
    def __compute_windows(self, in_raster, height, width, size, tilerows=0, tilecols=0, generator=True):
        #input validation
        size = int(size)
        try:
            tilerows = int(tilerows)
        except ValueError:
            tilerows = 0
        try:
            tilecols = int(tilecols)
        except ValueError:
            tilecols = 0
        #when raster's dimensions are modified due to reprojection, we must adjust the windows as well
        #this algorithm is quick'n'dirty - we just sompute one ratio and make all tiles larger/smaller
        #reprojecting each tile node would be better - perhaps in some future version
        if height != in_raster.height or width != in_raster.width:
            hratio = float(height)/in_raster.height
            wratio = float(width)/in_raster.width
        else:
            hratio = 1
            wratio = 1
        
        windows = []
        #if only one of tile's dimension was set, we assume a square
        if tilecols == 0 and tilerows > 0:
            tilecols = tilerows
        elif tilerows == 0 and tilecols > 0:
            tilerows = tilecols
        #if tiles are too small (including default 0 length), we make them automatically
        #"2*size" is the total padding length and also an arbitrarily chosen minimum
        #"size" would be a minimum to get accurate tiles, but this way only 1/9 of the tile would be useful => inefficient
        #"2*size" means at least 50% efficiency
        if min(tilerows, tilecols) <= 2*size:
            #if the raster has blocks and they are big enough, we use them
            blocks = in_raster.block_shapes
            block = blocks[0]
            if min(block[0],block[1]) > 2*size:
                #if we compute the original raster, use the block as-is
                #otherwise use the dimensions and continue
                if hratio==1 and wratio==1:
                    return in_raster.block_windows(1)
                else:
                    tilerows = block[0]
                    tilecols = block[1]
            else:
                #"2*size + 100" is an arbitrary constant
                #it's quite efficient on smaller rasters and shouldn't make any memory issues
                #really small rasters shouldn't be computed by tiles anyway
                tilerows = 2*size + 100
                tilecols = 2*size + 100
        #we transform the dimensions if needed
        tilerows = int(hratio * tilerows)
        tilecols = int(wratio * tilecols)
        #if the tiles are too big (more than half of any dimension of the raster),
        #we switch to the untiled algorithm
        if 2*tilerows >= height or 2*tilecols >= width:
            return False
        #if windows are not read from the raster, we must make them
        if generator:
            windows = self.__generate_windows(height, width, tilerows, tilecols)
        else:
            windows = self.__generate_window_array(height, width, tilerows, tilecols)
        return windows

    #computes the affine transformation, raster dimensions and metadata for the new raster
    def __compute_transform(self, in_raster, new_crs):
        affine, width, height = calculate_default_transform(
            in_raster.crs, new_crs, in_raster.width, in_raster.height, *in_raster.bounds
        )
        kwargs = in_raster.meta.copy()
        kwargs.update({
            'driver':'GTiff',
            'crs': new_crs,
            'transform': affine,
            'affine': affine,
            'width': width,
            'height': height
        })
        return affine, height, width, kwargs

    #calls reproject() function for every band
    def __reproject(self, in_raster, out_raster, affine, new_crs):
        for k in range(1, in_raster.count + 1):
            reproject(
                source=rasterio.band(in_raster, k),
                destination=rasterio.band(out_raster, k),
                src_transform=affine,
                src_crs=in_raster.crs,
                dst_transform=affine,
                dst_crs=new_crs,
                resampling=Resampling.nearest)
        return out_raster

    #the original MikeT's function from http://gis.stackexchange.com/a/10467
    #my addition is the conversion of the padded array to float to avoid errors with integer rasters
    #the intended input is a single band raster array
    def __gaussian_blur1d(self, in_array, size):
        #check validity
        try:
            if 0 in in_array.shape:
                raise Exception("Null array can't be processed!")
        except TypeError:
            raise Exception("Null array can't be processed!")
        # expand in_array to fit edge of kernel
        padded_array = np.pad(in_array, size, 'symmetric').astype(float)
        # build kernel
        x, y = np.mgrid[-size:size + 1, -size:size + 1]
        g = np.exp(-(x**2 / float(size) + y**2 / float(size)))
        g = (g / g.sum()).astype(float)
        # do the Gaussian blur
        out_array = fftconvolve(padded_array, g, mode='valid')
        return out_array.astype(in_array.dtype)

    #the intended input is an array with various number of bands
    #returns a numpy array
    def __gaussian_blur(self, in_array, size):
        #make sure the input is a numpy array
        in_array = np.asarray(in_array)
        #find number of dimensions - 2 for single-band or 3 for multiband rasters
        rank = self.__array_rank(in_array)
        if rank == 2:
            return self.__gaussian_blur1d(in_array, size).astype(in_array.dtype)
        elif rank > 3 or rank == 1:
            raise TypeError("Invalid number of dimensions!")
        #continue to multiband
        count = in_array.shape[0]
        out = []
        for i in range(count):
            band = in_array[i]
            out_band = self.__gaussian_blur1d(band, size)#.astype(in_array.dtype)
            #if out_band != False:
            out.append( out_band )
        return np.asarray(out)

    #the real work is done here
    #filters a raster specified by the file's path (in_path) and writes it to another file (out_path)
    def gaussian_filter(self, in_path, out_path, size, edge=False, tiled=False, tilerows=0, tilecols=0, new_crs=None):
		with rasterio.Env():
		#with rasterio.drivers():
			with rasterio.open(in_path,'r') as in_raster:
				if new_crs == None:
					new_crs = in_raster.crs
				affine, height, width, kwargs = self.__compute_transform(in_raster, new_crs)
				if tiled:
					#we make two sets of tiles, for the old and the new raster
					#this is important in case of reprojection
					old_windows = self.__compute_windows(
						in_raster=in_raster,
						height=in_raster.height,
						width=in_raster.width,
						size=size,
						tilerows=tilerows,
						tilecols=tilecols
					)
					#windows for the new raster are made in two steps: generator and array
					new_windows = self.__compute_windows(
						in_raster=in_raster,
						height=height,
						width=width,
						size=size,
						tilerows=tilerows,
						tilecols=tilecols,
						generator=False
					)
					#if windows are too big or invalid, we process the raster without them
					try:
						iter(old_windows)
						iter(new_windows)
					except TypeError:
						tiled = False
				with rasterio.open(out_path,'w',**kwargs) as out_raster:
					out_raster = self.__reproject(in_raster, out_raster, affine, new_crs)
					if tiled:
						for index, window in old_windows:
							oldbigwindow = self.__extend_window(window,size,in_raster.height,in_raster.width)
							in_array = in_raster.read(window=oldbigwindow)
							out_array = self.__gaussian_blur(in_array, size)
							#for edge detection we subtract the output array from the original
							#this may produce some artifacts when the raster is reprojected
							#or extensive and with degree coordinates
							if edge:
								out_array = np.subtract(in_array, out_array)
							#now compute the window for writing into the new raster
							nwindow = new_windows[index[0]][index[1]]
							newbigwindow = self.__extend_window(nwindow,size,height,width)
							out_raster.write(out_array,window=newbigwindow)
					else:
						in_array = in_raster.read()
						out_array = self.__gaussian_blur(in_array, size)
						if edge:
							out_array = out_array = np.subtract(in_array, out_array)
						out_raster.write(out_array)
		return self.__load_layer(out_path)
