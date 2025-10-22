# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 18:03:44 2025

@author: cassa
"""

from scipy.stats import pearsonr
import sys
import os
import numpy as np

'''
    Usage: network_correlation [path to correlation matrix one] [path to correlation matrix two] 
'''

if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print("Usage: network_correlation [path to correlation matrix one] [path to correlation matrix two]")
        exit(-1)
        
    network_correlation_fpath = os.path.join(os.getcwd(), 'network_correlations')
    if not os.path.exists(network_correlation_fpath):
        os.makedirs(network_correlation_fpath)
    
    matrix_1 = np.load(sys.argv[1])
    matrix_2 = np.load(sys.argv[2])
    matrix_1_name = sys.argv[1].split("_")[0]
    matrix_2_name = sys.argv[2].split("_")[0]
    
    correlation = pearsonr(matrix_1, matrix_2)[0]
    
    print(f"Correlation between {matrix_1_name} and {matrix_2_name}: {correlation}")
    
    np.save(os.path.join(network_correlation_fpath, f"{matrix_1_name}-{matrix_2_name}_network_correlation.npy"), correlation)