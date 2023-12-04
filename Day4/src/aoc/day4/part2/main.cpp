#include "aoc/day4/day4.h"

#include <fstream>
#include <iterator>
#include <iostream>

std::string getText(const std::string_view fileName)
{
    return [fileName]{
        std::ifstream inputFile{std::string{fileName}};
        if(!inputFile.is_open())
        {
            throw std::runtime_error("File could not be opened.");
        }
        return std::string{std::istreambuf_iterator<char>{inputFile}, std::istreambuf_iterator<char>{}};
    }();
}

void example(const std::string_view fileName) noexcept
{
    const auto text = getText(fileName);
    const auto solution = aoc::day4::part2::solve(text);

    std::cout << "Solution for \"" << fileName << "\" is: " << solution << '\n';
}

int main()
{
    constexpr static auto INITIAL_FILE_NAME = "initial_input_part2.txt";
    constexpr static auto FILE_NAME = "input_part2.txt";

    example(INITIAL_FILE_NAME);
    example(FILE_NAME);

    return 0;
}