#include "cosineSimilarity.h"
#include <iostream>

// there must be a better way of doing this..
// (it doesn't look like there is)
std::vector<short> get_column(const std::vector<std::vector<short>> &v, const int &col_idx) {
    std::vector<short> return_v;
    for (const auto &row : v) {
        return_v.push_back(row.at(col_idx));
    }

    return(return_v);
}

float cosine_similarity(const std::vector<short> &A, const std::vector<short> &B) {
    int ncomp = 0;
    if (A.size() != B.size()) {
        throw std::invalid_argument("Size of vectors is not the same (must be for dot product)");
    }
    else {
        ncomp = A.size();
    }

    short dot_product = 0, mag_A = 0, mag_B = 0;
    for (int i = 0; i < ncomp; ++i) {
        dot_product += A[i] * B[i];
        mag_A += A[i] * A[i];
        mag_B += B[i] * B[i];
    }

    return (dot_product / (std::sqrt(mag_A) * std::sqrt(mag_B)));
}

std::vector<std::vector<float>> cosine_sim(const std::vector<std::vector<short>> &A) {
    size_t n_col = A[0].size();
    // define resulting square matrix
    std::vector<std::vector<float>> cosim_matrix(n_col, std::vector<float>(n_col));

    // calculate upper-triangle of matrix by iterating through columns
    for (int i = 0; i < n_col; ++i) {
        for (int j = 0; j <= i; ++j) {
            if (j < i) { // only actual calculation
                cosim_matrix[i][j] = cosine_similarity(get_column(A, i), get_column(A, j));
            }
            else if (i == j) { // occurs after calculation except for first pass
                cosim_matrix[i][j] = 1;
            }
        }
    }

    return (cosim_matrix);
}

std::pair<std::string, double> find_max(std::map<std::string, double> &similarities) {
    // return greatest element and key with lambda function
    auto max = std::max_element(similarities.begin(), similarities.end(), 
    [](const auto &x, const auto &y) {
            return (x.second < y.second); });
    // return key-value pair
    return(std::pair<std::string, double>(max->first, max->second));
}


std::vector<std::vector<float>>::const_iterator find_greatest(const std::vector<std::vector<float>> &similarities) {
    auto max = std::max_element(similarities.begin(), similarities.end());
    return(max);
}