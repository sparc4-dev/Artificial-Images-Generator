#!/usr/bin/env python
# coding: utf-8

# Este script cria uma imagem sintética, fornecido o modo de operação do CCD.
# Utiliza-se uma fonte constante de fótons, que são convertidos em ADU de
# acordo com o valor do ganho do CCD.
# É utilizada uma tabela de ruído de leitura e uma imagem de bias para
# adicionar ruído à imagem.

#04/04/2020. Denis Varise Bernardes.

import astropy.io.fits as fits
import numpy as np
import matplotlib.pyplot as plt
import Read_Noise_Calculation_Bib as RNC

from astropy.table import Table
from photutils.datasets import make_gaussian_prf_sources_image, make_gaussian_sources_image
from photutils.datasets import make_noise_image
from sys import exit
import os
import json

from collections import OrderedDict
from astropy.modeling.models import Moffat2D
from photutils.datasets import make_model_sources_image

class Create_Synthetic_Images:

    def __init__(self, ccd_temp, serial_number, star_amplitude, sky_flux, bias_name, image_dir, image_sigma):       

        self.ccd_temp = ccd_temp
        self.serial_number = serial_number
        self.image_name = ''   
        if '.fits' not in bias_name: bias_name+='.fits'
        self.bias_name = bias_name
        if '\\' not in image_dir[-1]: image_dir+='\\'
        self.image_dir = image_dir
        self.bias_level = 0     
        
        self.sky_flux = sky_flux #e-/pix/s                        
        self.star_amplitude = star_amplitude
        self.image_sigma = image_sigma        
          
        self.read_bias_image()
        self.hdr = []


    def write_image_mode(self, mode):
        self.em_mode = mode['em_mode']
        self.noise_factor = 1
        self.em_gain = 1
        if self.em_mode == 1:
            self.noise_factor = 1.41            
            self.em_gain = mode['em_gain']
        self.preamp = mode['preamp']
        self.hss = mode['hss']
        self.bin = mode['bin']        
        self.t_exp = mode['t_exp']        

        self.gain = 0 #preamp gain
        self.set_gain()        
        self.dark_current = 0
        self.set_dc() #função para setar a corrente de escuro
        self.read_noise = 0
        self.calc_RN()



    def set_gain(self):
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
        #equacao tirada do artigo de caract. dos CCDs
        T = self.ccd_temp
        if self.serial_number == 9914:
            self.dark_current = 24.66*np.exp(0.0015*T**2+0.29*T) 
        if self.serial_number == 9915:
            self.dark_current = 35.26*np.exp(0.0019*T**2+0.31*T)
        if self.serial_number == 9916:
            self.dark_current = 9.67*np.exp(0.0012*T**2+0.25*T)
        if self.serial_number == 9917:
            self.dark_current = 5.92*np.exp(0.0005*T**2+0.18*T)


    def read_bias_image(self):
        image = fits.getdata(self.image_dir + self.bias_name).astype(float)        
        bias_shape = image.shape
        if bias_shape[0] == 1: self.bias_data = self.bias_data[0]
        self.bias_level = np.median(image)


    def calc_RN(self):
        #calcula o RN utilizando a biblioteca desenvolvida        
        RN = RNC.ReadNoiseCalc()    
        RN.write_operation_mode(self.em_mode, self.em_gain, self.hss, self.preamp, self.bin)
        RN.calc_read_noise()        
        self.read_noise =  float(RN.noise)


    def create_image_header(self):
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
        em_gain = '_G' + str(self.em_gain)
        em_mode = 'CONV_'
        if self.em_mode == 1: em_mode = 'EM_'
        hss = str(self.hss) + 'MHz'
        preamp = '_PA' + str(self.preamp)
        binn = '_B' + str(self.bin)
        t_exp = '_TEXP'+ str(self.t_exp)
        star_amp = '_S'+ str(self.star_amplitude)
        
        self.image_name = em_mode + hss + preamp + binn + t_exp + em_gain #+ star_amp


    def create_synthetic_image(self):
        t_exp = self.t_exp
        em_gain = self.em_gain
        gain = self.gain
        bias = self.bias_level                
        dc = self.dark_current*t_exp
        rn = self.read_noise       
        sky = self.sky_flux
        nf = self.noise_factor
        binn = self.bin

        #print(t_exp, em_gain, gain, bias, dc, rn, sky, nf) ,exit()
        star_amplitude = self.star_amplitude * t_exp*em_gain*binn**2 / gain        
##        table = Table()
##        table['amplitude'] = [star_amplitude]
##        table['x_0'] = [100]
##        table['y_0'] = [100]
##        table['gamma'] = [self.image_sigma]
##        table['alpha'] = [1]
##
        shape = (200, 200)
##        model = Moffat2D()        
##        image = make_model_sources_image(shape, model, table)

        table = Table()
        table['amplitude'] = [star_amplitude]
        table['x_mean'] = [100]
        table['y_mean'] = [100]
        table['x_stddev'] = [3/binn]
        table['y_stddev'] = [3/binn]
        table['theta'] = np.radians(np.array([0]))
        image = make_gaussian_sources_image(shape, table)                

        background_level = bias + (dc + sky) * t_exp * em_gain * binn**2 / gain        
        image_noise = np.sqrt(rn**2 + (sky + dc)*t_exp * nf**2 * em_gain**2 * binn**2)
        #print(background_level),exit()
        #print(self.image_name, image_noise/gain)
        noise_image = make_noise_image(shape, distribution='gaussian', mean=0, stddev=image_noise)/gain
        bias_image = make_noise_image(shape, distribution='gaussian', mean=background_level, stddev=0)
        image+=noise_image+bias_image
        #image_noise = np.sqrt(star * t_exp * nf**2 * em_gain**2 + n_pix * (rn**2 + (sky + dc)*t_exp * nf**2 * em_gain**2))
        #image_noise = np.sqrt(rn**2 + (sky + dc)*t_exp * nf**2*em_gain**2)        
        #poisson_noise = (sky + dc)*t_exp * em_gain
        #gaussian_noise_image = make_noise_image(shape, distribution='gaussian', mean=0, stddev=rn)
        #poisson_noise_image = make_noise_image(shape, distribution='poisson', mean=poisson_noise)
        #bias_image = make_noise_image(shape, mean=bias, stddev=0)                               
        #noise_image = (gaussian_noise_image + poisson_noise_image)/gain + bias_image
        #print(np.mean(noise_image))       
   

##        y, x = np.indices(shape, dtype='float32')
##        radius = 12.6217213865933
##        working_mask = np.ones(shape,bool)
##        r = np.sqrt((x - 100)**2 + (y - 100)**2)                    
##        mask = (r < radius) * working_mask
##        n_pix = len(np.where(mask)[0])
##        star = sum(image[np.where(mask)])
##        print(star),exit()

        
        fits.writeto(self.image_dir + self.image_name+ '.fits', image, overwrite=True, header=self.hdr)


    def create_bias_image(self):
        t_exp = 1e-5
        em_gain = self.em_gain
        gain = self.gain
        bias = self.bias_level
        rn = self.read_noise       
        binn = self.bin
        
        shape = (200, 200)               
        background_level = bias     
        image_noise = rn      
        noise_image = make_noise_image(shape, distribution='gaussian', mean=0, stddev=image_noise)/gain
        bias_image = make_noise_image(shape, distribution='gaussian', mean=background_level, stddev=0)
        image = noise_image + bias_image
        fits.writeto(self.image_dir + self.image_name+ '_BIAS.fits', image, overwrite=True, header=self.hdr)

        

mode = {"em_mode": 0, "hss": 1, "preamp": 1, "bin": 1, "t_exp": 20, "em_gain": 1}
image_dir = r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Testes do codigo'
json_file = 'INITIAL_SETUPS.txt'

##modes=[]
##with open(image_dir + '/' + json_file) as arq:
##    lines = arq.read().split('}')
##    del lines[-1]    
##    arq.close()
##    for line in lines:
##        line+='}'        
##        mode = json.loads(line)        
##        modes.append(mode)   
##    
##    
    
##for mode in modes:
CSI = Create_Synthetic_Images(ccd_temp=-60,
                          serial_number=9917,                              
                          star_amplitude = 2000, #e-/s
                          sky_flux=12.298897076737294, #e-/pix/s                              
                          bias_name='bias_final_002',
                          image_dir = image_dir,
                          image_sigma= 2)
CSI.write_image_mode(mode)
CSI.create_image_header()
CSI.write_image_name()    
CSI.create_synthetic_image()
CSI.create_bias_image()
