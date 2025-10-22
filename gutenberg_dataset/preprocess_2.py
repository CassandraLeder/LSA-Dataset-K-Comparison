# -*- coding: utf-8 -*-
"""
Input: text file
Output: Preprocess text files and divide into 100 word chunks documents

@author: cassa
"""

import re
import sys
import os
import constants

def standard_preprocess(text):
    text = text.lower() # lowercase text
    text = text.replace('\n', ' ') # get text as one paragraph without breaks
    text = re.sub(r'[^\w\s]', '', text) # remove punctuation
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text) # remove special characters
    text = re.sub(r'\d+', '', text) # remove numbers
    
    return(text)

# divide text into 100 word documents using splicing
def divide_documents(text):
    documents = []
    words = text.split(' ')
    # remove white space and empty strings
    words = list(filter(lambda word: word.strip(), words))
    
    # split into documents    
    NUM_WORDS = 100 # the word size of each document    
    idx = 0
    while(idx + NUM_WORDS <= len(words)):
        documents.append(' '.join(words[idx:idx+NUM_WORDS]))
        idx += NUM_WORDS
    
    # get the remainder
    documents.append(' '.join(words[idx:]))
    
    return(documents)

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 2:
        print("Usage ./preprocess.py [input text file]")
    
    arg = sys.argv[1]
    print(f"\nCurrently preprocessing {arg}")
    with open(arg, 'r', encoding="utf8") as file:
        text = file.read()
        
        # all gutenberg books have a header that ends with *** START OF THE PROJECT ... ***
        # now we have to get the title of the work to remove the header
        
        # first line contains the full title after the same text (32 chars) every time, title, then a new line
        # go 32 chars in, split all new lines, and get the 0th element (just the title)
        HEAD_LEN = 32
        title = text[HEAD_LEN:].split('\n')[0]
        
        # find header beginning
        head_text = "*** START OF THE PROJECT GUTENBERG EBOOK " + title.upper() + " ***"
        head_indx = text.find(head_text)
        
        # find where heading ends
        head_end = head_indx + len(head_text)
        
        # now we have to remove the footer
        foot_text = "*** END OF "
        # find start of footer then go back one
        foot_indx = text.find(foot_text) - 1               
        
        # get all of text after the header and before footer
        text = text[head_end:foot_indx]
        
        # usually the title occurs at the start of a book, so remove title
        text = text.replace(title, '').replace(title.title(), '').replace(title.upper(), '')
        text = standard_preprocess(text)
        
        # we divide into documents before lower-case because it makes the processing easier..
        documents = divide_documents(text)
        f_title = arg.split('\\')[-1].replace('.txt', '')
        print(f"ftitle: {f_title}")
        main_dir = os.path.join(constants.DATASET_PATH, 'documents')
        document_fpath = os.path.join(main_dir, f_title + 'docs')
        
        if(not os.path.exists(main_dir)):
            os.makedirs(main_dir)
        if (not os.path.exists(document_fpath)):
            os.makedirs(document_fpath)
            
        for i, doc in enumerate(documents):
           doc_fname = os.path.join(document_fpath, f_title + str(i + 1) + '.txt') 
           with open(doc_fname, 'w', encoding='utf-8') as file:
               print(doc, file=file)