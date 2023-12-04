cmake_minimum_required(VERSION 3.23)

project(Day4 LANGUAGES CXX)
enable_testing()

set(CMAKE_CXX_STANDARD 23)

add_library(day4)
target_sources(day4
    PRIVATE
        src/aoc/day4/day4.cpp
    PUBLIC
        FILE_SET HEADERS
        TYPE HEADERS
        BASE_DIRS
            include
        FILES
            include/aoc/day4/day4.h
)

add_executable(day4_part1)
target_sources(day4_part1
    PRIVATE
        src/aoc/day4/part1/main.cpp
)
target_link_libraries(day4_part1
    PRIVATE
        day4
)
add_custom_command(
    TARGET day4_part1
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/res/input_part1.txt ${CMAKE_CURRENT_BINARY_DIR}/input_part1.txt
)
add_custom_command(
    TARGET day4_part1
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/res/initial_input_part1.txt ${CMAKE_CURRENT_BINARY_DIR}/initial_input_part1.txt
)

add_executable(day4_part2)
target_sources(day4_part2
    PRIVATE
        src/aoc/day4/part2/main.cpp
)
target_link_libraries(day4_part2
    PRIVATE
        day4
)
add_custom_command(
    TARGET day4_part2
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/res/input_part2.txt ${CMAKE_CURRENT_BINARY_DIR}/input_part2.txt
)
add_custom_command(
    TARGET day4_part2
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/res/initial_input_part2.txt ${CMAKE_CURRENT_BINARY_DIR}/initial_input_part2.txt
)