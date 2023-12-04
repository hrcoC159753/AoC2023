#include "aoc/day4/day4.h"

#include <fstream>
#include <iterator>
#include <iostream>

int main()
{
    constexpr static auto FILE_NAME = "input_part1.txt";

    const std::string text = []{
        std::ifstream inputFile{FILE_NAME};
        if(!inputFile.is_open())
        {
            throw std::runtime_error("File could not be opened.");
        }
        return std::string{std::istreambuf_iterator<char>{inputFile}, std::istreambuf_iterator<char>{}};
    }();

    const auto solution = aoc::day4::part1::solve(text);

    std::cout << "Solution for \"" << FILE_NAME << "\" is: " << solution << '\n';

    return 0;
}