# -*- coding: utf-8 -*-
"""
Created on Sun Sep 14 14:32:03 2025

@author: cassa
"""
import requests
import os
import re
import constants
from bs4 import BeautifulSoup

# get file from url and write file to path
def download_write_file(url, file_name, save_path):
    
    if (os.path.exists(save_path) != True):
        os.makedirs(save_path)
    response = requests.get(url)
    
    # if response indicates there was no problem fetching file
    if (response.ok):
        full_path = os.path.join(save_path, file_name)
        
        with open(full_path, "wb") as file:
            file.write(response.content)
            
        print(f"\n\nDownloaded {file_name} successfully! Saved to {full_path}")
    else:
        print(f"\n\nThe file {file_name} was not able to be downloaded. Status code: {response.status_code}")

def create_link(ebook_num):
    ebook_num = ebook_num.replace('/ebooks/', '') # leave only the actual ebook number
    LINK_TEMPLATE = "https://www.gutenberg.org/cache/epub/"
    
    return(LINK_TEMPLATE + str(ebook_num) + '/pg' + str(ebook_num) + '.txt')

if __name__ == "__main__":
    # page to query
    QUERY_PAGE = "https://www.gutenberg.org/browse/scores/top#books-last30"
    
    # get HTML of the books most frequently downloaded page
    request = requests.get(QUERY_PAGE)
    if (request.ok): # if 200
        parsed_content = BeautifulSoup(request.text, 'html.parser')
        # output to file
        with open('query_page.html', 'w', encoding='utf-8') as file:
            print(parsed_content.prettify(), file=file)
    
    # find ordered list for most frequently downloaded in last 30 days header
    ID = "books-last30"
    with open('ol.html', 'w', encoding='utf-8') as file:
        print(parsed_content.find(id=ID).find_next("ol"), file=file)
    
    # get list of ebook numbers and titles for downloading
    ebook_nums = []
    titles = []
    with open('ol.html', 'r', encoding='utf-8') as file:
        parsed_ol = BeautifulSoup(file, 'html.parser')
        anchors = parsed_ol.find_all('a') 
        for a in anchors:
            ebook_nums.append(a.get('href'))
            titles.append(a.get_text())
            
    # remove special characters, numbers, spaces from titles and add .txt
    for i in range(0, len(titles)):
        titles[i] = re.sub(r'[^a-zA-Z0-9\s]', '', titles[i])
        titles[i] = re.sub(r'\d+', '', titles[i]) 
        titles[i] = titles[i].replace(' ', '_')
        titles[i] += '.txt'
    
    # download all books that can be downloaded as a txt file (TLP is usually in the list :/)
    SAVE_PATH = constants.DATASET_PATH
    for i, num in enumerate(ebook_nums):
        download_write_file(url=create_link(num), 
                            file_name=titles[i], 
                            save_path=SAVE_PATH)
     
    