# -*- coding: utf-8 -*-
"""
Created on Thu May 29 19:50:34 2025

@author: cassa
"""

import os
import subprocess
import constants
    
corpus_path = os.path.join(os.getcwd(), 'corpus' + constants.PATH_DELIMITER)

files_list = os.listdir(corpus_path)
files_list.sort()
print(f"Sorted files in corpus folder: {files_list}")
"""
    With current settings, files will be in the following order: 
    {work_name}_corpus, {work_name}_corpus.index, {work_name}_dictionary.dict
    
    Now supply these commands to our python lsa program
"""

# step size of 3 because 3 args
for i in range(0, len(files_list), 3):
    # ARGUMENTS: [PATH TO DATA DIRECTORY] [DICTIONARY FNAME] [CORPUS FNAME]
    subprocess.run([os.path.join(os.getcwd(), 'run_lsa.sh'), os.path.join(os.getcwd(), 'corpus' + constants.PATH_DELIMITER), files_list[i + 2], files_list[i]])
