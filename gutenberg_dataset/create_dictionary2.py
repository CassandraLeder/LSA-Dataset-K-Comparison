# -*- coding: utf-8 -*-
"""
Created on Wed Sep 24 07:32:02 2025

@author: cassa
"""

import sys
import os
from gensim import corpora
from nltk.tokenize import RegexpTokenizer
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


if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Usage: ./create_dictionary2.py [path to documents folder]")
    
    docs_folder = sys.argv[1]
    docs_title = docs_folder.split('\\')[-1].replace('docs', '')
    print(f"Current document folder {docs_folder}")
    docs_list = os.listdir(docs_folder)
    
    list_tokens = []
    for doc_f in docs_list:
        tokens = []         
        doc_path = os.path.join(docs_folder, doc_f)
        with open(doc_path, 'r', encoding='utf-8') as file:
            doc = file.read()
            tokens = tokenize_stem(doc)
            
        list_tokens.append(tokens)
    
    dict_path = constants.CORPUS_PATH
    os.makedirs(dict_path) if not os.path.exists(dict_path) else ""
    (dictionary, doc_term_matrix) = create_dictionary_matrix(list_tokens)
        
    dictionary_fname = os.path.join(dict_path, docs_title + '.dict')
    dictionary.save(dictionary_fname)
        
    doc_term_matrix_fname = os.path.join(dict_path, docs_title + 'corpus.corpus')
    corpora.MmCorpus.serialize(fname=doc_term_matrix_fname, corpus=doc_term_matrix)
