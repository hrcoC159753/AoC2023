#include "aoc/aoc.h"
#include "aoc/res.h"

#include <fstream>
#include <string>
#include <streambuf>
#include <limits.h>
#include <unistd.h>

namespace
{

std::filesystem::path getCurrentExecutablePath() noexcept
{
    char pathString[PATH_MAX];
    ssize_t count = readlink("/proc/self/exe", pathString, sizeof(pathString));
    return std::filesystem::path(pathString).parent_path();
}

}

namespace aoc
{
    std::filesystem::path getResourcePath() noexcept
    {
        return getCurrentExecutablePath() / aoc::REALTIVE_RESOURCE_DIRECTORY;
    }

    std::optional<std::string> getFileContents(const std::filesystem::path& filePath) noexcept
    {
        std::ifstream fs{filePath};
        if(!fs.is_open())
        {
            return std::nullopt;
        }

        using BufferIterator = std::istreambuf_iterator<char>;
        std::string buffer{BufferIterator{fs}, BufferIterator{}};

        return std::optional{buffer}; 
    }
}