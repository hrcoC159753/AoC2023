cmake_minimum_required(VERSION 3.23)

find_package(GTest REQUIRED)

add_executable(test_exe)
target_sources(test_exe
    PRIVATE
        src/main.cpp
)

target_link_libraries(test_exe
    PRIVATE
        GTest::gtest
        GTest::gtest_main
        GTest::gmock
        day5
)

include(GoogleTest)
gtest_discover_tests(test_exe)