#include "mmReader.h"

// default constructor definition (empty) in header file

mmReader::mmReader(std::string file_path) {
    // check that file exists (the slow but easy to read method)
    std::ifstream file(file_path);
    if (!file.good()) {
        throw std::invalid_argument(std::string("File ") + file_path + std::string(" could not be read."));
    }
    else { // file is good and code should function accordingly
        this->file_path = file_path;
    }
}

void mmReader::setFilePath(std::string file_path) {
    this->file_path = file_path;
}

bool mmReader::filePathExists() {
    return(this->file_path != "");
}

/*
    Parse the contents of a market matrix formatted file and return a 2d vector of double
*/
std::vector<std::vector<double>> mmReader::readMM() {
    if (!filePathExists()) {
        throw std::invalid_argument("File path must be set first.");
    }

    std::ifstream file(this->file_path); // begin reading file...
    // skip header
    std::string line = "";
    std::getline(file, line);

    std::getline(file, line);
    std::stringstream line_stream(line);

    // initialize 2d vector using dimensions from file and fill with 0
    std::size_t n_col, n_row;
    line_stream >> n_col >> n_row;
    std::vector<std::vector<double>> v(n_row, std::vector<double>(n_col));

    // now get every line that has nonzero values
    int col = 0, row = 0, val = 0;
    while(std::getline(file, line)) {
        std::stringstream line_stream(line);
        line_stream >> col >> row >> val;
        v[row - 1][col - 1] = val; // market matrix are indexed starting at 1..
    }

    return(v);
}