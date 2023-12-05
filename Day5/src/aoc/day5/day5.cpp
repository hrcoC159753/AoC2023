#include "aoc/day5/day5.h"

#include "cpp_utils/cpp_utils.h"

#include <iostream>
#include <regex>
#include <ranges>
#include <string_view>
#include <utility>
#include <vector>
#include <cassert>
#include <ostream>
#include <tuple>
#include <numeric>
#include <algorithm>
#include <functional>
#include <numeric>

using cpp_utils::operator<<;


namespace 
{
using Mapping = aoc::day5::Mapping;
using MappingInfo = aoc::day5::MappingInfo;
using Seeds = aoc::day5::Seeds;
using Data = aoc::day5::Data;

namespace r = std::ranges;
namespace v = std::views;

constexpr static auto toStringView = [](auto&& v) noexcept
{
    return std::string_view(std::forward<decltype(v)>(v));
};

Mapping numberLineToMapping(const std::string_view numberLine) noexcept
{
    auto numbersView = numberLine
        | v::split(' ')
        | v::transform(toStringView)
        | v::transform(cpp_utils::toNumber<std::size_t>);

    const std::vector<std::size_t> numbers(
        r::begin(numbersView),
        r::end(numbersView)
    );
    assert(numbers.size() == 3);

    return Mapping{numbers[0], numbers[1], numbers[2]};
}

MappingInfo paragraphToMappingInfo(const std::string_view paragraph) noexcept
{
    auto paragraphLinesView = paragraph
        | v::split('\n')
        | v::transform(toStringView);

    const std::vector paragraphLines(
        r::begin(paragraphLinesView),
        r::end(paragraphLinesView)
    );
    assert(paragraphLines.size() > 1);

    const std::string firstLine{paragraphLines[0]};
    std::regex r{R"((\w+)-to-(\w+) map:)"};
    std::smatch matchResults;
    const auto didItMatch = std::regex_match(
        firstLine,
        matchResults,
        r
    );

    assert(didItMatch);
    assert(matchResults.size() == 3);

    const auto& source = matchResults[1].str();
    const auto& destination = matchResults[2].str();

    auto mappingsPerParagraph = paragraphLinesView
        | v::drop(1)
        | v::transform(toStringView)
        | v::transform(numberLineToMapping);

    return MappingInfo{
        source, 
        destination, 
        std::vector<Mapping>
        (
            r::begin(mappingsPerParagraph), 
            r::end(mappingsPerParagraph)
        )
    };
} 

Data parse(const std::string_view text) noexcept
{
    constexpr static std::string_view PARAGRAPH_DELIMETER{"\n\n"};
    
    auto paragraphsView = text 
        | v::split(PARAGRAPH_DELIMETER) 
        | v::transform(toStringView);
    
    const std::vector<std::string_view> paragraphs(
        r::begin(paragraphsView),
        r::end(paragraphsView)
    );
    assert(paragraphs.size() > 1);

    const auto& seedParagraph = paragraphs[0];
    auto seedParagraphSplitView = seedParagraph
        | v::split(':')
        | v::transform(toStringView)
        | v::transform(cpp_utils::trim);
    
    const std::vector<std::string_view> seedParagraphSplit
    (
        r::begin(seedParagraphSplitView),
        r::end(seedParagraphSplitView)
    );
    assert(seedParagraphSplit.size() == 2);
    assert(seedParagraphSplit[0] == std::string_view{"seeds"});

    const std::string_view& numberPart = seedParagraphSplit[1];
    auto seedNumberStringsView = numberPart
        | v::split(' ')
        | v::transform(toStringView)
        | v::transform(&cpp_utils::toNumber<std::size_t>);



    const std::vector<std::string_view> restParagraph(r::begin(paragraphs) + 1, r::end(paragraphs)); 
    auto mappingInfosPerParagraph = restParagraph
        | v::transform(paragraphToMappingInfo);
    
    std::vector<MappingInfo> mappingInfos(
        r::begin(mappingInfosPerParagraph),
        r::end(mappingInfosPerParagraph)
    );
    return Data
    {
        Seeds
        {
            std::vector<std::size_t>
            (
                r::begin(seedNumberStringsView),
                r::end(seedNumberStringsView)
            )
        },
        std::move(mappingInfos)
    };
}

}

namespace aoc::day5::part1
{

std::size_t solve(const std::string_view text) noexcept
{
    const auto&[seeds, mappingInfos] = parse(text);

    using cpp_utils::operator<<;

    const auto findMappingInfoForSource = [&mappingInfos](const std::string_view source) noexcept
    {
        return *std::ranges::find(mappingInfos, source, &MappingInfo::m_source);
    };

    const auto calculateMappingForMappingInfo = [](const std::size_t number, const MappingInfo& mappingInfo) noexcept
    {
        for(const Mapping& mapping : mappingInfo.m_mappings)
        {
            if(number >= mapping.m_sourceNumber && number <= mapping.m_sourceNumber + mapping.m_size - 1)
            {
                return mapping.m_destinationNumber + (number - mapping.m_sourceNumber);
            }
        }

        return number;
    };

    const auto finalFunction = [&](const std::size_t number)
    {
        auto mappingInfo = findMappingInfoForSource("seed");

        std::size_t numberCopy = number;
        while(mappingInfo.m_destination != "location")
        {
            numberCopy = calculateMappingForMappingInfo(numberCopy, mappingInfo);
            mappingInfo = findMappingInfoForSource(mappingInfo.m_destination);
        }

        numberCopy = calculateMappingForMappingInfo(numberCopy, mappingInfo);

        return numberCopy;
    };

    auto locationView = seeds.m_seedNumbers
        | v::transform(finalFunction);

    return std::ranges::min(locationView);
}

}

namespace aoc::day5::part2
{

std::size_t solve(const std::string_view text) noexcept
{

    const auto&[seeds, mappingInfos] = parse(text);

    using cpp_utils::operator<<;

    const auto findMappingInfoForSource = [&mappingInfos](const std::string_view source) noexcept
    {
        return *std::ranges::find(mappingInfos, source, &MappingInfo::m_source);
    };

    const auto calculateMappingForMappingInfo = [](const std::size_t number, const MappingInfo& mappingInfo) noexcept
    {
        for(const Mapping& mapping : mappingInfo.m_mappings)
        {
            if(number >= mapping.m_sourceNumber && number <= mapping.m_sourceNumber + mapping.m_size - 1)
            {
                return mapping.m_destinationNumber + (number - mapping.m_sourceNumber);
            }
        }

        return number;
    };

    const auto finalFunction = [&](const std::size_t number)
    {
        auto mappingInfo = findMappingInfoForSource("seed");

        std::size_t numberCopy = number;
        while(mappingInfo.m_destination != "location")
        {
            numberCopy = calculateMappingForMappingInfo(numberCopy, mappingInfo);
            mappingInfo = findMappingInfoForSource(mappingInfo.m_destination);
        }

        numberCopy = calculateMappingForMappingInfo(numberCopy, mappingInfo);

        return numberCopy;
    };

    const auto toMinimalValueOfRange = [&](const std::tuple<std::size_t, std::size_t>& range) noexcept
    {
        const auto&[rangeBegin, rangeSize] = range;
        std::size_t minNumber = std::numeric_limits<std::size_t>::max(); 
        for(std::size_t num = rangeBegin; num < rangeBegin + rangeSize; ++num)
        {
            const auto resultNum = finalFunction(num);
            if(resultNum < minNumber)
            {
                minNumber = resultNum;
            }

            if(num % 100'000 == 0)
            {
                std::cout << std::string_view{"num: "} << num << std::endl;
            }
        }

        return minNumber;
    };

    std::vector<std::tuple<std::size_t, std::size_t>> ranges{};
    assert(seeds.m_seedNumbers.size() % 2 == 0);
    for(std::size_t i = 0; i < seeds.m_seedNumbers.size(); i += 2)
    {
        const auto& rangeBegin = seeds.m_seedNumbers[i];
        const auto& rangeSize = seeds.m_seedNumbers[i + 1];

        ranges.emplace_back(std::size_t{rangeBegin}, std::size_t{rangeSize});
    }

    auto locationView = ranges
        | v::transform(toMinimalValueOfRange);

    return std::ranges::min(locationView);
}

std::size_t solve2(const std::string_view text) noexcept
{
    const auto&[seeds, mappingInfos] = parse(text);

    constexpr static auto calculateMappingForMappingInfo = [](const std::size_t number, const MappingInfo& mappingInfo) noexcept
    {
        for(const Mapping& mapping : mappingInfo.m_mappings)
        {
            if(number >= mapping.m_sourceNumber && number <= mapping.m_sourceNumber + mapping.m_size - 1)
            {
                return mapping.m_destinationNumber + (number - mapping.m_sourceNumber);
            }
        }

        return number;
    };

    const auto findMappingInfoForSource = [&mappingInfos](const std::string_view source) noexcept -> const MappingInfo&
    {
        return *std::ranges::find(mappingInfos, source, &MappingInfo::m_source);
    };

    const MappingInfo seedToLocationMappingInfo = [&]
    {
        MappingInfo current = findMappingInfoForSource("seed");
        
        while(current.m_destination != "location")
        {
            const MappingInfo& newMappingInfo = findMappingInfoForSource(current.m_destination);

            current = compose(current, newMappingInfo);
        }

        return current;
    }();

    using RangeType = std::tuple<std::size_t, std::size_t>;

    const auto rangeToMinimumElement = [&](const RangeType& range) noexcept
    {
        const auto& [rangeBegin, rangeSize] = range;
        std::size_t minElement = std::numeric_limits<std::size_t>::max();
        for(std::size_t n = rangeBegin; n < rangeBegin + rangeSize; ++n)
        {
            const std::size_t locationNumber = calculateMappingForMappingInfo(n, seedToLocationMappingInfo);
            if(locationNumber < minElement)
            {
                minElement = locationNumber;
            }
        }
        return minElement;
    };

    std::vector<RangeType> ranges{};
    for(std::size_t i = 0; i < seeds.m_seedNumbers.size(); i += 2)
    {
        const std::size_t& rangeBegin = seeds.m_seedNumbers[i];
        const std::size_t& rangeSize = seeds.m_seedNumbers[i + 1];
        ranges.emplace_back(rangeBegin, rangeSize);
    }

    auto minimumLocationsView = ranges
        | v::transform(rangeToMinimumElement);

    return std::ranges::min(minimumLocationsView);
}

}