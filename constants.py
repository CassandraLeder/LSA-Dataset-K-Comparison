# -*- coding: utf-8 -*-
"""
Define common paths shared among scripts.
Created on Thu May 29 20:03:21 2025
"""

import os

def create_directories(dirs):
    for dir in dirs:
        os.makedirs(dir) if not os.path.exists(dir) else ""

# directories in the main github project folder
DATASET_FOLDER = os.path.join(os.getcwd(), 'most_downloaded_dataset\\')
FIND_SIMILAR_DOCS_FOLDER = os.path.join(os.getcwd(), "find_similar_docs\\")
MODEL_FOLDER = os.path.join(os.getcwd(), 'models\\')
CORPUS_FOLDER = os.path.join(os.getcwd(), 'corpus\\')
GRAPH_FOLDER = os.path.join(os.getcwd(), 'graphs\\')
CORRELATION_FOLDER = os.path.join(os.getcwd(), 'network_correlations\\')
# sub-directories of correlation
COSIM_FOLDER = os.path.join(CORRELATION_FOLDER, "cosim\\")
PEARSON_FOLDER = os.path.join(CORRELATION_FOLDER, "pearson\\")

# sub-directories of dataset 
POINTCLOUD_FOLDER = os.path.join(DATASET_FOLDER, "docs_similarity_pointcloud\\")
STATS_AFTER_FOLDER = os.path.join(DATASET_FOLDER, "after_stats\\")
WORKS_FOLDER = os.path.join(DATASET_FOLDER, 'works\\')
DOCUMENTS_FOLDER = os.path.join(DATASET_FOLDER, 'documents\\')

# create all directories
dirs = [DATASET_FOLDER, 
        FIND_SIMILAR_DOCS_FOLDER, 
        POINTCLOUD_FOLDER, 
        STATS_AFTER_FOLDER, 
        WORKS_FOLDER, 
        CORPUS_FOLDER, 
        DOCUMENTS_FOLDER, 
        MODEL_FOLDER, 
        GRAPH_FOLDER, 
        CORRELATION_FOLDER,
        COSIM_FOLDER,
        PEARSON_FOLDER]
create_directories(dirs)

# paths to scripts
DOWNLOAD_SCRIPT_PATH = os.path.join(os.getcwd(), 'download_dataset.py')
PREPROCESS_SCRIPT_PATH = os.path.join(os.getcwd(), 'preprocess.py')
CREATE_DICTIONARY_SCRIPT_PATH = os.path.join(os.getcwd(), 'create_dictionary.py')
LSA_SCRIPT_PATH = os.path.join(os.getcwd(), "lsa_model.py")
FIND_SIMILAR_DOCS_BEFORE_SCRIPT_PATH = os.path.join(FIND_SIMILAR_DOCS_FOLDER, "find_similar_docs.exe")
FIND_SIMILAR_DOCS_AFTER_SCRIPT_PATH = os.path.join(FIND_SIMILAR_DOCS_FOLDER, "find_similar_docs.py")