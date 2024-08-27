cmake_minimum_required(VERSION 3.12)
project(html_generator)

# Set C++ standard to C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Locate pybind11
find_package(pybind11 REQUIRED)

# Add the module
pybind11_add_module(html_generator html_generator.cpp)
