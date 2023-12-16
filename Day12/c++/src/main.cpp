#include <string>
#include <iostream>
#include <fstream>
#include <thread>
#include <algorithm>
#include <cstdint>
#include <string_view>
#include <cassert>
#include <iterator>
#include <ranges>
#include <sstream>
#include <utility>
#include <vector>
#include <thread>
#include <mutex>
#include <optional>
#include <limits>
#include <unordered_map>

constexpr static bool IS_FIRST_PART{false};
constexpr static bool IS_MULTITHREADED{false};
constexpr static bool USE_IDENTITY_TRANSFORM{false}; // DO NOT USE.
constexpr static std::size_t NUMBER_OF_THREADS{12};

std::string getFileContent(const std::string_view fileName) noexcept
{
    std::fstream fs{std::string{fileName}};
    
    assert(fs.is_open());

    return std::string{std::istreambuf_iterator<char>{fs}, std::istreambuf_iterator<char>{}};
}

bool canFitNHashes(const std::string_view line, const std::size_t currentIndex, const std::size_t n) noexcept
{
    assert(n > 0);

    std::size_t i{};
    while(i < line.size() && (line[currentIndex + i] == '?' || line[currentIndex + i] == '#') && i < n)
    {
        ++i;
    }

    if(i != n)
    {
        return false;
    }

    if(currentIndex + i == line.size())
    {
        return true;
    }

    if(line[currentIndex + i] == '#')
    {
        return false;
    }
    else
    {
        return true;
    }
}

std::pair<std::string, std::vector<std::size_t>> transformData(const std::string_view line, std::vector<std::size_t> numbers) noexcept
{
    if constexpr(USE_IDENTITY_TRANSFORM)
    {
        return std::pair<std::string, std::vector<std::size_t>>{line, numbers};
    }
    else
    {
        std::string buffer{
            std::string{line} + std::string("?")  + 
            std::string(line) + std::string("?")  + 
            std::string(line) + std::string("?")  + 
            std::string(line) + std::string("?")  + 
            std::string(line)
        };

        const std::vector tmp = numbers;
        for(std::size_t i = 0; i < 4; ++i)
        {
            for(std::size_t j = 0; j < tmp.size(); ++j)
            {
                numbers.push_back(tmp[j]);
            }
        }
        return std::pair{std::move(buffer), std::move(numbers)};
    }
}

std::size_t countNumberOfPreviousHashes(const std::string_view line, const ssize_t lastIndex) noexcept
{
    if(lastIndex < 0)
    {
        return 0;
    }

    std::size_t acc{};
    for(ssize_t i = lastIndex; i > -1; --i)
    {
        if(line[i] == '#')
        {
            ++acc;
            continue;
        }
        else if(line[i] == '.')
        {
            break;
        }

        assert(false);
    }

    return acc;
}

template<typename T>
T toNumber(const std::string_view v) noexcept
{
    T buffer{};

    std::stringstream{std::string{v}} >> buffer;

    return buffer;
}

template<typename T>
std::string_view toStringView(T&& t) { return {std::forward<decltype(t)>(t)}; }

struct Counter
{
    std::unordered_map<std::string, std::size_t> cache{};
    std::size_t cacheHit{};

    std::size_t count(const std::string_view line, const std::vector<std::size_t>& groups, const std::size_t currentIndex = 0) noexcept
    {
        // std::cout << line << ", " << currentIndex << std::endl;
        if(currentIndex >= line.size() && groups.size() == 0)
        {
            // std::cout << __FILE__ << ':' << __LINE__ << std::endl;
            return 1;
        }

        if(currentIndex >= line.size() && groups.size() > 0)
        {
            return 0;
        }

        if(line.size() > currentIndex && groups.size() == 0)
        {
            const auto iter = std::ranges::find(line.substr(currentIndex), '#');
            const auto isThereHashLeft = iter != std::ranges::end(line);
            if(isThereHashLeft)
            {
                return 0;
            }
            else
            {
                // std::cout << __FILE__ << ':' << __LINE__ << std::endl;
                return 1;
            }
        }

        if(line[currentIndex] == '.')
        {
            std::size_t i{currentIndex};
            while(i < line.size() && line[i] == '.')
            {
                ++i;
            }

            return count(line, groups, i);
        }
        else if(line[currentIndex] == '#')
        {
            if(groups.size() == 0)
            {
                return 0;
            }

            const auto currentGroupSize = groups[0];
            if(!canFitNHashes(line, currentIndex, currentGroupSize))
            {
                return 0;
            }

            std::string buffer{line};
            for(std::size_t i = currentIndex; i < currentGroupSize; ++i)
            {
                buffer[i] = '#';
            }
            buffer[currentIndex + currentGroupSize] = '.';

            std::vector<std::size_t> newGroups{std::next(std::ranges::begin(groups)), std::ranges::end(groups)};
            return count(buffer, std::move(newGroups), currentIndex + currentGroupSize);
        }
        else if(line[currentIndex] == '?')
        {
            std::string buffer{line};
            std::size_t returningSum{};

            buffer[currentIndex] = '.';
            const auto dotPart = count(buffer, groups, currentIndex);
            returningSum += dotPart;

            if(currentIndex == 0 || buffer[currentIndex - 1] == '.')
            {
                buffer[currentIndex] = '#';
                const auto hashPart = count(buffer, groups, currentIndex);
                returningSum += hashPart;
            }

            return returningSum;
        }

        return std::numeric_limits<std::size_t>::max();
    }
};

struct Counter2
{
    std::size_t count(const std::string_view line, const std::vector<std::size_t>& groups) noexcept
    {
        const auto delim = std::string{"#"};
        const auto lineStr = std::string{line};
        std::vector<std::size_t> newGroups = groups;
        const auto addBatch = [&]
        {
            for(const auto& s : groups)
            {
                newGroups.push_back(s);
            }
        };

        const std::size_t solution1 = c.count(lineStr, newGroups);
        addBatch();
        const std::size_t solution2 = c.count(lineStr + delim + lineStr, newGroups);
        addBatch();
        const std::size_t solution3 = c.count(lineStr + delim + lineStr + delim + lineStr, newGroups);
        addBatch();
        const std::size_t solution4 = c.count(lineStr + delim + lineStr + delim + lineStr + delim + lineStr, newGroups);
        addBatch();
        const std::size_t solution5 = c.count(lineStr + delim + lineStr + delim + lineStr + delim + lineStr + delim + lineStr, newGroups);

        std::size_t sum{};
        sum += solution1 * solution1 * solution1 * solution1 * solution1;
        sum += solution1 * solution1 * solution1 * solution2 * 4;
        sum += solution1 * solution1 * solution3 * 3;
        sum += solution1 * solution2 * solution2 * 3;
        sum += solution1 * solution4 * 2;
        sum += solution2 * solution3 * 2;
        sum += solution5;

        return sum;
    }

    Counter c{};
    std::unordered_map<std::string, std::size_t>& cache = c.cache;
    std::size_t& cacheHit = c.cacheHit;
};

int main(const int argc, const char* const argv[])
{
    if(argc != 2)
    {
        std::cerr << "Wrong usage.\n";
        return 1;
    }
    constexpr static auto toStringView = []<typename T>(T&& t) { return std::string_view{std::forward<decltype(t)>(t)}; };

    const std::string_view fileName{argv[1]};
    std::string text = getFileContent(fileName);

    namespace v = std::ranges::views;

    auto splitView = text 
        | v::split('\n')
        | v::transform(toStringView);

    std::vector<std::pair<std::string, std::vector<std::size_t>>> data{};

    for(const auto& s : splitView)
    {
        auto split = s
            | v::split(' ')
            | v::transform(toStringView);
        std::vector<std::string_view> temp{std::ranges::begin(split), std::ranges::end(split)};
        assert(temp.size() == 2);

        std::vector<std::size_t> numbers{};

        for(const auto& numStr : temp[1] | v::split(','))
        {
            numbers.push_back(toNumber<std::size_t>(std::string_view{numStr}));
        }

        data.emplace_back(temp[0], std::move(numbers));
    }

    // data = std::vector{
        // std::pair{std::string{"?###????????"}, std::vector<std::size_t>{3,2,1}}
    // };
 
    if(IS_MULTITHREADED)
    {
        std::vector<std::thread> threads;

        std::mutex m{};
        const auto acquireData = [&]() -> std::optional<std::pair<std::string, std::vector<std::size_t>>> 
        {
            std::unique_lock lock{m};
            if(!data.empty())
            {
                std::pair<std::string, std::vector<std::size_t>> value = std::move(data.front());
                data.erase(data.begin());
                return std::optional{std::move(value)};
            }
            return std::nullopt;
        };

        std::size_t sum{};
        std::size_t i{};
        for(std::size_t n = 0; n < NUMBER_OF_THREADS; ++n)
        {
            threads.emplace_back([&acquireData, &sum, &i, &m]
            {
                std::optional optData = acquireData();
                while(optData.has_value())
                {
                    const auto&[line, numbers] = *optData;
                    auto c{[&]
                        {
                            if constexpr(IS_FIRST_PART)
                            {
                                return Counter{};
                            }
                            else
                            {
                                return Counter2{};
                            }
                        }()
                    };
                    std::size_t k{};

                    {
                        k = ++i;
                        std::unique_lock lock{m};
                        std::cout << k << ": Working on: " << line << std::endl; 
                    }

                    const auto result = c.count(line, numbers);

                    {
                        std::unique_lock lock{m};
                        std::cout << k << ": " << line << ": " << result << ", cache size: " << c.cache.size() << ", cache hit: " << c.cacheHit << std::endl;
                        sum += result;
                    }
    
                    optData = acquireData();
                }
            });
        }

        for(auto&& t : threads)
        {
            t.join();
        }
    
        std::cout << "Solution: " << sum << std::endl;
    }
    else
    {
        std::size_t sum{};
        std::size_t i{};
        for(const auto&[line, numbers] : data)
        {
            auto c{[&]
                        {
                            if constexpr(IS_FIRST_PART)
                            {
                                return Counter{};
                            }
                            else
                            {
                                return Counter2{};
                            }
                        }()
                    };
            std::cout << ++i << ": Working on: " << line << std::endl; 
            const auto result = c.count(line, numbers);
            std::cout << i << ": " << line << ": " << result << ", cache size: " << c.cache.size() << ", cache hit: " << c.cacheHit << std::endl;
            sum += result;
        }

        std::cout << "Solution: " << sum << std::endl;
    }


    
}