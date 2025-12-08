#pragma once
#include <vector>
#include <cmath>
#include <stdexcept>
#include <algorithm>
#include <limits>
#include <map>
#include <assert.h>
#include "coords.h"
#include "util.h"

float cosine_similarity(const std::vector<short> &A, const std::vector<short> &B);
std::vector<std::vector<float>> cosine_similarity(const std::vector<std::vector<short>> &corpus);
bool comparision (float a, float b);
std::pair<Coords, float> find_max(const std::vector<std::vector<float>> &similarities);
std::vector<float> find_top_maxs(const std::vector<std::vector<float>> &similarities);