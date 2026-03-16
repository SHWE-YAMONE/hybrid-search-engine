#ifndef SEARCH_ENGINE_H
#define SEARCH_ENGINE_H

#include <vector>
#include <string>
#include <unordered_map>
#include <cmath>
#include <algorithm>
#include <shared_mutex>

struct Posting {
    int doc_id;
    int freq;
};

class SearchEngine {
private:
    std::unordered_map<std::string, std::vector<Posting>> index;
    std::unordered_map<int, double> doc_norms;
    int total_docs = 0;
    mutable std::shared_mutex mutex_; // Thread-safety for API concurrency

public:
    void index_document(int doc_id, const std::vector<std::string>& tokens);
    std::vector<std::pair<int, double>> search(const std::vector<std::string>& query_tokens);
};

#endif