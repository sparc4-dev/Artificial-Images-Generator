#!/usr/bin/env python
# coding: utf-8

#This file runs the Artificial Images Generator algorithm

#14/10/2020. Denis Varise Bernardes.

import Artificial_Images_Simulator as AIG

ccd_operation_mode = {"em_mode": 0, "hss": 1, "preamp": 1, "bin": 1, "t_exp": 20, "em_gain": 1}
AIG = AIG.Artificial_Images_Generator(star_flux = 2000, #e-/s
                          sky_flux = 12.29, #e-/pix/s                 
                          gaussian_stddev = 3, #pixels
                          ccd_operation_mode = ccd_operation_mode)
AIG.write_image_mode()
AIG.create_image_header()
AIG.write_image_name()    
AIG.create_artificial_image()
