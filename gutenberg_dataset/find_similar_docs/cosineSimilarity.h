#pragma once
#include <vector>
#include <string>
#include <cmath>
#include <stdexcept>
#include <algorithm>
#include <map>

std::vector<short> get_column(const std::vector<std::vector<short>> &v, const int &col_idx);
float cosine_similarity(const std::vector<short> &A, const std::vector<short> &B);
std::vector<std::vector<float>> cosine_sim(const std::vector<std::vector<short>> &A);
std::pair<std::string, double> find_max(std::map<std::string, double> &similarities);
std::vector<std::vector<float>>::const_iterator find_greatest(const std::vector<std::vector<float>> &similarities);