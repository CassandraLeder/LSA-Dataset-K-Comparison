#include "cosineSimilarity.h"

// there must be a better way of doing this..
// (it doesn't look like there is)
std::vector<double> get_column(const std::vector<std::vector<double>> &v, const int &col_idx) {
    std::vector<double> return_v;
    for (const auto &row : v) {
        return_v.push_back(row.at(col_idx));
    }

    return(return_v);
}

double cosine_similarity(const std::vector<double> &A, const std::vector<double> &B) {
    int ncomp = 0;
    if (A.size() != B.size()) {
        throw std::invalid_argument("Size of vectors is not the same (must be for dot product)");
    }
    else {
        ncomp = A.size();
    }

    double dot_product = 0.0, mag_A = 0.0, mag_B = 0.0;
    for (int i = 0; i < ncomp; ++i) {
        dot_product += A[i] * B[i];
        mag_A += A[i] * A[i];
        mag_B += B[i] * B[i];
    }

    return (dot_product / (std::sqrt(mag_A) * std::sqrt(mag_B)));
}

double mean(const std::vector<double> &similarities) {
    auto sum = 0.0;

    for (auto &sim : similarities) {
        sum += sim;
    }

    return(sum / similarities.size());
}

double std_dev(const std::vector<double> &similarities, const double &mu) {
    auto sum = 0.0;
    
    for (auto &sim : similarities) {
        sum += (sim - mu) * (sim - mu);
    }

    return(sqrt((sum / similarities.size())));
}

double z_score(const double &x, const double& mu, const double& sigma) {
    return ((x - mu) / sigma);
}

std::pair<std::string, double> find_max(std::map<std::string, double> &similarities) {
    // return greatest element and key with lambda function
    auto max = std::max_element(similarities.begin(), similarities.end(), 
    [](const auto &x, const auto &y) {
            return (x.second < y.second); });
    // return key-value pair
    return(std::pair<std::string, double>(max->first, max->second));
}

// find the cosine similarity of an entire corpus
std::map<std::string, double> cosine_similarity_corpus(const std::vector<std::vector<double>> &corpus) {
    /* 
    rows are stored as vectors in 2d vector, 
    so get the columns as rows of a new 2d vector
    */
    std::vector<std::vector<double>> docs;
    for (int i = 0; i < corpus[0].size(); ++i) { // column size is equal to size of any row vector
        docs.push_back(get_column(corpus, i));
    }
    // now we have extracted the documents (columns) from the corpus matrix
    
    // get cosine similarity between each doc in corpus
    std::map<std::string, double> similarities;
    for(int i = 0; i < docs.size(); ++i) {
        for (int j = i+1; j < docs.size(); ++j) {
            double similarity = cosine_similarity(docs[i], docs[j]);
            std::string sim_str = std::to_string(i+1) + "->" + std::to_string(j+1);
            
            similarities.insert({sim_str, similarity});
        }
    }
    return(similarities); 
}