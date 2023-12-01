cmake_minimum_required(VERSION 3.23)

project(Day1_Tests LANGUAGES CXX)

set(EXECUTABLE_NAME Day1_Tests)
add_executable(${EXECUTABLE_NAME})
target_sources(${EXECUTABLE_NAME}
    PRIVATE
        src/main.cpp
)

add_custom_command(
    TARGET ${EXECUTABLE_NAME}
    POST_BUILD
    COMMAND
        ${CMAKE_COMMAND} -E copy_directory ${CMAKE_CURRENT_SOURCE_DIR}/res ${CMAKE_CURRENT_BINARY_DIR}/res
)

target_link_libraries(${EXECUTABLE_NAME}
    PRIVATE
        aoc
        day1
        GTest::gtest
        GTest::gtest_main
        GTest::gmock
)

include(GoogleTest)
gtest_discover_tests(${EXECUTABLE_NAME})