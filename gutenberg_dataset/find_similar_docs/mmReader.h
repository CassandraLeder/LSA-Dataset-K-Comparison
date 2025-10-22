#pragma once

#include <stdexcept>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

class mmReader {
    private:
        std::string file_path;
    public:
        mmReader(){};
        mmReader(std::string file_path);
        void setFilePath(std::string file_path);
        bool filePathExists();
        std::vector<std::vector<double>> readMM();
};