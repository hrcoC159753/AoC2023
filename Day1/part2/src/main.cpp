#include "aoc/day1/day1.h"
#include "aoc/aoc.h"

#include <string>
#include <iostream>

int main()
{
    constexpr static auto RESOURCE_FILE_NAME = "input.txt";
    const std::filesystem::path filePath = aoc::getResourcePath() / RESOURCE_FILE_NAME;
    const std::string text = aoc::getFileContents(filePath).value();

    std::cout << "Result: " << aoc::day1::solvePart2(text) << std::endl;

    return 0;
}