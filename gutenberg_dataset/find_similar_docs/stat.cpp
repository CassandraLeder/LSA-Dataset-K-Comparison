#include "stat.h"

// get population mean and standard deviation for the cosine similarity matrix
Statistics::Statistics(const std::vector<std::vector<float>> &similarities) {
    mu = pop_mean(similarities);
    sigma = pop_std_dev(similarities, mu);
}

// compute the arithmetic of mean but only return sum and count
std::pair<float, int> Statistics::mean(const std::vector<float> &sim_vec) {
    auto sum = 0.0;
    auto count = 0;

    for (auto& similarity : sim_vec) {
        if (similarity != 1) {
            ++count;
            sum += similarity;
        }
    }

    std::pair<float,int> mean_pair = {sum, count};

    return (mean_pair);
}

// return population mean, mu
float Statistics::pop_mean(const std::vector<std::vector<float>> &similarities) {
    auto sum = 0.0;
    auto count = 0;

    for (auto& row : similarities) {   
        auto mean_pair = mean(row);
        sum += mean_pair.first;
        count += mean_pair.second;
    }

    return(sum / count);
}

// return population standard deviation, sigma
// sigma = each element - population mean squared
double Statistics::pop_std_dev(const std::vector<std::vector<float>> &similarities, const float &mu) {
    auto sum = 0.0;
    
    for (auto& row : similarities) {
        for (auto& similarity : row) {
            if (similarity != 1) {
                sum += (similarity - mu) * (similarity - mu);
            }
        }
    }

    return(sqrt(sum / similarities.size()));
}

// z-score for each individual cosine similarity = score - population mean / population standard deviation
double Statistics::pop_z_score(const float &x) {
    return ((x - mu) / sigma);
}

double Statistics::z_score(const float &x, const float &x_bar, const double &s) {
    return((x - x_bar) / s);
}

// get a document's mean cosine similarity for all documents in corpus
std::vector<float> Statistics::doc_mean(const std::vector<std::vector<float>> &similarities) {
    std::vector<float> means;
    
    for (auto i = 0; i < similarities[0].size(); ++i) {
        auto doc_i = get_column(similarities, i);
        auto sum = 0.0;
        auto count = 0;
        auto mean_pair = mean(doc_i);
        means.push_back(mean_pair.first / mean_pair.second);
    }

    return(means);
}

std::vector<double> Statistics::doc_std_dev(const std::vector<std::vector<float>> &similarities, const std::vector<float> &doc_means) {
    std::vector<double> std_devs;

    for (auto i = 0; i < similarities[0].size(); ++i) {
        auto sum = 0.0;
        auto doc_i = get_column(similarities, i);

        for (auto& similarity : doc_i) {
            if (similarity != 1) {
                sum += (similarity - doc_means[i]) * (similarity - doc_means[i]);
            }
        }
        std_devs.push_back(sqrt(sum / doc_i.size()));
    }

    return(std_devs);
}

std::vector<double> Statistics::doc_z_score(const std::vector<std::vector<float>> &similarities, const std::vector<float> &doc_means, const std::vector<double> &doc_std_dev) {
    std::vector<double> z_scores;

    for (auto i = 0; i < similarities[0].size(); ++i) {
        auto doc_i = get_column(similarities, i);
        for (auto& similarity : doc_i) {
            if (similarity != 1) {
                z_scores.push_back(z_score(similarity, doc_means[i], doc_std_dev[i]));
            }
        }
    }
    return(z_scores);
}
