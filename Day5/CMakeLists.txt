cmake_minimum_required(VERSION 3.23)

project(
        day5 
        LANGUAGES CXX
)
enable_testing()

add_library(day5)
target_sources(day5
        PRIVATE
                src/aoc/day5/day5.cpp
        PUBLIC
                FILE_SET HEADERS
                TYPE HEADERS
                BASE_DIRS
                        include
                FILES
                        include/aoc/day5/day5.h
)

find_package(cpp_utils REQUIRED)
target_link_libraries(day5
        PUBLIC
                cpp_utils::cpp_utils
)

add_subdirectory(part1)
# add_subdirectory(part2)

add_subdirectory(test)

install(TARGETS day5
        RUNTIME DESTINATION bin
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        )
