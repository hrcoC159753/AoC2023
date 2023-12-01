cmake_minimum_required(VERSION 3.23)

project(Day1_lib LANGUAGES CXX)

add_library(day1)
target_sources(day1
    PRIVATE
        src/day1.cpp
    PUBLIC
        FILE_SET HEADERS
        TYPE HEADERS
        BASE_DIRS
            include
        FILES
            include/aoc/day1/day1.h
)