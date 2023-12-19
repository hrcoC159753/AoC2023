cmake_minimum_required(VERSION 3.23)

project(Day19
    LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 23)

add_executable(main)
target_sources(main
    PRIVATE
        src/main.cpp
)

add_executable(main2)
target_sources(main2
    PRIVATE
        src/main2.cpp
)