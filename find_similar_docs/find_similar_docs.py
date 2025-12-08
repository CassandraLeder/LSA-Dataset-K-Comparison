# -*- coding: utf-8 -*-
"""
Compute statistics on the saved cosine similarity matrices from the LSA script.
Created on Wed Nov 12 12:03:45 2025
"""

import sys
import os
import numpy as np

def print_write(string, fname):
    print(string)
    with open(fname, 'w', encoding='utf-8') as file:
        file.write(string)

def print_npsave(string, fname):
    print(string)
    np.save(fname)

def z_score(similarity, mu, sigma):
    return ((similarity - mu) / sigma)

# compute population wide statistics
def pop_mean(similarities):
    return(np.mean(similarities))

def pop_std(similarities):
    return(np.std(similarities))
    
def pop_z_score(similarities, mu, sigma):
    z_scores = []
    for similarity in similarities:
        z_scores.append(z_score(similarity, mu, sigma))
    return(z_scores)

# compute statistics based on matrix columns (documents)
def doc_mean(similarities):
    return(np.mean(similarities, axis=1))
    
def doc_std(similarities):
    return(np.std(similarities, axis=1))

def doc_z_score(similarities, x_bar, s):
    z_scores = []
    for similarity in similarities:
        z_scores.append(z_score(similarity, x_bar, s))
    return(z_scores)

def find_similar_docs(similarities):
    return(similarities.max(axis=1, where=(similarities > 0), initial=0))
    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError("Usage: [path to cosine similarity matrix] [path to destination directory]")
    
    dest_dir = sys.argv[2]
    
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
    pop_file = os.path.join(dest_dir, "pop_stats.txt")
    
    print_write(f"μ = {mu}", pop_file)
    print_write(f"σ = {sigma}", pop_file)
    
    for z_score in pop_z_scores:
        print_npsave(z_score, pop_file)
        
    doc_file = os.path.join(dest_dir, "doc_stats.txt")
    
    print_write(f"x̄ = {x_bar}", doc_file)
    print_write(f"s = {s}", doc_file)

    for z_score in doc_z_scores:
        print_npsave(z_score, doc_file)
    
    max_similarity_file = os.path.join(dest_dir, "max_similarity.npy")
    max_similarity = find_similar_docs(similarities)
    print_write(f"Max similarity is {max_similarity}", max_similarity_file)