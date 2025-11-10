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

// template for outputting to table-like structure
const int WIDTH = 10;
template<typename T> void print_tbl(T t) {
    std::cout << std::left << std::setw(WIDTH) << t;
}
template<typename T> void print_ln(T t) {
    std::cout << t << std::endl;
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
    for (auto col_it = similarities.begin(); col_it != similarities.end(); ++col_it) {
        for (auto row_it = col_it->begin(); row_it != col_it->end(); ++row_it) {
            // print
            if (*row_it != 0) {
                print_tbl(*row_it);
            }
            
            // write to file
            if (row_it == col_it->end()) { // if on the last element
                file << *row_it;
            }
            else {
                file << *row_it << ",";
            }
        }
        print_ln("");
        file << "\n";
    }
    file.close();

    // find max cosine similarity between documents in corpus
    auto max = find_max(similarities);

    std::cout << "The greatest cosine similarity is between document " << max.first.x << " and document " << max.first.y 
    << ". The cosine similarity is " << max.second << std::endl;

    Statistics statistics(similarities);
    size_t n_col = similarities[0].size();

    std::cout << std::string("μ = ", statistics.get_mu());
    std::cout << std::string("σ = ", statistics.get_sigma());

    std::vector<double> pop_z_scores;
    for (auto& row : similarities) {
        for (auto& similarity : row) {
            pop_z_scores.push_back(statistics.pop_z_score(similarity));
        }
    }

    auto doc_means = statistics.doc_mean(similarities);
    auto doc_std_devs = statistics.doc_std_dev(similarities, doc_means);
    auto doc_z_scores = statistics.doc_z_score(similarities, doc_means, doc_std_devs);

    // preform a sanity check (these vectors should all be of equal size)
    assert(doc_means.size() == doc_std_devs.size());
    assert(pop_z_scores.size() == doc_z_scores.size());
    
    // if passed..
    auto n_elements = doc_means.size();
    for (auto i = 0; i < n_elements; ++i) {
        print_ln(std::string("For document ", i + 1));
        print_ln(std::string("Mean is ", doc_means[i]));
        print_ln(std::string("Standard deviation is ", doc_std_devs[i]));
        print_ln(std::string("Local z-score is ", doc_z_scores[i]));
        print_ln(std::string("Population z-score is ", pop_z_scores[i]));
    }
    
    return(0);
}