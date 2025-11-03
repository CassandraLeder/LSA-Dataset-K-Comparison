#include <iostream>
#include <fstream>
#include <regex>
#include "cosineSimilarity.h"
#include "mmReader.h"
#include "stat.h"

/*
    Input: 1 corpus in MM format that has the same amount of vocabulary terms (dot-product limitation)
    Output: The most similar documents in each corpus and most similar documents between corpora
*/

int main(const int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Current commands are: ";
        for(int i = 0; i < argc; ++i){
            std::cerr << argv[i];
        }
        throw std::invalid_argument("Usage: ./find_similar_docs.exe [path to corpus]");
    }    

    std::string corpus_path = std::string(argv[1]);


    // create variables for data and calculation
    mmReader Reader;

    // get 2d vector representation of Market Matrix (BoW corpus from Gensim)
    Reader.setFilePath(corpus_path);
    auto corpus = Reader.readMM();

    // compute upper-triangle of cosine similarity between documents in corpus
    auto similarities = cosine_sim(corpus);

    // print out cosine similarities and write to file

    // get the file name without the path
    std::regex path_delimiter("\\");
    std::sregex_token_iterator it(corpus_path.begin(), corpus_path.end(), 
    path_delimiter,
    -1);
    std::string pathless_fname = "";

    std::sregex_token_iterator end;
    for(; it != end; ++it) {
        pathless_fname = *it;
    }

                                                            // replace _corpus.corpus with _pointcloud.csv
    std::string file_name = std::regex_replace(pathless_fname, std::regex("_corpus.corpus"), "_pointcloud.csv");
    std::ofstream file(file_name);

    for (int i = 0; i < similarities.size(); ++i) {
        for (int j = 0; j < similarities[i].size(); ++j) {
            // print
            if (similarities[i][j] != 0) {
                std::cout << similarities[i][j] << " ";
            }
            
            // write to file
            if (j != similarities[i].size()) {
                file << similarities[i][j] << ",";
            }
            else {
                file << similarities[i][j] << "\n";
            }
        }
        std::cout << std::endl;
    }

    auto greatest = find_greatest(similarities);
    //auto similarities = cosine_similarity_corpus(corpus);
    // find most similar doc pair from corpus
    //auto best_docs = find_max(similarities);

    // output similarities / best doc pairs
    /*
    std::cout << "Similarities are: \n";
    for (auto& similarity : similarities) {
        std::cout << similarity.first << " " << similarity.second << std::endl;
    }
    std::cout << "Corpus' best docs are: " << best_docs.first << " " << best_docs.second << std::endl;
    */

    return(0);
}