# -*- coding: utf-8 -*-
"""
Define common paths shared among scripts.
Created on Thu May 29 20:03:21 2025
"""

import os

DATASET_PATH = os.path.join(os.getcwd(), 'most_downloaded_dataset')
CORPUS_PATH = os.path.join(os.getcwd(), 'corpus')
DOCUMENTS_PATH = os.path.join(DATASET_PATH, 'documents')
DOWNLOAD_SCRIPT_PATH = './download_dataset.py'
PREPROCESS_SCRIPT_PATH = os.path.join(os.getcwd(), 'preprocess_2.py')
CREATE_DICTIONARY_SCRIPT_PATH = os.path.join(os.getcwd(), 'create_dictionary2.py')
LSA_SCRIPT_PATH = os.path.join(os.getcwd(), "./lsa_model.py")
CPP_FOLDER = os.path.join(os.getcwd(), "find_similar_docs/")
POINTCLOUD_FOLDER = os.path.join(DATASET_PATH, "docs_similarity_pointcloud/")
POINTCLOUD_AFTER_FOLDER = os.path.join(DATASET_PATH, "after_pointcloud/")