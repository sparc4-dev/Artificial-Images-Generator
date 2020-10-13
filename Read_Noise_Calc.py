#!/usr/bin/env python
# coding: utf-8

#Este codigo cotem a classe ReadNoiseCalc que calcula
#o valor do ruido de leitura para a camera CCD iXon Ultra EMCCD
#em funcao do modo de operacao. O calculo e realizado
#com base nos dados das caracterizacoes da camera e estruturados
#em planilhas excel.
#Denis Varise Bernardes.
#08/10/2019.

import pandas as pd
import numpy as np
from scipy.interpolate import interp1d


class ReadNoiseCalc:

    def __init__(self):         
        self.noise = 0
##        self.PA1B1HSS1  = 'RN_PA1B1HSS1.xlsx'
##        self.PA1B1HSS10 = 'RN_PA1B1HSS10.xlsm'
##        self.PA1B1HSS20 = 'RN_PA1B1HSS20.xlsm'
##        self.PA1B1HSS30 = 'RN_PA1B1HSS30.xlsm'    
##    
##        self.PA1B2HSS1 =  'RN_PA1B2HSS1.xlsm'
##        self.PA1B2HSS10 = 'RN_PA1B2HSS10.xlsm'
##        self.PA1B2HSS20 = 'RN_PA1B2HSS20.xlsm'
##        self.PA1B2HSS30 = 'RN_PA1B2HSS30.xlsm'    
##    
##        self.PA2B1HSS1 =  'RN_PA2B1HSS1.xlsm'
##        self.PA2B1HSS10 = 'RN_PA2B1HSS10.xlsm'
##        self.PA2B1HSS20 = 'RN_PA2B1HSS20.xlsm'
##        self.PA2B1HSS30 = 'RN_PA2B1HSS30.xlsm'
##
##        self.PA2B2HSS1 =  'RN_PA2B2HSS1.xlsm'
##        self.PA2B2HSS10 = 'RN_PA2B2HSS10.xlsm'
##        self.PA2B2HSS20 = 'RN_PA2B2HSS20.xlsm'
##        self.PA2B2HSS30 = 'RN_PA2B2HSS30.xlsm'
##

    def write_operation_mode(self, em_mode, em_gain, hss, preamp, binn):
        # Foi feito um ajuste por causa da funcao Bayesian OPT
        self.em_mode = em_mode
        self.em_gain = em_gain
        self.hss = hss
        self.preamp = preamp
        self.binn = binn


    def get_operation_mode(self):
        print('em_mode = ',self.em_mode)
        print('em_gain = ',self.em_gain)
        print('hss = ',self.hss)
        print('preamp = ',self.preamp)
        print('binn = ',self.binn)
    
            
    def read_tab_return_column(self, tab_name, column_name):        
        df = pd.read_excel(tab_name) 
        columns = pd.DataFrame(df)
        return columns[column_name]


    def calc_read_noise(self):
        #Para o modo convencional, retorna o valor da tabela
        #Para o modo EM, calcula em funcao do ganho_em
        if self.em_mode == 0:
            self.calc_read_noise_conventional()
        if self.em_mode == 1:
            self.calc_read_noise_em()
       


    def calc_read_noise_conventional(self):
        #O modo de operacao determina a posicao da tabela
        # que sera lido o valor do read noise
        indice_tab = 0
        if self.hss == 1: 
            if self.preamp == 1:
                if self.binn == 1:
                    indice_tab = 17
                if self.binn == 2:
                    indice_tab = 18
            if self.preamp == 2:
                if self.binn == 1:
                    indice_tab = 19
                if self.binn == 2:
                    indice_tab = 20
        if self.hss == 0.1:
            if self.preamp == 1:
                if self.binn == 1:
                    indice_tab = 21
                if self.binn == 2:
                    indice_tab = 22
            if self.preamp == 2:
                if self.binn == 1:
                    indice_tab = 23
                if self.binn == 2:
                    indice_tab = 24
        
        column_noise = self.read_tab_return_column('planilhas/Tabelas_Valores_Ruido_Leitura.xlsm', 'Noise')
        self.noise = column_noise[indice_tab]      
    

    def calc_read_noise_em(self):
        #Eh realizada uma interpolacao do valor do ruido de leitura em funcao do ganho_em
        #A planilha eh escolhida em funcao do modo de operacao
        hss = self.hss
##        if self.hss == 30: hss = 1
##        if self.hss == 20: hss = 10
##        if self.hss == 10: hss = 20
##        if self.hss == 1: hss = 30       
        
        tab_name = 'planilhas/RN_PA' + str(int(self.preamp)) + 'B' + str(int(self.binn)) + 'HSS' + str(int(hss)) + '.xlsm'           
        column_noise = self.read_tab_return_column(tab_name, 'Noise (e-)')[0:11]
        column_em_gain = self.read_tab_return_column(tab_name, 'EM Gain')[0:11]
        f = interp1d(column_em_gain, column_noise)
        self.noise = f(self.em_gain)    
        



    
