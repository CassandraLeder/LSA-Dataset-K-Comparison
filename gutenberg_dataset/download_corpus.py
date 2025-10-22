# -*- coding: utf-8 -*-
"""
Created on Wed May  7 19:12:34 2025

    Input: Gutenberg catalog csv and name of books to be downloaded for corpus
    Output: Save list of downloaded books and download books into corpus folder

@author: Cassandra Leder
"""

import pandas as pd
import os
from IPython.display import display
from datetime import datetime
import requests
import constants

# get file from url and write file to path
def download_write_file(url, file_name, save_path):
    
    if (os.path.exists(save_path) != True):
        os.makedirs(save_path)
    response = requests.get(url)
    
    # if response indicates there was no problem fetching file
    if (response.status_code == 200):
        full_path = os.path.join(save_path, file_name)
        
        with open(full_path, "wb") as file:
            file.write(response.content)
            
        print(f"Downloaded {file_name} successfully! Saved to {full_path}")
    else:
        print(f"The file was not able to be downloaded. Status code: {response.status_code}")

# take a work title and find its ebook based on the method described by the option
def find_choose_ebook(work, option='old'):
    options = ['old', 'middle', 'young', 'all']
    
    if option not in options:
        raise ValueError(f"Option {option} passed to find_choose_ebook not in the allowable options.")
    
    
    # search for the work we're looking for
    book_listings = catalog[authors_catalog]['Title'].str.contains(work, na=False)
    # filter non-English versions
    en = catalog[authors_catalog][book_listings]['Language'].str.contains('en', na=False)
    # filter out audiobooks
    text = catalog[authors_catalog][book_listings][en]['Type'].str.contains('Text', na=False)
                
    print("-" * 80)
    print(f"\nVersions of {work} in Project Gutenberg catalog:")
    display(catalog[authors_catalog][book_listings][en][text])
    """
        The question now is which "Hamlet", for instance, do we want? (a tie-breaker in other words)
        We want the one that's the oldest
    """
    
    if (option == 'old' or option == 'young'):   
        # create date object from the publication date in the catalog
        pub_dates = catalog[authors_catalog][book_listings][en][text]['Issued'].to_list()
        
        # this is how the date data looks in the csv file (ex. 1997-12-01)
        format_str = "%Y-%m-%d"
        
        # *(I cannot find a less ugly way to filter column info with regex in pandas)
        
        dates = []
        
        # create datetime object of publication dates
        for pub_date in pub_dates:
            dates.append(datetime.strptime(pub_date, format_str).date())
        
        if (option == 'old'):
            """
                What if two years are the same? Choose the one with smallest index
                (min does this automatically)
            """
            
            # find index of ebook with smallest (oldest) publication date
            oldest = dates.index(min(dates))

            # get that ebook's number (to construct the download link)
            ebook_num = catalog[authors_catalog][book_listings][en][text]['Text#'].to_list()[oldest]
            
        if (option == 'young'):
            youngest = dates.index(max(dates))
            
            ebook_num = catalog[authors_catalog][book_listings][en][text]['Text#'].to_list()[youngest]
            
    # return the median or middlemost work
    elif (option == 'middle'):
        n = len(catalog[authors_catalog][book_listings][en][text]['Text#'].to_list())
        
        # if n is even
        if (n % 2 == 0):
            median = n/2
        elif (n % 2 != 0):
            median = (n + 1) / 2
            
        # fix off by one error with indexing
        median -= 1
            
        ebook_num = catalog[authors_catalog][book_listings][en][text]['Text#'].to_list()[int(median)]
    
    # return all the ebooks
    elif (option == 'all'): 
        ebook_num = catalog[authors_catalog][book_listings][en][text]['Text#'].to_list()
    
    return ebook_num

# take ebook number and find the subjects from the catalog
def find_subject(ebook_num):
    book = catalog[catalog["Text#"] == ebook_num]
    return(book['Subjects'].to_list())

if __name__ == "__main__":    
    # switches
    # display full dataframe
    pd.set_option('display.max_rows', None,
                  'display.max_columns', None)
    
    # constants
    catalog_name = "pg_catalog.csv"
    link_template = "https://www.gutenberg.org/cache/epub/"
    
    
    # download and write csv    
    download_write_file("https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv",
                        catalog_name, os.getcwd())
    
    # make sure letters with accents are encoded or we get NAAN for next step
    catalog = pd.read_csv(catalog_name, encoding="utf_8")
    catalog = catalog.dropna()
    display(catalog.head(5))
    
    # define list of works to get
    book_titles = {"Shakespeare, William": ["Hamlet", "Macbeth", "Much Ado about Nothing"],
                   "Eliot, George": ["Middlemarch"],
                   "Homer": ["The Odyssey"],
                   "Kant, Immanuel": ["The Critique of Pure Reason"]}
    
    # this is our output dataframe (which will be converted into a csv)
    book_titles_df = {"Author": [],
                      "Work": [],
                      "File names": [],
                      "Subjects": []}
                      # drama does not have a typical table of contents like other works (for preprocessing)
    book_titles_df = pd.DataFrame(book_titles_df)


    
    for i, (author, works) in enumerate(book_titles.items()):
    
        # find all titles available from an author
        authors_catalog = catalog['Authors'].str.contains(author, na=False)
        
        # print the doc number, work title, and author name for found results once
        print(f"\nWorks by {author} in Project Gutenberg catalog:")
        display(catalog[authors_catalog][['Text#', 'Title', 'Authors']].to_string())
    
        # these lists are needed for the output csv
        f_names = []
        subjects = []

        for work in works:
            # get the number of the ebook so we can download it
            # (if option = all, then ebook num is a list)
            ebook_num = find_choose_ebook(work, option='old')
            
            # int has no len()... are you serious. the length is 1 cmon!
            # this is a simple workaround. alternatively you could do option = all
            if (isinstance(ebook_num, int)):
                range_num = 1
            elif (isinstance(ebook_num, list)):
                range_num = len(ebook_num)
            
            for i in range(0, range_num):
                print(f"\n\nNow downloading {work} (book #{ebook_num})....\n\n")
                
                # create link
                if (isinstance(ebook_num, int)):
                    ebook_link = link_template + str(ebook_num) + '/pg' + str(ebook_num) + '.txt'
                    file_name = work.replace(' ', '_') + '.txt'
                    
                    # pandas can only output the string accurately as a list, so just take the only element
                    subjects.append(find_subject(ebook_num)[0])
                
                elif (isinstance(ebook_num, list)):
                    ebook_link = link_template + str(ebook_num[i]) + '/pg' + str(ebook_num[i]) + '.txt'
                    file_name = work.replace(' ', '_') + str(i + 1) + '.txt'
                    
                    # see above
                    subjects.append(find_subject(ebook_num[i])[0])
                
                f_names.append(file_name)

                # download text file
                book_path = os.path.join(os.getcwd(), 'text' + constants.PATH_DELIMITER)                                                
                download_write_file(ebook_link, file_name, book_path)
    
        # create a dataframe from the dictionary so we can save it as .csv for preprocessing
        book_list_path = os.path.join(os.getcwd(), "book_list.csv")

        # add new data to pre-existing dataframe
        new_df = pd.DataFrame({
            "Author": [author], # convert lists into strings with comma separation
             "Work": [','.join(map(str, works))],
             "File names": [','.join(map(str, f_names))],
             "Subjects": [','.join(map(str, subjects))]})
        
        book_titles_df = pd.concat([book_titles_df, new_df], ignore_index=True)
        book_titles_df.to_csv(book_list_path, index=False)
