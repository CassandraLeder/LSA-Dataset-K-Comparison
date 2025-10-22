# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 15:17:41 2025

@author: cassa
"""

import numpy as np

pagan_taoism = np.load('pagan-taoism_network_correlation.npy')
spirituality_pagan = np.load('spirituality-pagan_network_correlation.npy')
spirituality_taoism = np.load('spirituality-taoism_network_correlation.npy')

print(np.round(pagan_taoism, 4))
print(np.round(spirituality_pagan, 4))
#print(spirituality_pagan)
print(np.round(spirituality_taoism, 4))