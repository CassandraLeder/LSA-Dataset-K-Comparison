#pragma once

#include <vector>

/*
    UTIL.H
    Define utility templates that are shared across files
*/

// there must be a better way of doing this..
// (it doesn't look like there is)
// take in a 2d vector (corpus) and return just the column requested
template<typename T, typename A> 
std::vector<T> get_column(const std::vector<std::vector<T,A>> &v, const int &col_idx) {
    std::vector<T> return_v;
    for (const auto &row : v) {
        return_v.push_back(row.at(col_idx));
    }

    return(return_v);
}