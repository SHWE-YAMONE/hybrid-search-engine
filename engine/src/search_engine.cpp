#include "search_engine.h"

#include <mutex>

void SearchEngine::index_document(int doc_id, const std::vector<std::string>& tokens) {
    std::unique_lock lock(mutex_);
    total_docs++;
    std::unordered_map<std::string, int> counts;
    for (const auto& t : tokens) counts[t]++;

    double sum_sq = 0;
    for (auto const& [term, freq] : counts) {
        index[term].push_back({doc_id, freq});
        sum_sq += std::pow(freq, 2);
    }
    doc_norms[doc_id] = std::sqrt(sum_sq);
}

std::vector<std::pair<int, double>> SearchEngine::search(const std::vector<std::string>& query_tokens) {
    std::shared_lock lock(mutex_); // Read lock 
    std::unordered_map<int, double> scores;
    
    for (const auto& term : query_tokens) {
        if (index.count(term)) {
            // double idf = std::log((double)total_docs / (index.at(term).size()));

            double idf = std::log((double)total_docs / (index.at(term).size())) + 1.0;
            for (const auto& p : index.at(term)) {
                scores[p.doc_id] += (p.freq * idf) * (1.0 * idf);
            }
        }
    }

    std::vector<std::pair<int, double>> results;
    for (auto& [doc_id, score] : scores) {
        results.push_back({doc_id, score / (doc_norms[doc_id] + 1e-9)});
    }

    std::sort(results.begin(), results.end(), [](auto& a, auto& b){ return a.second > b.second; });
    return results;
}