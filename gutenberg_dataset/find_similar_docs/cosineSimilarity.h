#pragma once
#include <vector>
#include <string>
#include <stdexcept>
#include <algorithm>
#include <map>
#include <cmath>

std::vector<double> get_column(const std::vector<std::vector<double>> &v, const int &col_idx);
double mean(const std::vector<double> &similarities);
double std_dev(const std::vector<double> &similarities, const double &mu);
double z_score(const double &x, const double &mu, const double &sigma);
double cosine_similarity(const std::vector<double> &A, const std::vector<double> &B);
std::pair<std::string, double> find_max(std::map<std::string, double> &similarities);
std::map<std::string, double> cosine_similarity_corpus(const std::vector<std::vector<double>> &A);