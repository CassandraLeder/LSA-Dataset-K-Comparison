#include <iostream>
#include <array>
#include "cosineSimilarity.h"
#include "mmReader.h"

/*
    Input: 2 corpora in MM format that have the same amount of vocabulary terms (dot-product limitation)
    Output: The most similar documents in each corpus and most similar documents between corpora
*/

const int NUM_CORPORA = 2;

bool is_corpus_size_same(const std::size_t &corpus_0_size, const std::array<std::vector<std::vector<double>>, NUM_CORPORA> &corpora) {
    for (auto &corpus : corpora) {
        if (corpus.size() != corpus_0_size) {
            return(false);
        }
    }
    return(true);
}

int main(const int argc, char** argv) {
    
    if (argc < 2) {
        std::cerr << "Current commands are: ";
        for(int i = 0; i < argc; ++i){
            std::cerr << argv[i];
        }
        throw std::invalid_argument("Usage: ./find_similar_docs.exe [path to first corpus] [path to second corpus]");
    }    
    // create arrays for data and calculation
    std::array<mmReader, NUM_CORPORA> readers;
    std::array<std::vector<std::vector<double>>, NUM_CORPORA> corpora;
    std::array<std::map<std::string, double>, NUM_CORPORA> similarities;
    std::array<std::pair<std::string, double>, NUM_CORPORA> best_docs;

    for (int i = 0; i < NUM_CORPORA; ++i) {
        // get 2d vector representation of MM doc
        readers[i].setFilePath(argv[i+1]);
        corpora[i] = readers[i].readMM();
        // cosine similarity on entire corpus
        similarities[i] = cosine_similarity_corpus(corpora[i]);
        // find most similar doc pair from corpus
        best_docs[i] = find_max(similarities[i]);
    }
    
    // output best doc pairs
    int i = 1;
    for (auto &best_doc : best_docs) {
        std::cout << "Corpus " << i << " best docs are: " << best_doc.first << " " << best_doc.second << std::endl;
        ++i;
    }
    
    // check that corpus sizes are the same
    const std::size_t corpus_0_size = corpora[0].size();
    if (!is_corpus_size_same(corpus_0_size, corpora)) {
        std::cout << "\nCorpora sizes:";
        for (auto &corpus : corpora) {
            std::cerr << corpus.size();
        }
        throw std::invalid_argument("Corpora sizes are not equal.");
    }
    
    // else they are equal

    // get the cosine similarities between the corpora
    std::vector<double> corpora_similarities;
    for (int i = 0; i < corpus_0_size; ++i) {
        // columns in the matrix represent documents
        auto doc_i = get_column(corpora[i], i);
        for (int j = i + 1; j < corpus_0_size; ++j) {
            auto doc_j = get_column(corpora[j], j);
            corpora_similarities.push_back(cosine_similarity(doc_i, doc_j));
        }
    }
}