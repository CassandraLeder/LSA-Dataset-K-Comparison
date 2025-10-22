# -*- coding: utf-8 -*-
"""
Created on Fri May  9 09:56:41 2025

    Input: raw text from ./text/
    Output: preprocessed text suitable for LSA

@author: Cassandra Leder
"""

import pandas as pd
import re
import os
import csv
from IPython.display import display
import io
import constants

# drama typically has acts and scenes + character list
# while non-drama typically has table of contents
# the use of this function helps divide text into documents
def is_drama(work, book_list):
    # get every cell individually in case there's lists
    work_string = ""
    subject_string = ""
    for i in range(0, len(book_list)):
        work_string += book_list.iloc[i]["Work"] + ','
        subject_string += book_list.iloc[i]["Subjects"] + ','
    work_list = work_string.split(',')
    subject_list = subject_string.split(',')
        
    # find specified work in list
    work_idx = work_list.index(work)
    # if it contains 'drama' in the subject column for the selected row at all, return true
    if (subject_list[work_idx].find("drama") != -1 
            or subject_list[work_idx].find("Drama") != -1):
        return True
    else:
        return False
        

# divides plays into scenes using the fact that scenes are subsections of acts
def divide_play(text):
    # unforunately, our shakespeare plays are divided into scene/acts with latin
    # so we need to know latin translations of scene/act
    latin_act = "Actus"
    latin_scene = "Scena"

    # acts
    major_documents = []
    # scenes
    minor_documents = []
    # all scenes
    documents = []
    
    # search for major documents (acts)
    major_idxs = []
    while (text.find(latin_act) != -1):
        idx = text.find(latin_act) 
    
        # remove section (or else find will find the same header over and over)
        # find first newline following location of act
        # this is start of new section
        newline_idx = text.find('\n', idx)
        
        # slice out Actus Secundus or similar
        text = text[:idx] + text[newline_idx:]
       
        # old index is now the new line, plus one is to avoid newline
        major_idxs.append(idx + 2)

    # now that the headers are gone, we can add to major documents
    for i, idx in enumerate(major_idxs):
        # if not going out of bounds
        if (i + 1 < len(major_idxs)):
            major_documents.append(text[idx:major_idxs[i + 1]])
        # if last section the slice is from new line to end
        else:
            major_documents.append(text[idx:]) 
    
    # search for minor documents (scenes) with same procedure
    # acts start with a scene, so now we just need to find subscenes in acts
    minor_idxs = []
    for i, doc in enumerate(major_documents):
        idxs = [] 
        while (doc.find(latin_scene) != -1):
            idx = doc.find(latin_scene)
            newline_idx = doc.find('\n', idx)
            
            # remove heading
            doc = doc[:idx] + doc[newline_idx:]
            
            # separate because we need a list of indicies of scenes for a given act
            idxs.append(idx + 2)
        
        major_documents[i] = doc
        # we need the index i so we know from which act the scenes are in
        minor_idxs.append([i, idxs])
            
    # now we need to take the acts and reduce them down to just the first scence
    # note: everything is subscripted zero and one bc that's the actual list
    for i, doc in enumerate(major_documents): 
        # i identifies document and i+1 selects list, not major doc index
        for j in range(0, len(minor_idxs[i][1])):
            idx = minor_idxs[i][1]

            # remove all scences after scene 1 from act, add to minor docs
            if (j + 1 < len(idx)):
                scene = doc[idx[j]:idx[j + 1]]
            else:
                scene = doc[idx[j]:]
                
            minor_documents.append(scene)
       
    # check that the play isn't composed entirely of acts (shoutout Much Ado About Nothing)
    if (len(minor_documents) != 0):
        for i in range(0, len(major_documents)):
            # total all documents if doc index = the index put in minor_indxs
            if (i == minor_idxs[i][0]):
                # remove all scenes after first scene
                major_documents[i] = major_documents[i][:minor_idxs[i][1][0]]
                documents.append(major_documents[i]) # append first scene
                for j in range(0, len(minor_documents)): # append all subscenes
                    documents.append(minor_documents[j])
    else:
        documents = major_documents
    return documents
                

def divide_nonplay(text, work):
    documents = []
    """
        My strategy for this assumes that there exists a table of contents,
        where the table of contents acts as a natural list of documents.
        Thus, we need to make a vector of all the section headings,
        then remove the table of contents and search for the headings.
    """
    # Do we remove introductions, prefaces, etc? I'm going to keep it minimal. 
    # I think it's best to include them as they reference the work at a more broad level
    contents_idx = text.find("Contents")
    newline_idx = text.find('\n', contents_idx)
    text = text[:contents_idx] + text[newline_idx:]
    
    # start read buffer at first entry in table of contents
    buffer = io.StringIO(text)
    buffer.seek(contents_idx)
    headers = []
    
    # keep going until headers repeat (example: preface [...] preface)
    line = buffer.readline().strip() # remove whitespace
    while (line not in headers):
        if (line == '\n' or line == ''):
            line = buffer.readline().strip()
            continue
        
        if (work == "The Critique of Pure Reason" and "Preface" in line):
            line = line.upper()
            line = re.sub(r'[^\w\s]', '', line)
        
        headers.append(line)
        end_idx = buffer.tell()
        line = buffer.readline().strip()
                
        
    # delete table of contents
    text = text[:contents_idx] + text[end_idx:]
    
    if (work != "The Critique of Pure Reason"):
        for i in range(0, len(headers)):
            # in most cases it's best to remove punctuation as it may make a match fail
            headers[i] = re.sub(r'[^\w\s]', '', headers[i]) 
                    
    # now find location of all headers
    header_idx = []
    for header in headers:
        if (work == "The Critique of Pure Reason" 
                and ("PREFACE" in header or "Introduction" in header)):
            header = header.upper()
            
        if (text.find(header) != -1):
            idx = text.find(header)
            newline_idx = text.find('\n', idx)
            text = text[:idx] + text[newline_idx:]
            header_idx.append(idx)
    
    for i, idx in enumerate(header_idx):
        if (i + 1 < len(header_idx)):
            documents.append(text[idx:header_idx[i + 1]])
        else:
            documents.append(text[idx:])
    
    """
        Since some headers may be containers and not actually have text,
        we remove all documents that have less than max characters
    """
    max_characters = 100
    for i, doc in enumerate(documents):
        if (len(doc) < max_characters):
            documents.remove(doc)
            
    return documents

# divides plays and non--plays into documents 
def divide_documents(text, work, book_list):        
    # if work is drama divide into scenes
    if (is_drama(work, book_list)):
        documents = divide_play(text)        
            
    # divide into chapters or sections if not drama
    else:
        documents = divide_nonplay(text, work)

    return documents


if __name__ == "__main__":
    # switches
    # display full dataframe
    pd.set_option('display.max_rows', None,
                  'display.max_columns', None)

    # Load in csv of downloaded book as dataframe
                            # sys.argv[1]
    book_list = pd.read_csv("book_list.csv")
    display(book_list)

    # convert string of works back into a list
    works = []
    for work in book_list["Work"]:        
        # split based on comma
        works.append(work.split(','))
    
    authors = book_list["Author"]
    
    # becomes documents csv
    fields = ['Work', 'Path', 'Documents']
    rows = []
    
    # read text files
    for work in works:
                
        # work is list, but usually only has a single element
        for i in range(0, len(work)):            
            print(work[i])
            work_path = os.path.join(os.getcwd(), "text" + constants.PATH_DELIMITER + work[i].replace(' ', '_') + '.txt')
            
            with open(work_path, 'r', encoding="utf8") as file:
                text = file.read()
                
            # all gutenberg books have a header that ends with *** START OF THE PROJECT ... ***
            # now we have to get the title of the work to remove the header
            
            # first line contains the full title after the same text (32 chars) every time, title, then a new line
            # go 32 chars in, split all new lines, and get the 0th element (just the title)
            title = text[32:].split('\n')[0]
            
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

            # we divide into documents before lower-case because it makes the processing easier..
            documents = divide_documents(text, work[i], book_list)

            document_folder = os.path.join(os.getcwd(), work[i].replace(' ', '_') + '_docs' + constants.PATH_DELIMITER)
            
            if not os.path.exists(document_folder):
                os.makedirs(document_folder)
            
            fnames = []
            for j, doc in enumerate(documents):
                doc = doc.lower() # lowercase text
                doc = doc.replace('\n', ' ') # get text as one paragraph without breaks
                doc = re.sub(r'[^\w\s]', '', doc) # remove punctuation
                doc = re.sub(r'[^a-zA-Z0-9\s]', '', doc) # remove special characters
                doc = re.sub(r'\d+', '', doc) # remove numbers
                
                # save document
                document_fname = work[i].replace(' ', '_') + '_' + str(j) + '.txt'
                fnames.append(document_fname)
                with open(os.path.join(document_folder, document_fname), 'w', encoding='utf-8') as file:
                    file.write(doc)
                        
            rows.append([work[i], document_folder, ','.join(fnames)]) # convert list to string
            
            # print first document
            print(documents[0])    
    
    # save output csv
    documents_path = os.path.join(os.getcwd(), 'documents.csv')
    with open('documents.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(fields)
        writer.writerows(rows)
