cmake_minimum_required(VERSION 3.23)

project(Day1_part1 LANGUAGES CXX)

set(EXECUTABLE_NAME day1_part1)

add_executable(${EXECUTABLE_NAME})
target_sources(${EXECUTABLE_NAME}
    PRIVATE
        src/main.cpp
)
target_link_libraries(${EXECUTABLE_NAME}
    PRIVATE
        day1
        aoc
)

add_custom_command(
    TARGET ${EXECUTABLE_NAME}
    POST_BUILD
    COMMAND
        ${CMAKE_COMMAND} -E copy_directory ${CMAKE_CURRENT_SOURCE_DIR}/res ${CMAKE_CURRENT_BINARY_DIR}/res
)