import sys
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

# This class delays the pybind11 import until the build actually starts
class build_ext_subclass(build_ext):
    def build_extensions(self):
        import pybind11
        # Add the include directory for the compiler
        for ext in self.extensions:
            ext.include_dirs.append(pybind11.get_include())
        super().build_extensions()

ext_modules = [
    Pybind11Extension(
        "fast_search",
        ["engine/bindings.cpp", "engine/src/search_engine.cpp"],
        include_dirs=["engine/include"],
        language='c++',
        cxx_std=20,
    ),
]

setup(
    name="fast_search",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext_subclass},
)