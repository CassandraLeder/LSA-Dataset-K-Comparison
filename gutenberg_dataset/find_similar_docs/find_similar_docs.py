# -*- coding: utf-8 -*-
"""
Compute statistics on the saved cosine similarity matrices from the LSA script.
Created on Wed Nov 12 12:03:45 2025
"""

import sys
import os
import numpy as np
import constants

def clear_file(fname):
    with open(fname, 'w', encoding='utf-8') as f:
        f.write("")

def print_write(string, fname):
    print(string)
    with open(fname, 'a', encoding='utf-8') as f:
        f.write(string)

# compute population wide statistics
def pop_mean(similarities):
    return(np.mean(similarities))

def pop_std(similarities):
    return(np.std(similarities))
    
def pop_z_score(similarities, mu, sigma):
    z_scores = []
    for similarity in similarities:
        z_scores.append((similarity - mu) / sigma)
    return(z_scores)

# compute statistics based on matrix columns (documents)
def doc_mean(similarities):
    return(np.mean(similarities, axis=1))
    
def doc_std(similarities):
    return(np.std(similarities, axis=1))
    
def doc_z_score(similarities, x_bar, s):
    z_scores = []
    for similarity in similarities:
        z_scores.append((similarity - x_bar) / s)
    return(z_scores)
    
if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError("Usage: [path to cosine similarity matrix]")
    
    
    # load in data
    similarities = np.load(sys.argv[1])
    # get population level statistics
    mu = pop_mean(similarities)
    sigma = pop_std(similarities)
    pop_z_scores = pop_z_score(similarities, mu, sigma)
    
    # get document level statistics
    x_bar = doc_mean(similarities)
    s = doc_std(similarities)
    doc_z_scores = doc_z_score(similarities, x_bar, s)
    
    # output/write statistics
    pop_file = os.path.join(constants.POINTCLOUD_AFTER_FOLDER, sys.argv[1] + "pop_stats.txt")
    clear_file(pop_file)
    
    print_write(f"μ = {mu}", pop_file)
    print_write(f"σ = {sigma}", pop_file)
    
    print_write("Population z-scores are: ", pop_file)
    for z_score in pop_z_scores:
        print_write(z_score, pop_file)
        
    doc_file = os.path.join(constants.POINTCLOUD_AFTER_FOLDER, sys.argv[1] + "doc_stats.txt")
    clear_file(doc_file)
    
    print_write(f"x̄ = {x_bar}", doc_file)
    print_write(f"s = {s}", doc_file)

    print_write("Document z-scores are: ", doc_file)
    for z_score in doc_z_scores:
        print_write(z_score, doc_file)
