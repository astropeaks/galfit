# -*- coding: utf-8 -*-
#This script takes your data and cuts out a star for PSF creation.

from astropy.io import fits
from astropy import wcs
import matplotlib.pyplot as plt

#Input Parameters: CHANGE STUFF HERE using info from the header. Keep NCOMBINE = 1.0
filename = 'RGG058.fits'
gain = 2.5
exptime = 972.183470000001
NCOMBINE = 1.0
photflam = 1.5274129E-20
newgain = 1/photflam
f = fits.open(filename)
w = wcs.WCS(f[1].header)

#Set the coordinates of each corner of the square you want to cut out.
xmin = 232
xmax = 314
ymin = 41
ymax = 123

newf1 = fits.PrimaryHDU()
newf1.header.append(('GAIN',newgain, 'commanded gain of CCD'))
newf1.header.append(('EXPTIME', exptime, 'exposure duration (seconds)--calculated'))
newf1.header.append(('NCOMBINE',1,'number of image sets combined during CR rejecti'))
newf1.header.append(('photflam',photflam,'inverse sensitivity, ergs/cm2/Ang/electron'))
newf1.data = f[1].data[ymin:ymax,xmin:xmax]
newf1.header.update(w[ymin:ymax,xmin:xmax].to_header())

newf1.data = newf1.data*exptime*photflam
plt.imshow(newf1.data)

newf1.header['BUNIT'] = 'ergs/cm2/ang'

newf1.header
newf1.writeto('starpsf.fits')
