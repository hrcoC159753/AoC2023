#include "aoc/day5/day5.h"

#include <fstream>
#include <iostream>
#include <string>
#include <iterator>

std::string getFileContents(std::string_view fileName)
{
    std::ifstream file{std::string{fileName}};
    if(!file.is_open())
    {
        throw std::runtime_error("Can not open the file.");
    }

    return std::string{std::istreambuf_iterator<char>{file}, std::istreambuf_iterator<char>{}};
}


void example(std::string_view fileName) noexcept
{
    const auto text = getFileContents(fileName);

    const auto solution = aoc::day5::part1::solve(text);

    std::cout << "Solution for '" << fileName << "' is " << solution << std::endl;
}

int main()
{
    constexpr static std::string_view INITIAL_FILE_NAME = "initial_input1.txt";
    constexpr static std::string_view FILE_NAME = "input1.txt";

    example(INITIAL_FILE_NAME);
    example(FILE_NAME);
}