# -*- coding: utf-8 -*-
"""
Created on Wed Sep 24 07:17:46 2025

Tasks:
    1. Download Gutenberg dataset
    2. Preprocess and split into documents
    3. Create corpora
    4. Run LSA experiments
    5. Run document-level experiments on cosine similarity matrices before/after LSA

"""

import os
import subprocess
import constants

if __name__ == "__main__":
    """
    # download dataset
    subprocess.run(["python", constants.DOWNLOAD_SCRIPT_PATH])    

    # get a list of text files to run tasks o
    
    works_list = os.listdir(constants.WORKS_FOLDER)
    for work in works_list:
        print(f"\n\nRunning experiments on \'{work.strip('.txt').replace('_', ' ')}\'.")
        #preprocess
        work_path = os.path.join(constants.WORKS_FOLDER, work)
        subprocess.run(["python", constants.PREPROCESS_SCRIPT_PATH, 
                        work_path])
        
        #create dictionary/corpus
        docs_path = os.path.join(constants.DOCUMENTS_FOLDER, 
                                 work.replace('.txt','') + '_docs')
        subprocess.run(["python", constants.CREATE_DICTIONARY_SCRIPT_PATH, 
                        docs_path])
        # run LSA on corpora
        data_path = constants.CORPUS_FOLDER
        corpus_dict_fname = work.replace('.txt', '') + '.dict'
        corpus_file_fname = work.replace('.txt', '') + '_corpus.corpus'
        
        subprocess.run(["python", constants.LSA_SCRIPT_PATH,
                        data_path,
                        corpus_dict_fname,
                        corpus_file_fname])
        
        # do document level analysis before LSA
        """
    """
            Note: due to memory issues involved with computing large cosine similarities matrices for corpora, this code was written in C++.
            (C++ files are built in advance for this script) 
        """
    """
        subprocess.run([constants.FIND_SIMILAR_DOCS_BEFORE_SCRIPT_PATH,
                        corpus_file_path])
        
        pointcloud_file_path = os.path.join(constants.POINTCLOUD_FOLDER,
                                            work.replace('.txt', '') + '_pointcloud.csv')
        
        subprocess.run(["risper", "--threshold 1", pointcloud_file_path])
    """
    # compute more document level tests with each cosine similarity file after LSA
    similarity_list = os.listdir(constants.COSIM_FOLDER)    
    for similarity in similarity_list:
        subprocess.run(["python", constants.FIND_SIMILAR_DOCS_AFTER_SCRIPT_PATH, os.path.join(constants.COSIM_FOLDER, similarity), constants.STATS_AFTER_FOLDER])
        #subprocess.run(["risper", "--threshold 1", ""])
    
    