# -*- coding: utf-8 -*-
"""
Created on Wed Sep 24 07:17:46 2025

Tasks:
    1. Download Gutenberg dataset
    2. Preprocess and split into documents
    3. Create corpora
    4. Run LSA experiments
    5. Run document-level experiments

"""

import os
import subprocess
import constants

if __name__ == "__main__":
    # download dataset
    subprocess.run(["python", constants.DOWNLOAD_SCRIPT_PATH])    
    # build cpp files in advance
    subprocess.run(["g++", constants.CPP_FOLDER, "*.cpp", "-o", "find_similar_docs.exe"])

    # now we have a list of text files to run tasks on
    works_list = os.listdir(constants.DATASET_PATH)
    for work in works_list:
        print(f"\n\nRunning experiments on {work}.")
        #preprocess
        work_path = os.path.join(os.getcwd(), 
                                 constants.DATASET_PATH, work)
        subprocess.run(["python", constants.PREPROCESS_SCRIPT_PATH, 
                        work_path])
        
        #create dictionary/corpus
        docs_path = os.path.join(constants.DOCUMENTS_PATH, 
                                 work.replace('.txt','') + 'docs')
        subprocess.run(["python", constants.CREATE_DICTIONARY_SCRIPT_PATH, 
                        docs_path])
        # run LSA on corpora
        corpora_list = os.listdir(constants.CORPUS_PATH)
        result_path = os.path.join(os.getcwd(), 
                                   'lsa_results')
        corpus_dict_path = os.path.join(constants.CORPUS_PATH, 
                                        work.replace('.txt', '') + '.dict')
        corpus_file_path = os.path.join(constants.CORPUS_PATH, 
                                        work.replace('.txt', '') + 'corpus.corpus')
        
        subprocess.run(["python", constants.LSA_SCRIPT_PATH,
                        result_path,
                        corpus_dict_path,
                        corpus_file_path])
        
        # do document level analysis 
        subprocess.run(["find_similar_docs.exe", corpus_file_path])
        
        pointcloud_file_path = os.path.join(constants.POINTCLOUD_FOLDER,
                                            work.replace('.txt', '') + '_pointcloud.csv')
        
        subprocess.run(["risper", "--threshold 1", pointcloud_file_path])