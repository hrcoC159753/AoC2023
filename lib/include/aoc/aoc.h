#pragma once

#include <filesystem>
#include <string>
#include <optional>

namespace aoc
{
    std::filesystem::path getResourcePath() noexcept; 
    std::optional<std::string> getFileContents(const std::filesystem::path& filePath) noexcept;
}