# -*- coding: utf-8 -*-
"""
Created on Thu May 22 11:26:15 2025

@author: cassa
"""

import sys
import os
import csv
from gensim import corpora
from nltk.tokenize import RegexpTokenizer
#from nltk.stem.porter import PorterStemmer
import numpy as np
import constants

def tokenize_stem(document):
    tokenizer = RegexpTokenizer(r'\w+')
    # not sure whether to stem
    #p_stemmer = PorterStemmer()
    tokens = tokenizer.tokenize(document)
    #stemmed_tokens = [p_stemmer.stem(i) for i in tokens]
    #print(stemmed_tokens)
    
    return tokens


def create_dictionary_matrix(tok_documents):
    dictionary = corpora.Dictionary(tok_documents)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in tok_documents]
    
    return (dictionary, doc_term_matrix)

def get_work_name(fname):
    work = docs_fnames[i][0].split('.txt')[0].replace('_', ' ')[:-2]
    return(work)

if __name__ == "__main__":
    with open('documents.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        docs_fnames = []
        paths = []
        for line in reader:
            # if header
            if (reader.line_num == 1):
                work_idx = line.index("Work")
                path_idx = line.index("Path")
                doc_idx = line.index("Documents")
            # if not header
            else:
                # get list of paths
                paths.append(line[path_idx])
                # get list of file names
                docs_fnames.append(line[doc_idx].split(','))
                
    # so docs_fnames is now a list of lists
    work_docs = [] # create list of docs so we can keep works separate
    for i in range(0, len(docs_fnames)):
        docs = []
        fname = docs_fnames[i][0]

        # print statement
        if i == 0:
            work = get_work_name(fname)
            print(f"\nNow reading {work}'s documents...")
        
        # update work if new work
        print(f"\nNow reading {get_work_name(fname)}'s documents..." 
                if work != get_work_name(fname) else "")
        
        work = get_work_name(fname) if work != get_work_name(fname) else work
        
        for j, doc_fname in enumerate(docs_fnames[i]):
            fname = os.path.join(paths[i], doc_fname)
            with open(fname, 'r', encoding='utf-8') as file:
                docs.append(file.read())
                
        work_docs.append([work, docs])
    list_tokens = []
    for i in range(0, len(work_docs)):
        tokens = []         

        for j, doc in enumerate(work_docs[i][1]):
            # make list of lists of token for each work
            tokens.append(tokenize_stem(doc))
            
        list_tokens.append(tokens)
    
    dict_path = os.path.join(os.getcwd(), 'corpus' + constants.PATH_DELIMITER)
    os.makedirs(dict_path) if not os.path.exists(dict_path) else ""
    for i, doc_list in enumerate(list_tokens):
        (dictionary, doc_term_matrix) = create_dictionary_matrix(doc_list)

        dictionary_fname = os.path.join(dict_path, work_docs[i][0].replace(' ', '_') + '_dictionary.dict')
        dictionary.save(dictionary_fname)
        
        doc_term_matrix_fname = os.path.join(dict_path, work_docs[i][0].replace(' ', '_') + '_corpus')
        
        corpora.MmCorpus.serialize(fname=doc_term_matrix_fname, corpus=doc_term_matrix)
