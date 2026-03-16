#include <pybind11/pybind11.h>
#include <pybind11/stl.h>  // Crucial: Converts std::vector and std::pair to Python lists/tuples
#include "search_engine.h"

namespace py = pybind11;

// The name 'fast_search' here MUST match the name in your setup.py 
// and the name of the final shared library file.
PYBIND11_MODULE(fast_search, m) {
    m.doc() = "Hybrid C++ Search Engine Core"; // Optional module docstring

    // Expose the SearchEngine class
    py::class_<SearchEngine>(m, "SearchEngine")
        .def(py::init<>()) // Expose the default constructor
        
        // Expose the indexing method
        .def("index_document", &SearchEngine::index_document, 
             "Indexes a document",
             py::arg("doc_id"), py::arg("tokens"))
             
        // Expose the search method
        // Note: This returns a vector of pairs, which pybind11/stl.h 
        // will automatically convert to a Python list of tuples: [(id, score), ...]
        .def("search", &SearchEngine::search, 
             "Performs a ranked search and returns doc IDs with scores",
             py::arg("query_tokens"));
}