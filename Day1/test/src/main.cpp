#include <gtest/gtest.h>

#include <cstdint>
#include <iostream>

#include "aoc/day1/day1.h"
#include "aoc/aoc.h"

TEST(Day1_Part1, Initial) 
{
    constexpr static std::size_t EXPECTED_SOLUTION = 142;
    constexpr static const char* const INPUT_FILE_NAME = "part1_init.txt";

    const auto filePath = aoc::getResourcePath() / INPUT_FILE_NAME;
    const std::string text = aoc::getFileContents(filePath).value();

    const auto solution = aoc::day1::solvePart1(text);

    EXPECT_EQ(solution, EXPECTED_SOLUTION);
}

TEST(Day1_Part2, Initial) 
{
    constexpr static std::size_t EXPECTED_SOLUTION = 281;
    constexpr static const char* const INPUT_FILE_NAME = "part2_init.txt";

    const auto filePath = aoc::getResourcePath() / INPUT_FILE_NAME;
    const std::string text = aoc::getFileContents(filePath).value();

    const auto solution = aoc::day1::solvePart2(text);
    
    EXPECT_EQ(solution, EXPECTED_SOLUTION);
}