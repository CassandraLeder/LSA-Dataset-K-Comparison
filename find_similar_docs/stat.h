#pragma once

#include <vector>
#include <cmath>

#include "cosineSimilarity.h"
#include "util.h"
class Statistics {
    private:
        float mu;
        double sigma;
        
        std::pair<float,int> mean(const std::vector<float> &sim_vec);
        double z_score(const float &x, const float &x_bar, const double &s);

        bool is_valid(float sim);
    public:
        Statistics(const std::vector<std::vector<float>> &similarities);
        
        float pop_mean(const std::vector<std::vector<float>> &similarities);
        std::vector<float> doc_mean(const std::vector<std::vector<float>> &similarities);
        
        double pop_std_dev(const std::vector<std::vector<float>> &similarities, const float &mu);
        std::vector<double> doc_std_dev(const std::vector<std::vector<float>> &similarities, const std::vector<float> &doc_means);
        
        std::vector<double> pop_z_score(const std::vector<std::vector<float>> &similarities); // uses class mu and sigma in calculation
        std::vector<double> doc_z_score(const std::vector<std::vector<float>> &similarities, const std::vector<float> &doc_means, const std::vector<double> &doc_std_dev);


        float get_mu() {return mu;}
        double get_sigma() {return sigma;}
};