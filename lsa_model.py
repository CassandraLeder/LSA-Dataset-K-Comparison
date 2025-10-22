"""
# cassandra leder based on example code by zachary k stine
# 2024-10-25
#
# Train many LSA models for K = {5, 100, 200, 300, 500, 700} 
# Find document cosine similarities for each model, 
# then get the pearson correlation for the similarity matricies
# Save all of the above to file
"""

import os
import sys
import gensim
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import networkx as nx
from math import ceil

def get_corpus_name(corpus_fname):
    # slice all non '_corpus' out of fname
    if (corpus_fname.find("_corpus") != -1):
        corpus_name = corpus_fname[:corpus_fname.find("_corpus")]
    else:
        raise ValueError(f'_corpus not found in {corpus_fname}!')
    return(corpus_name)

class model_:
    doc_similarity = {} # dictionary of cosine similarities
    # below are gensim objects
    model = ''
    dictionary = ''
    corpus = ''
    
    def __init__(self, k):
        self.k = k

    # abstract the lsa function into parts
    """
    # 1. read in processed corpus
    """    
    def load_data(self, data_dir, dictionary_fname, corpus_fname):
        self.dictionary = gensim.corpora.Dictionary.load(os.path.join(data_dir, dictionary_fname))
        self.corpus = gensim.corpora.MmCorpus(os.path.join(data_dir, corpus_fname))
        
        if(len(self.corpus) == 0):
            raise ValueError(f'Corpus {corpus_fname} equal to 0!')
        else:
            print(f"Total number of documents in corpus: {len(self.corpus)}")
            return()
        
    """        
    # 2. get TFIDF-weighted matrices
    """
    def get_tfidf(self):
        tfidf_model = gensim.models.TfidfModel(self.corpus)
        corpus_tfidf = tfidf_model[self.corpus]

        return(corpus_tfidf)
    
    """
    # 3. Get the lsa model for value of k, get document vectors for the # of docs in doc_count    
    """
    def lsa(self, dest_dir, corpus_tfidf, doc_count = 'corpus_length'):
        doc_count = len(self.corpus) if doc_count == 'corpus_length' else doc_count
        num_topics = ceil(self.k * len(self.corpus))
        print(f"Number of topics for k = {self.k * 100}%: {num_topics}")
        lsa_model = gensim.models.LsiModel(corpus_tfidf, num_topics=num_topics, id2word=self.dictionary)
            
        # save model for reference
        model_fpath = os.path.join(dest_dir, 'lsa_k-' + str(self.k) + '.model')
        lsa_model.save(model_fpath)
        
        """
        # get doc vectors for sample docs and write to file.
        """
        doctopic_matrix = np.zeros((doc_count, num_topics))

        for doc_idx, doc in enumerate(self.corpus[:doc_count]):
            docvec = lsa_model[doc]
            for topic_idx, value in docvec:
                doctopic_matrix[doc_idx, topic_idx] = value
        return (lsa_model, doctopic_matrix)
    """
    # Find connections between documents in document network using cosine similarity
    """
    def cosineSim(self, doc_matrix):
        similarity = cosine_similarity(doc_matrix)
        self.doc_similarity[f"k = {self.k} similarity"] = similarity
        return (similarity)
    
    """
    # the run function for LSA
    """
    def run_lsa(self, data_dir, dest_dir, dictionary_fname, corpus_fname, doc_count='corpus_length'):
        # load corpus/dictionary
        self.load_data(data_dir, dictionary_fname, corpus_fname)
        # get lsa models
        (lsa_model, doctopic_matrix) = self.lsa(dest_dir, self.get_tfidf(), doc_count=doc_count)
        self.model = lsa_model
        # compute similarity matrix (cosine similarity)
        similarity = self.cosineSim(doctopic_matrix)

        # save files
        corpus_name = get_corpus_name(corpus_fname)
        lsa_docvectors_fpath = os.path.join(dest_dir, corpus_name + '_lsa_docvecs_k-' + str(self.k))
        np.save(lsa_docvectors_fpath, doctopic_matrix)
        
        lsa_cosinesim_fpath = os.path.join(dest_dir, corpus_name + '_lsa_cosineSim_k-' + str(self.k))
        np.save(lsa_cosinesim_fpath, similarity)
        
        return (lsa_model)
        

class network_model:
    lsa_models = []
    models = []
    def __init__(self, k_list, graph_fpath, connections):
        for k in k_list:
            self.models.append(model_(k))
        self.k_list = k_list
        self.graph_fpath = graph_fpath
        self.connections = connections # dictionary of possible connections in network

    # create graph for network and output graphxml file to graph_fpath
    def create_graph(self):
        # create graph
        G = nx.Graph()
            
        # add nodes
        G.add_nodes_from(self.k_list)
            
        # create edges and edge weight
        for i, k_i in enumerate(self.k_list):
            for j, k_j in enumerate(self.k_list):
                if (k_i != k_j and f"{k_i}->{k_j}" in self.connections):
                    rounded_weight = round(self.connections[f"{k_i}->{k_j}"], 4)
                    G.add_edge(k_i, k_j, weight=rounded_weight)
            
        # create layout, get edges
        pos = nx.spring_layout(G, k=10)
        e = [(u,v) for (u,v,d) in G.edges(data=True)]
            
        # draw graph
        nx.draw_networkx_nodes(G, pos, node_size=1200, node_color="gray")
        nx.draw_networkx_edges(G, pos, edgelist=e, width=2)
            
        # add labels
        nx.draw_networkx_labels(G, pos, font_size = 20, font_family="serif")
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels)
            
        # show graph to screen
        plt.show()
            
        # output graphxml file
        nx.write_graphml(G, self.graph_fpath)
        
    # Find pearson connections between similarity matricies in model network
    def correlationCoeff(self):
        # for every model in the network, get the correlation
        correlations = []
        
        for i, model_i in enumerate(network.models):
            for j, model_j in enumerate(network.models):
                
                similarity_i = list(model_i.doc_similarity.values())
                similarity_j = list(model_j.doc_similarity.values())
                
                # check that i != j and key not already in dictionary
                if (i != j 
                    and f"{model_i.k}->{model_j.k}" not in network.connections 
                    and f"{model_j.k}->{model_i.k}" not in network.connections):
                    pear = pearsonr(similarity_i[0].flatten(),
                                    similarity_j[0].flatten())[0]
                
                    correlations.append(pear)
                    # ex. 5->100 = .0555
                    network.connections[f"{model_i.k}->{model_j.k}"] = pear
                
        return correlations
"""
    Usage:
        ./lsa_model [path to data directory] [dictionary name] [corpus name]
"""
if __name__ == '__main__':
    for arg in sys.argv:
        print(arg)
    if len(sys.argv) < 4:
        raise ValueError("Usage: ./lsa_model [path to data directory] [dictionary name] [corpus name]")
    
    data_dir = os.path.join(os.getcwd(), sys.argv[1])
    dest_dir = os.path.join(os.getcwd(), 'models')
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    corpus_name = get_corpus_name(sys.argv[3])

    """
    # 1. Separate ks into 1 network(s) of models for experiments
    """
    networks = []
    networks.append(network_model(k_list = [.01, .05, .1, .5, .65, .75, .80, .85, .90, .95, .99],
                                  graph_fpath=os.path.join(dest_dir, corpus_name + '_k-network.graphml'),
                                  connections={}))
    
    """
    # 2. For each seperate network, get lsa models for each k value
    # Then get pearson correlation for each lsa model's cosine similarity matrix*
        *(calculated in lsa function)
    """
    for network in networks:
        # get LSA models
        for model in network.models:
            # get lsa model from model_ object in network_model object
            lsa_model = model.run_lsa(data_dir,
                                      dest_dir,
                                      sys.argv[2],
                                      sys.argv[3])
            # add to network models
            network.lsa_models.append(lsa_model)
            # output topic vectors
            print("k = ", model.k)
            print(model.model.print_topics()) 
            
        # get pearson coefficients
        correlations = network.correlationCoeff()
        print(network.connections)
        
        # save correlation to file
        lsa_correlation_fpath = os.path.join(dest_dir, corpus_name + '_lsa_correlation')
        np.save(lsa_correlation_fpath, correlations)
        
        # create/output graph
        network.create_graph()