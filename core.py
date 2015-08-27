import rasterio
from rasterio.warp import calculate_default_transform, reproject, RESAMPLING
import numpy as np
from scipy.signal import fftconvolve
import math


#returns number of array dimensions
def array_rank(arr):
	return len(arr.shape)

#pads the window to process its original extend accurately
def extend_window(window,size,height,width):
	minrow = max(window[0][0]-size,0)
	maxrow = min(window[0][1]+size,height-1)
	mincol = max(window[1][0]-size,0)
	maxcol = min(window[1][1]+size,width-1)
	return ((minrow,maxrow),(mincol,maxcol))

#creates a window generator, in the same format as it is returned by block_windows method
def generate_windows(height, width, tilerows, tilecols):
	rownum = int(math.ceil(float(height)/tilerows))
	colnum = int(math.ceil(float(width)/tilecols))
	
	for i in range(rownum):
		if i == rownum-1:
			rowsize = height%tilerows
		else:
			rowsize = tilerows-1
		for j in range(colnum):
			if j == colnum-1:
				colsize = width%tilecols
			else:
				colsize = tilecols-1
				cell = ((i,j),((i*tilerows,i*tilerows+rowsize),(j*tilecols,j*tilecols+colsize)))
				yield cell

#original MikeT's function from http://gis.stackexchange.com/a/10467/12768
#my addition is the conversion of the padded array to float to avoid errors with integer rasters
#the intended input is a single band raster array
def gaussian_blur1d(in_array, size):
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
#if as_np_array is true, returns numpz array, otherwise returns a list
def gaussian_blur_array(in_array, size, as_np_array=True):
	in_array = np.asarray(in_array)
	rank = array_rank(in_array)
	if rank == 2:
		return gaussian_blur1d(in_array, size).astype(in_array.dtype)
	elif rank > 3 or rank == 1:
		raise TypeError("Invalid number of dimensions!")
	#else continue
	count = in_array.shape[0]
	out = []
	for i in range(count):
		band = in_array[i]
		out_band = gaussian_blur1d(band, size).astype(in_array.dtype)
		out.append( out_band )
	if as_np_array:
		return np.asarray(out)
	else:
		return out

#smooths a raster specified by the file's path (in_path) and writes it to another file (out_path)
def gaussian_blur(in_path, out_path, size, tilerows=0, tilecols=0, new_crs=None, tiled=False):
	if tiled:
		return gaussian_blur_tiled(in_path, out_path, size, tilerows, tilecols, new_crs)
	with rasterio.drivers():
		with rasterio.open(in_path,'r') as in_raster:
			if new_crs == None:
				new_crs = in_raster.crs
			affine, width, height = calculate_default_transform(
				in_raster.crs, new_crs, in_raster.width, in_raster.height, *in_raster.bounds)
			kwargs = in_raster.meta.copy()
			kwargs.update({
				'driver':'GTiff',
				'crs': new_crs,
				'transform': affine,
				'affine': affine,
				'width': width,
				'height': height
			})
			with rasterio.open(out_path,'w',**kwargs) as out_raster:
				for k in range(1, in_raster.count + 1):
					reproject(
						source=rasterio.band(in_raster, k),
						destination=rasterio.band(out_raster, k),
						src_transform=affine,
						src_crs=in_raster.crs,
						dst_transform=affine,
						dst_crs=new_crs,
						resampling=RESAMPLING.nearest)
				in_array = in_raster.read()
				out_array = gaussian_blur_array(in_array, size)
				out_raster.write(out_array)
	return True

#version of gaussian_blur function using window-processing to speed up the process for large rasters
#windows are padded to avoid window/processing artifacts
def gaussian_blur_tiled(in_path, out_path, size, tilerows=0, tilecols=0, new_crs=None):
	with rasterio.drivers():
		with rasterio.open(in_path,'r') as in_raster:
			windows = []
			if tilecols == 0 and tilerows > 0:
				tilecols = tilerows
			tilesize = min(tilerows, tilecols)
			if tilesize <= 2*size:
				blocks = in_raster.block_shapes
				block = blocks[0]
				if min(block[0],block[1]) > 2*size:
					windows = in_raster.block_windows(1)
					tilesize = min(block[0],block[1])
				else:
					tilerows = 2*size + 100
					tilecols = 2*size + 100
			#if windows are not read from the raster, we must make them
			if new_crs == None:
				new_crs = in_raster.crs
			affine, width, height = calculate_default_transform(
				in_raster.crs, new_crs, in_raster.width, in_raster.height, *in_raster.bounds)
			if windows == []:
				if 2*tilerows > height or 2*tilecols > width:
					return gaussian_blur(in_path, out_path, size, tilerows, tilecols, new_crs, tiled=False)
				windows = generate_windows(height, width, tilerows, tilecols)
			
			kwargs = in_raster.meta.copy()
			kwargs.update({
				'driver':'GTiff',
				'crs': new_crs,
				'transform': affine,
				'affine': affine,
				'width': width,
				'height': height
			})
			with rasterio.open(out_path,'w',**kwargs) as out_raster:
				for k in range(1, in_raster.count + 1):
					reproject(
						source=rasterio.band(in_raster, k),
						destination=rasterio.band(out_raster, k),
						src_transform=affine,
						src_crs=in_raster.crs,
						dst_transform=affine,
						dst_crs=new_crs,
						resampling=RESAMPLING.nearest)
				for index, window in windows:
					bigwindow = extend_window(window,size,height,width)
					in_array = in_raster.read(window=bigwindow)
					out_array = gaussian_blur_array(in_array, size)
					out_raster.write(out_array,window=bigwindow)
	return True

#edge detection based on subtraction of the result of gaussian_blur function from the original raster
def gaussian_sharpen(in_path, out_path, size, tilerows=0, tilecols=0, new_crs=None, tiled=False):
	if tiled:
		return gaussian_sharpen_tiled(in_path, out_path, size, tilerows, tilecols, new_crs)
	with rasterio.drivers():
		with rasterio.open(in_path,'r') as in_raster:
			if new_crs == None:
				new_crs = in_raster.crs
			affine, width, height = calculate_default_transform(
				in_raster.crs, new_crs, in_raster.width, in_raster.height, *in_raster.bounds)
			kwargs = in_raster.meta.copy()
			kwargs.update({
				'driver':'GTiff',
				'crs': new_crs,
				'transform': affine,
				'affine': affine,
				'width': width,
				'height': height
			})
			with rasterio.open(out_path,'w',**kwargs) as out_raster:
				for k in range(1, in_raster.count + 1):
					reproject(
						source=rasterio.band(in_raster, k),
						destination=rasterio.band(out_raster, k),
						src_transform=affine,
						src_crs=in_raster.crs,
						dst_transform=affine,
						dst_crs=new_crs,
						resampling=RESAMPLING.nearest)
				in_array = in_raster.read()
				inter_array = gaussian_blur_array(in_array, size)
				out_array = np.subtract(in_array, inter_array)
				out_raster.write(out_array)
	return True

#window-processed version of gaussian_sharpen
def gaussian_sharpen_tiled(in_path, out_path, size, tilerows=0, tilecols=0, new_crs=None):
	with rasterio.drivers():
		with rasterio.open(in_path,'r') as in_raster:
			windows = []
			if tilecols == 0 and tilerows > 0:
				tilecols = tilerows
			tilesize = min(tilerows, tilecols)
			if tilesize <= 2*size:
				blocks = in_raster.block_shapes
				block = blocks[0]
				if min(block[0],block[1]) > 2*size:
					windows = in_raster.block_windows(1)
					tilesize = min(block[0],block[1])
				else:
					tilerows = 2*size + 100
					tilecols = 2*size + 100
			#if windows are not read from the raster, we must make them
			if new_crs == None:
				new_crs = in_raster.crs
			affine, width, height = calculate_default_transform(
				in_raster.crs, new_crs, in_raster.width, in_raster.height, *in_raster.bounds)
			if windows == []:
				if 2*tilerows > height or 2*tilecols > width:
					return gaussian_blur(in_path, out_path, size, tilerows, tilecols, new_crs, tiled=False)
				windows = generate_windows(height, width, tilerows, tilecols)
			
			kwargs = in_raster.meta.copy()
			kwargs.update({
				'driver':'GTiff',
				'crs': new_crs,
				'transform': affine,
				'affine': affine,
				'width': width,
				'height': height
			})
			with rasterio.open(out_path,'w',**kwargs) as out_raster:
				for k in range(1, in_raster.count + 1):
					reproject(
						source=rasterio.band(in_raster, k),
						destination=rasterio.band(out_raster, k),
						src_transform=affine,
						src_crs=in_raster.crs,
						dst_transform=affine,
						dst_crs=new_crs,
						resampling=RESAMPLING.nearest)
				for index, window in windows:
					bigwindow = extend_window(window,size,height,width)
					in_array = in_raster.read(window=bigwindow)
					inter_array = gaussian_blur_array(in_array, size)
					out_array = np.subtract(in_array, inter_array)
					out_raster.write(out_array,window=bigwindow)
	return True
