#!/usr/bin/env python
# coding: utf-8
#Author: Denis Varise Bernardes.
#Date: 04/04/2020. 

"""
This file contains the software of the Artificial Images Generator (AIG). The AIG was developed to create artificial star images,
simulating the star images acquired by the SPARC4 CCD cameras in astronomical observations. To create the images, the AIG models
the star flux distribution as a 2D-Gaussian Distribution. This result is added to a noise image, created based a set of parameters
provided to the software, as the CCD operation mode, the star flux and the sky flux. Figure below presents an example of an image
created by the AIG.

For more information, access https://github.com/DBernardes/Artificial-Images-Generator
"""



import astropy.io.fits as fits
import numpy as np
import matplotlib.pyplot as plt
import Read_Noise_Calc as RNC

from astropy.table import Table
from photutils.datasets import make_gaussian_prf_sources_image, make_gaussian_sources_image
from photutils.datasets import make_noise_image
from sys import exit
import os
import json

from collections import OrderedDict
from astropy.modeling.models import Moffat2D
from photutils.datasets import make_model_sources_image

class Artificial_Images_Generator:

    def __init__(self, star_flux, sky_flux, gaussian_stddev, ccd_operation_mode, ccd_temp=-70, serial_number=9916, bias_level=500, image_dir=''):
        #star flux in photons/s
        self.star_flux = star_flux
        #sky flux in photons/s
        self.sky_flux = sky_flux
        #standard deviaion of the 2D-Gaussian Distribution in pixels
        self.gaussian_stddev = gaussian_stddev
        #operation mode of the CCD.        
        self.ccd_operation_mode = ccd_operation_mode
        #CCD temperature. It should be between 0 ºC to -70 ºC  
        self.ccd_temp = ccd_temp
        #Serial number of the CCD. For the SPARC4 cameras, they would be 9914, 9915, 9916, or 9917.
        self.serial_number = serial_number        
        #Bias level in analogical-to digital units for the pixels of the created image
        self.bias_level = bias_level
        #Directory where the image should be saved
        if image_dir != '':        
            if '\\' not in image_dir[-1]: image_dir+='\\'
        self.image_dir = image_dir                
        #Name of the createde image. It is automatically generated.
        self.image_name = ''

        #Dark current of the CCD.        
        self.dark_current = 0
        #Read noise of the CCD.        
        self.read_noise = 0
        #Gain of the CCD in e-/ADU
        self.gain = 0
        #Image header
        self.hdr = []


    def write_image_mode(self):
        #This function writes the CCD operation to the class paramters.        
        self.em_mode = self.ccd_operation_mode['em_mode']
        self.noise_factor = 1
        self.em_gain = 1
        if self.em_mode == 1:
            self.noise_factor = 1.41            
            self.em_gain = self.ccd_operation_mode['em_gain']
        self.preamp = self.ccd_operation_mode['preamp']
        self.hss = self.ccd_operation_mode['hss']
        self.bin = self.ccd_operation_mode['bin']        
        self.t_exp = self.ccd_operation_mode['t_exp']        
        #Calculated the gain, dark current and the read noise of the CCD for the provided operation mode
        self.set_gain()          
        self.set_dc()        
        self.calc_RN()



    def set_gain(self):
        #This function sets the CCD gain based on the provided operation mode
        #The gain values in this function were obtained through the camera datasheet
        em_mode = self.em_mode
        hss = self.hss
        preamp = self.preamp
        gain = 0
        if em_mode == 1:
            if hss == 30:
                if preamp == 1:
                    gain = 17.2
                if preamp == 2:
                    gain = 5.27
            if hss == 20:
                if preamp == 1:
                    gain = 16.4
                if preamp == 2:
                    gain = 4.39
            if hss == 10:
                if preamp == 1:
                    gain = 16.0
                if preamp == 2:
                    gain = 3.96
            if hss == 1:
                if preamp == 1:
                    gain = 15.9
                if preamp == 2:
                    gain = 3.88
        else:
            if hss == 1:
                if preamp == 1:
                    gain = 3.37
                if preamp == 2:
                    gain = 0.8
            if hss == 0.1:
                if preamp == 1:
                    gain = 3.35
                if preamp == 2:
                    gain = 0.8
        self.gain = gain


    def set_dc(self):
        #This function calculates the dark current of the CCD.       
        T = self.ccd_temp
        if self.serial_number == 9914:
            self.dark_current = 24.66*np.exp(0.0015*T**2+0.29*T) 
        if self.serial_number == 9915:
            self.dark_current = 35.26*np.exp(0.0019*T**2+0.31*T)
        if self.serial_number == 9916:
            self.dark_current = 9.67*np.exp(0.0012*T**2+0.25*T)
        if self.serial_number == 9917:
            self.dark_current = 5.92*np.exp(0.0005*T**2+0.18*T)
            


    def calc_RN(self):
        #This function calls the ReadNoiseCalc library to calculate the read noise
        # of the CCD, based on the provided operation mode
        RN = RNC.ReadNoiseCalc()    
        RN.write_operation_mode(self.em_mode, self.em_gain, self.hss, self.preamp, self.bin)
        RN.calc_read_noise()        
        self.read_noise =  float(RN.noise)


    def create_image_header(self):
        #This function creates the image header based on the paramters provided to the class.
        hdr = fits.Header()                               
        hdr['NAXIS1']  =(200, 'length of data axis 1')
        hdr['NAXIS2']  =(200, 'length of data axis 2')                          
        hdr['EXTEND']  = ('T', 'FITS dataset may contain extensions')                                             
        hdr['COMMENT'] = 'and Astrophysics, volume 376, page 359; bibcode: 2001A&A...376..3'
        hdr['ACQMODE'] = ('Single  ', 'Acquisition Mode')
        hdr['READMODE']= ('Image   ', 'Readout Mode')
        hdr['IMGRECT'] = ('1, 200,200, 1', 'Image Format')
        hdr['HBIN']    = (self.bin, 'Horizontal Binning')
        hdr['VBIN']    = (self.bin,'Vertical Binning')
        hdr['TRIGGER'] = ('Internal','Trigger Mode')
        hdr['EXPOSURE']= (self.t_exp, 'Total Exposure Time')
        hdr['TEMP']    = (self.ccd_temp, 'Temperature')
        hdr['READTIME']= (str(1/self.hss)+'E-006' ,'Pixel readout time ')
        hdr['VSHIFT']  = ('4.33E-06', 'Vertical Shift Speed')
        hdr['GAIN']    = (self.gain, 'Preamp Gain (e-/ADU)')
        em_mode = 'Conventional'
        if self.em_mode == 1: em_mode = 'Electron Multiplying'
        hdr['OUTPTAMP']= (em_mode, 'Output Amplifier')
        hdr['EMGAIN'] = (self.em_gain, 'Electron Multiplying Gain')
        hdr['PREAMP']  = (str(self.preamp)+'x', 'Pre Amplifier Gain')
        hdr['SERNO']   = (self.serial_number, 'Serial Number')
        hdr['DATE']   = ('2017-07-14T00:00:58', 'File Creation Date (YYYY-MM-HHThh:mm:ss)')
        hdr['FRAME']   = ('2017-07-14T00:00:58.642', 'Start of Frame Exposure')
        hdr['IMAGE']  = ('hats-24_I_transito_001', 'Nome do arquivo')
        self.hdr = hdr


    def write_image_name(self):
        #This function creates the image name based on the provided operation mode
        em_gain = '_G' + str(self.em_gain)
        em_mode = 'CONV_'
        if self.em_mode == 1: em_mode = 'EM_'
        hss = str(self.hss) + 'MHz'
        preamp = '_PA' + str(self.preamp)
        binn = '_B' + str(self.bin)
        t_exp = '_TEXP'+ str(self.t_exp)
        star_flux = '_S'+ str(self.star_flux)
        
        self.image_name = em_mode + hss + preamp + binn + t_exp + em_gain #+ star_flux


    def create_artificial_image(self):
        #This function creates the artificial image.
        t_exp = self.t_exp
        em_gain = self.em_gain
        gain = self.gain
        bias = self.bias_level                
        dc = self.dark_current*t_exp
        rn = self.read_noise       
        sky = self.sky_flux
        nf = self.noise_factor
        binn = self.bin
        gaussian_stddev = self.gaussian_stddev

        #Calculation of the guassian amplitude based on the parameters provided to the software.        
        gaussian_amplitude = self.star_flux * t_exp * em_gain * binn**2 / gain
        #The create image has 200 x 200 pixels
        shape = (200, 200)
        table = Table()
        table['amplitude'] = [gaussian_amplitude]
        #X coordinate of the star
        table['x_mean'] = [100]
        #Y coordinate of the star
        table['y_mean'] = [100]
        #Standard devion of the Gaussian in X direction
        table['x_stddev'] = [gaussian_stddev/binn]
        #Standard devion of the Gaussian in Y direction
        table['y_stddev'] = [gaussian_stddev/binn]
        #Rotation angle of the Gaussian. It is fixed in zero.
        table['theta'] = np.radians(np.array([0]))
        #This command creates the 2D-Gaussiain Distribution
        star_image = make_gaussian_sources_image(shape, table)                


        #Calculation of the background level of the image.        
        background_level = bias + (dc + sky) * t_exp * em_gain * binn**2 / gain
        #Calculation of the image noise
        image_noise = np.sqrt(rn**2 + (sky + dc)*t_exp * nf**2 * em_gain**2 * binn**2)/gain               
        #This command creates a noise image with a Gaussian Distribution. This image has counts distribution
        # arround zero, for the noise calculated in the previous step.
        noise_image = make_noise_image(shape, distribution='gaussian', mean=background_level, stddev=image_noise)
        #Adds the noise image to the star image
        star_image+=noise_image
        #Save in FITS format
        fits.writeto(self.image_dir + self.image_name + '.fits', star_image, overwrite=True, header=self.hdr)


    def create_bias_image(self):
        #This function creates a bias image: image without light incidente.
        t_exp = 1e-5
        em_gain = self.em_gain
        gain = self.gain
        bias = self.bias_level
        rn = self.read_noise       
        binn = self.bin
        
        shape = (200, 200)               
        background_level = bias     
        image_noise = rn      
        noise_image = make_noise_image(shape, distribution='gaussian', mean=background_level, stddev=image_noise)/gain                
        fits.writeto(self.image_dir + self.image_name+ '_BIAS.fits', noise_image, overwrite=True, header=self.hdr)       


