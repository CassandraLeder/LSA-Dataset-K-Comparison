#include <iostream>
#include <iomanip>
#include <filesystem>
#include <fstream>
#include <regex>
#include "cosineSimilarity.h"
#include "mmReader.h"
#include "stat.h"

/*
    Input: 1 corpus in MM format that has the same amount of vocabulary terms (dot-product limitation) 
    Output: The most similar documents in each corpus and most similar documents between corpora, save them to file
*/
const static std::filesystem::path SAVE_FOLDER = std::filesystem::current_path() / "../most_downloaded_dataset" / "docs_similarity_pointcloud";
const static std::string PATH_DELIMITER = "\\";

const int WIDTH = 10;
template<typename T> void print(T t) {
    std::cout << std::left << std::setw(WIDTH) << t;
}

// get the file name without the path by removing delimiter until final substring is found
auto getPathlessFname(std::string corpus_path) {
    while (corpus_path.find(PATH_DELIMITER) != std::string::npos) {
        corpus_path.erase(0, corpus_path.find(PATH_DELIMITER) + PATH_DELIMITER.length());
    }

    return(corpus_path);
}

int main(const int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Current commands are: ";
        for(int i = 0; i < argc; ++i){
            std::cerr << argv[i];
        }
        throw std::invalid_argument("Usage: ./find_similar_docs.exe [path to corpus]");
    }    

    // get 2d vector representation of Market Matrix (BoW corpus from Gensim)
    std::string corpus_path = std::string(argv[1]);
    mmReader Reader(corpus_path);
    auto corpus = Reader.readMM();

    // compute upper-triangle of cosine similarity between documents in corpus
    auto similarities = cosine_similarity(corpus);

    // print out cosine similarities and write to file

    // set up write to file...    
    auto pathless_fname = getPathlessFname(corpus_path);

                                                            // replace _corpus.corpus with _pointcloud.csv
    std::string file_name = std::regex_replace(pathless_fname, std::regex("_corpus.corpus"), "_pointcloud.csv");
    if (!std::filesystem::exists(SAVE_FOLDER)) { // create directory
        std::filesystem::create_directory(SAVE_FOLDER);
    }
    
    // create file
    const std::filesystem::path SAVE_PATH = SAVE_FOLDER / file_name;
    std::ofstream file(SAVE_PATH);

    // print + write
    for (int i = 0; i < similarities.size(); ++i) {
        for (int j = 0; j < similarities[i].size(); ++j) {
            // print
            if (similarities[i][j] != 0) {
                print(similarities[i][j]);
            }
            
            // write to file
            if (j != similarities[i].size()) {
                file << similarities[i][j] << ",";
            }
            else {
                file << similarities[i][j] << "\n";
            }
        }
        print("\n");
    }
    file.close();

    // find max cosine similarity between documents in corpus
    auto max = find_max(similarities);

    std::cout << "The greatest cosine similarity is between document " << max.first.x << " and document " << max.first.y 
    << ". The cosine similarity is " << max.second << std::endl;
    
    // create van-ripps diagrams


    return(0);
}