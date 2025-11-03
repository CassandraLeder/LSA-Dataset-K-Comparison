#pragma once

#include <vector>
#include <cmath>

double mean(const std::vector<double> &similarities);
double std_dev(const std::vector<double> &similarities, const double &mu);
double z_score(const double &x, const double &mu, const double &sigma);
