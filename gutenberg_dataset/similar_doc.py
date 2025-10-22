"""
Find most similar documents before and after dimensionality reduction (SVD) done by LSA
"""

import gensim
from ripser import ripser
from persim import plot_diagrams
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os

class doc:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        
    def find_similar_documents(self, corpora):
            """
            docs is a 2d sparse matrix where the docs are columns,
            so we need to find the similarity of each column pf each doc obj 
            """
            return(cosine_similarity(corpora))
    
    def find_similar_documents(self, corpusA, corpusB):
        similarities = []
        x_ndocs = np.shape(corpusA)[1]
        y_ndocs = np.shape(corpusB)[1]
        for i in range(0,x_ndocs):
            for j in range(0,y_ndocs):
                similarities.append(cosine_similarity(corpusA[:,i], corpusB[:,j]))
        return(similarities)
    
    # where A is population (matrix representing entire corpus of docs) and x is cosine-sim for doc in A
    def find_zscore(self, x, A):
        mu = np.mean(A)
        sigma = np.std(A)
        return((x-mu) / sigma)        
        
    # example code taken from Ripser
    def persistent_homology(data):
        diagrams = ripser(data)['dgms']
        plot_diagrams(diagrams, show=True)
        
        

# use this class to find corpora from directory and store as sparse-array obj
class doc_before_LSA(doc):
    def __init__(self, root_dir):
        super().__init__(root_dir=root_dir)
             
    def __find_corpora(self, dir):
        list_ = os.listdir(dir)
        list_.sort()
        # get files that have "_corpus" but not "_corpus.index" (used for reading in corpora in gensim)
        return([fname for fname in list_ if "_corpus" in fname and ".index" not in fname])
        
    def __read_corpus(self, file_path):
        corpus = gensim.corpora.MmCorpus(file_path)
        dict_fname = file_path.replace('_corpus', '_dictionary.dict')
        dictionary = gensim.corpora.Dictionary.load(dict_fname)
        return(gensim.matutils.corpus2csc(corpus, len(dictionary)))
    
    
    def read(self):
        corpora = self.__find_corpora(self.root_dir)
        Corpora = [] # list of gensim corpora objs
        for corpus in corpora:
            fname = os.path.join(self.root_dir, corpus)
            Corpora.append(self.__read_corpus(fname))            
        [print(corpus) for corpus in Corpora]
        return(Corpora)
    
    def find_similar_documents(self, corpora):
        similarities = []
        print(super().find_similar_documents(corpora[0], corpora[1]))
        # get the cosine similiarity of every corpus to every other corpus (cols are docs)
        for corpus in corpora:
            similarities.append(super().find_similar_documents(corpus))
        
        return(similarities)

class doc_after_LSA(doc):
    def __init__(self, root_dir):
        super().__init__(root_dir=root_dir)
        
    def __find_cosineSim(self):
        list_ = os.listdir(self.root_dir)
        return([fname for fname in list_ if "cosineSim" in fname])
    
    # not exactly necessary but extracts *how* docvecs are read as oppossed to docs
    def __read_cosineSim(self, fname):
        return(np.load(fname))
    
    def read(self):
        fnames = self.__find_cosineSim()
        return([self.__read_cosineSim(os.path.join(self.root_dir, fname)) for fname in fnames])
    
    def find_similar_documents(self, cosineSim):
        print(cosineSim)
        return(max(cosineSim))
    
if __name__ == "__main__":
    """
    if (len(sys.argv) != 2):
        raise ValueError('Usage: [path to root dir containing doc dirs] [path to dir containing docvecs]')
    """
    data = np.random.random((100,2))
    print(data)
    # set switch
    # (first arg is always the file)
    print(os.getcwd())
    text_obj = doc_before_LSA(os.path.join(os.getcwd(), "corpus\\"))
    docvecs_obj = doc_after_LSA(os.path.join(os.getcwd(), "models"))

    # find most similar docs
    Corpora = text_obj.read()
    similarities_before = text_obj.find_similar_documents(Corpora)
    similarities_after = docvecs_obj.find_similar_documents(docvecs_obj.read())
    
    # output the result
    print(f"The most similar documents before reduction were {max(similarities_before, key=similarities_before.get)}.")
    print(f"The most similar documents after reduction are {max(similarities_after, key=similarities_after.get)}.")