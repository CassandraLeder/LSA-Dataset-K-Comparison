#include "cosineSimilarity.h"

// helper function to cosine similarity for corpus. this function computes the cosine similarity between two column vectors A and B
float cosine_similarity(const std::vector<short> &A, const std::vector<short> &B) {
    // check the sizes of the column vectors
    assert((A.size() == B.size()) && "Size of vectors is not the same (must be for dot product)");
    auto n_comp = A.size();

    short dot_product = 0, mag_A = 0, mag_B = 0;
    for (size_t i = 0; i < n_comp; ++i) {
        dot_product += A[i] * B[i];
        mag_A += A[i] * A[i];
        mag_B += B[i] * B[i];
    }
        // = sigma(A[i] * B[i]) / (sqrt(sigma(A[i]^2)) * sqrt(sigma(B[i]^2)))
    return (dot_product / (std::sqrt(mag_A) * std::sqrt(mag_B)));
}

// take a whole corpus and return a cosine similarity matrix
std::vector<std::vector<float>> cosine_similarity(const std::vector<std::vector<short>> &corpus) {
    size_t n_col = corpus[0].size(); // assume that every row vector has same size (they should)
    // define resulting square matrix
    std::vector<std::vector<float>> cosim_matrix(n_col, std::vector<float>(n_col));

    // calculate upper-triangle of matrix by iterating through columns
    for (int i = 0; i < n_col; ++i) {
        for (int j = 0; j < n_col; ++j) { // "<=" because we want to ignore the condition where j > i (extracting upper-triangle with diagonal)
            if (j > i) { // only actual calculation
                cosim_matrix[i][j] = cosine_similarity(get_column(corpus, i), get_column(corpus, j));
            }
            else if (i == j) { // occurs after calculation except for first pass
                cosim_matrix[i][j] = 1;
            }
        }
    }

    return (cosim_matrix);
}

// comparison function to be used to find max (ignores diagonal by turning 1s into 0s)
bool comparision (float a, float b) {
    a = a == 1 ? 0 : a; // if a == 1, a = 0; else a = a
    b = b == 1 ? 0 : b;
 
    return (a < b); 
}

// find the max float from a cosine similarity matrix ignoring the 1 diagonal
std::pair<Coords, float> find_max(const std::vector<std::vector<float>> &similarities) {
    // create min vector for initalization of max iterator
    std::vector<float> MIN_VECTOR = {std::numeric_limits<float>::min()};
    std::vector<float>::const_iterator iter_max = MIN_VECTOR.begin();

    // for each row in 2d vector, find the greatest element, use if statement to find actual max
    int i = 0;
    int max_row_idx = 0;
    for (const auto &row : similarities) {
        auto max = std::max_element(row.begin(), row.end(), comparision); // may return 1 is max in the case that 1 is the only non-zero in row (so first row only)
        // find actual max
        if (*max != 1 && *max > *iter_max) {
            iter_max = max; // iterator to actual max
            max_row_idx = i; // row where max is located
        }
        ++i;
    }
    // find indices of iterator max
    int max_col_idx = std::distance(similarities[max_row_idx].begin(), iter_max);
    
    Coords coords; // could also use std::pair<int,int> then std::pair<std::pair<int,int> float> (I prefer this because there's no max.first.first in main vs. max.first.x)
    coords.x = max_row_idx; coords.y = max_col_idx;
    
    std::pair<Coords, float> index_max = {coords, *iter_max};
    
    return(index_max);
}

// return sorted flattened 1d vector of 2d cosine similarity vector
std::vector<float> find_top_maxs(const std::vector<std::vector<float>> &similarities) {
    std::vector<float> v;

    for (auto &row : similarities) {
        for (auto &similarity : row) {
            if (similarity != 0 && similarity != 1) {
                v.push_back(similarity);
            }
        }
    }
    // use greater as comparator to sort in descending order (greatest first)
    std::sort(v.begin(), v.end(), std::greater<>());
    return(v);
}