#include "stat.h"

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