#include <iostream>
#include <iomanip>
#include <iterator>
#include <filesystem>
#include <fstream>
#include <regex>

#include "cosineSimilarity.h"
#include "mmReader.h"
#include "stat.h"
#include "util.h"

/*
    Input: 1 corpus in MM format that has the same amount of vocabulary terms (dot-product limitation) 
    Output: The most similar documents in each corpus and most similar documents between corpora, save them to file
*/
const static std::filesystem::path CLOUDPOINT_FOLDER = std::filesystem::current_path() / "docs_similarity_pointcloud";
const static std::filesystem::path RESULTS_FOLDER = std::filesystem::current_path() / "results";
const static std::vector<std::filesystem::path> FOLDERS = {CLOUDPOINT_FOLDER, RESULTS_FOLDER};

// template for outputting to table-like structure
template<typename T> void print_tbl(T t) {
    const int WIDTH = 10;
    std::cout << std::left << std::setw(WIDTH) << t;
}
template<typename T> void print_ln(T t) {
    std::cout << t << std::endl;
}

void createFolders() {
    for (auto& folder : FOLDERS) {
        if (!std::filesystem::exists(folder)) {
            std::filesystem::create_directory(folder);
        }
    }
}

// get the file name without the path by removing delimiter until final substring is found
auto getPathlessFname(std::string corpus_path) {
    const std::string PATH_DELIMITER = "\\";

    while (corpus_path.find(PATH_DELIMITER) != std::string::npos) {
        corpus_path.erase(0, corpus_path.find(PATH_DELIMITER) + PATH_DELIMITER.length());
    }

    return(corpus_path);
}

// replace _corpus.corpus with user ending
std::string createFName(std::string pathless_fname, std::string ending) {
    return (std::regex_replace(pathless_fname, std::regex("_corpus.corpus"), ending));
}

// print function to be used by std::for_each()
void print(const double element) {
    print_tbl(element);
}

template<typename T, typename A> void write_to_csv(const std::vector<T,A> &v, const std::filesystem::path SAVE_PATH) {
    std::ofstream file(SAVE_PATH);
    const std::ostream_iterator<T> output_itr(file, ",");
    std::copy(v.begin(), v.end(), output_itr);
    file.close();
}

int main(const int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Current commands are: ";
        for(int i = 0; i < argc; ++i){
            std::cerr << argv[i];
        }
        throw std::invalid_argument("Usage: ./find_similar_docs.exe [path to corpus]");
    }    

    // set up write to file...    
    auto corpus_path = std::string(argv[1]);
    auto pathless_fname = getPathlessFname(corpus_path);
    createFolders();

    // read-in input data
    // get 2d vector representation of Market Matrix (BoW corpus from Gensim)
    mmReader Reader(corpus_path);
    auto corpus = Reader.readMM();

    // compute upper-triangle of cosine similarity between documents in corpus
    auto similarities = cosine_similarity(corpus);

    // print out cosine similarities and write to file    
    // create file
    const auto CLOUDPOINT_FNAME = createFName(pathless_fname, "_pointcloud.csv");
    const auto CLOUDPOINT_SAVE_PATH = CLOUDPOINT_FOLDER / CLOUDPOINT_FNAME;
    std::ofstream cloud_file(CLOUDPOINT_SAVE_PATH);

    // print + write
    for (auto col_it = similarities.begin(); col_it != similarities.end(); ++col_it) {
        for (auto row_it = col_it->begin(); row_it != col_it->end(); ++row_it) {
            // print
            if (*row_it != 0) {
                print_tbl(*row_it);
            }
            
            // write to file
            if (row_it == col_it->end()) { // if on the last element
                cloud_file << *row_it;
            }
            else {
                cloud_file << *row_it << ",";
            }
        }
        print_ln("");
        cloud_file << "\n";
    }
    cloud_file.close();

    // find max cosine similarity between documents in corpus
    auto max = find_max(similarities);

    std::cout << "The greatest cosine similarity is between document " << max.first.x << " and document " << max.first.y 
    << ". The cosine similarity is " << max.second << std::endl;

    // get sorted matrix
    auto out_maxs = find_top_maxs(similarities);

    // write
    const auto MAXS_FNAME = createFName(pathless_fname, "_MAXS.csv");
    const auto MAXS_SAVE_PATH = RESULTS_FOLDER / MAXS_FNAME;
    write_to_csv(out_maxs, MAXS_SAVE_PATH);

    // print
    std::for_each(out_maxs.begin(), out_maxs.end(), print);

    /*          STATS           */

    Statistics statistics(similarities);

    print_ln("μ = " + std::to_string(statistics.get_mu()));
    print_ln("σ = " + std::to_string(statistics.get_sigma()));

    auto doc_means = statistics.doc_mean(similarities);
    auto doc_std_devs = statistics.doc_std_dev(similarities, doc_means);
    auto doc_z_scores = statistics.doc_z_score(similarities, doc_means, doc_std_devs);
    auto pop_z_scores = statistics.pop_z_score(similarities);

    // preform a sanity check (these vectors should all be of equal size)
    assert(doc_means.size() == doc_std_devs.size());
    assert(pop_z_scores.size() == doc_z_scores.size());
    
    // if passed..
    // print + save
    const auto RESULTS_FNAME = createFName(pathless_fname, "_results.txt");
    const auto RESULTS_SAVE_PATH = RESULTS_FOLDER / RESULTS_FNAME;
    std::ofstream results_file(RESULTS_SAVE_PATH);

    auto n_docs = similarities.size();
    for (auto i = 0; i < n_docs; ++i) {
        print_ln("For document " + i + 1);
        print_ln("Mean is " + std::to_string(doc_means[i]));
        print_ln("Standard deviation is " + std::to_string(doc_std_devs[i]));

        results_file << "For document " << i + 1 << std::endl;
        results_file << "Mean is " << doc_means[i] << std::endl;
        results_file << "Standard deviation is " << doc_std_devs[i] << std::endl;
    }
    results_file.close();
        
    // print + save pop z-scores
    const auto POP_Z_SCORE_FNAME = createFName(pathless_fname, "pop_z_score.csv");
    const auto POP_Z_SCORE_SAVE_PATH = RESULTS_FOLDER / POP_Z_SCORE_FNAME;
    write_to_csv(pop_z_scores, POP_Z_SCORE_SAVE_PATH);

    print_ln("Population z-scores for cosine similarity matrix: ");
    std::for_each(pop_z_scores.begin(), pop_z_scores.end(), print);

    // print + save doc z-scores
    const auto DOC_Z_SCORE_FNAME = createFName(pathless_fname, "doc_z_score.csv");
    const auto DOC_Z_SCORE_SAVE_PATH = RESULTS_FOLDER / DOC_Z_SCORE_FNAME;
    write_to_csv(doc_z_scores, DOC_Z_SCORE_SAVE_PATH);

    print_ln("Document-sampled z-scores for cosine similarity matrix: ");
    std::for_each(doc_z_scores.begin(), doc_z_scores.end(), print);
    
    return(0);
}