#pragma once
#include <vector>
#include <cmath>
#include <stdexcept>
#include <algorithm>
#include <limits>
#include <map>
#include <assert.h>
#include "coords.h"

std::vector<short> get_column(const std::vector<std::vector<short>> &v, const int &col_idx);
std::vector<float> get_column(const std::vector<std::vector<float>> &v, const int &col_idx);
float cosine_similarity(const std::vector<short> &A, const std::vector<short> &B);
std::vector<std::vector<float>> cosine_similarity(const std::vector<std::vector<short>> &corpus);
bool comparision (float a, float b);
std::pair<Coords, float> find_max(const std::vector<std::vector<float>> &similarities);