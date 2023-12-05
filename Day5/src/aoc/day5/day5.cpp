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

namespace 
{
using cpp_utils::operator<<;
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
    using std::string_view_literals::operator""sv;
    const auto&[seeds, mappingInfos] = parse(text);

    const auto getMappingInfoFor = [&](const std::string_view source) -> const MappingInfo&
    {
        const auto foundMappingInfo = std::ranges::find(mappingInfos, source, &MappingInfo::m_source);
        assert(foundMappingInfo != std::ranges::end(mappingInfos));

        return *foundMappingInfo;
        
    };

    MappingInfo mappingInfo = getMappingInfoFor("seed");
    while(mappingInfo.m_destination != "location")
    {
        std::vector<Mapping> newMappings{};

        const MappingInfo& destinationInfo = getMappingInfoFor(mappingInfo.m_destination);
        for(const Mapping& infoMapping : mappingInfo.m_mappings)
        {
    
            std::vector<Mapping> restMappings{};
            for(const Mapping& destinationInfoMapping : destinationInfo.m_mappings)
            {
                const auto&[optNewMapping, optOldMapping] = combineMappings(infoMapping, destinationInfoMapping);

                if(optNewMapping.has_value())
                {
                    newMappings.push_back(*optNewMapping);
                }

                for(const Mapping& restMapping : restMappings)
                {
                    const auto&[optNewRestMapping, optOldRestMapping] = combineMappings(infoMapping, destinationInfoMapping);
                    if(optNewRestMapping.has_value())
                    {
                        newMappings.push_back(*optNewRestMapping);
                    }

                    if(optOldRestMapping.has_value())
                    {
                        restMappings.push_back(*optOldRestMapping);
                    }
                }

                if(optOldMapping.has_value())
                {
                    restMappings.push_back(*optNewMapping);
                }
            }
        }

        mappingInfo = MappingInfo{
            "seed",
            destinationInfo.m_destination,
            std::move(newMappings)
        };
    }

    assert(mappingInfo.m_destination == "location");

    auto locationsView = seeds.m_seedNumbers
        | v::transform(
            [&](const std::size_t seed)
            {
                const auto foundMappingIter = std::ranges::find_if(
                    mappingInfo.m_mappings, 
                    [&](const Mapping& m) { return m.m_sourceNumber <= seed and m.m_sourceNumber + m.m_size - 1 >= seed; }
                );

                if(foundMappingIter == std::ranges::end(mappingInfo.m_mappings))
                {
                    return seed;
                }

                const auto& foundMapping = *foundMappingIter;

                return foundMapping.m_destinationNumber + seed - foundMapping.m_sourceNumber;
            }
        );

    return std::ranges::min(locationsView);
}

}

namespace aoc::day5::part2
{

std::size_t solve(const std::string_view text) noexcept
{
    return 2;
}

}