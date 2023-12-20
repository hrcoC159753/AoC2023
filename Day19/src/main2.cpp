#include <iostream>
#include <cstdint>
#include <type_traits>
#include <vector>
#include <fstream>
#include <iterator>
#include <utility>
#include <string>
#include <string_view>
#include <optional>
#include <ranges>
#include <algorithm>
#include <numeric>
#include <cassert>
#include <functional>
#include <sstream>
#include <array>

std::string getStreamContents(std::istream& stream) noexcept
{
    return std::string{std::istreambuf_iterator<char>{stream}, std::istreambuf_iterator<char>{}};
}

std::string getFileContents(const std::string_view fileName) noexcept
{
    std::fstream fs{std::string{fileName}};

    assert(fs.is_open());

    return getStreamContents(fs);
}

std::tuple<std::string_view, std::string_view> parseText(const std::string_view text) noexcept
{
    namespace v = std::ranges::views;
    namespace r = std::ranges;

    auto paragraphView = text 
        | v::split(std::string_view{"\n\n"})
        | v::transform([]<typename T>(T&& v) { return std::string_view{std::forward<T>(v)}; });

    const std::vector<std::string_view> paragraphs{
        r::begin(paragraphView),
        r::end(paragraphView)
    };

    assert(paragraphs.size() == 2);

    return std::make_tuple(paragraphs[0], paragraphs[1]);
}

struct Part
{
    struct Params
    {
        std::size_t x;
        std::size_t m;
        std::size_t a;
        std::size_t s;
    };  

    Part(Params params) noexcept
        : m_map{}
    {
        m_map['x'] = params.x;
        m_map['m'] = params.m;
        m_map['a'] = params.a;
        m_map['s'] = params.s;
    }

    auto operator[](const char id) const noexcept
    {
        return m_map.at(id);
    }

private:
    std::unordered_map<char, std::size_t> m_map;
};

struct Mapping
{
    Mapping(const char c, std::function<std::optional<std::string>(std::size_t)> map) noexcept
        : 
            m_c{c},
            m_map{map}
    {
        
    }

    Mapping(std::function<std::optional<std::string>(std::size_t)> map) noexcept
        : 
            m_c{std::nullopt},
            m_map{map}
    {
        
    }

    std::optional<std::string> operator()(const std::size_t n) const noexcept
    {
        return m_map(n);
    }
    
    std::optional<char> m_c;
    std::function<std::optional<std::string>(std::size_t)> m_map;
};


struct Rule
{
    constexpr Rule(const std::string id, std::vector<Mapping> mappings) noexcept
        :
            m_id{id},
            m_mappings{std::move(mappings)}
    {

    }

    std::string operator()(const Part& part) const noexcept
    {
        for(const Mapping& map : m_mappings)
        {
            if(!map.m_c.has_value())
            {
                return *map(std::size_t{0});
            }

            if(const std::optional<std::string> optResult = map(part[*map.m_c]); optResult != std::nullopt)
            {
                return *optResult;
            }
        }

        std::unreachable();
    }

    std::string m_id;
    std::vector<Mapping> m_mappings;
};

struct Range
{
    std::size_t m_begin;
    std::size_t m_end; // exlusive
};

constexpr Range intersect(const Range& r1, const Range& r2) noexcept
{
    if(r1.m_end <= r2.m_begin || r1.m_begin >= r2.m_end)
    {
        return Range{r1.m_begin, r1.m_begin + 1};
    }

    if(r1.m_begin <= r2.m_begin && r1.m_end >= r2.m_end)
    {
        return r2;
    }
    else if(r1.m_begin >= r2.m_begin && r1.m_end <= r2.m_end)
    {
        return r1;
    }
    else if(r1.m_begin < r2.m_begin && r1.m_end > r2.m_begin)
    {
        return Range{r2.m_begin, r1.m_end};
    }
    else if(r1.m_begin > r2.m_begin && r1.m_end > r2.m_end)
    {
        return Range{r1.m_begin, r2.m_end};
    }
    else
    {
#ifndef NDEBUG
        std::unreachable();
#else
        assert(false);
#endif
    }
}

constexpr Range difference(const Range& r1, const Range& r2) noexcept
{
    // No crossing.
    if(r1.m_begin >= r2.m_end || r1.m_end <= r2.m_begin)
    {
        return r1;
    }

    // Whole r2 in r1.
    if(r1.m_begin < r2.m_begin && r1.m_end > r2.m_end)
    {
#ifndef NDEBUG
        std::unreachable();
#else
        assert(false);
#endif
    }
    // Whole r1 in r2.
    else if(r1.m_begin >= r2.m_begin && r1.m_end <= r2.m_end)
    {
        return Range{0, 0};
    }
    // r1 begin in r2.
    else if(r1.m_begin >= r2.m_begin && r1.m_end >= r2.m_end)
    {
        return Range{r2.m_end, r1.m_end};
    }
    // r1 end in r2
    else if(r1.m_begin <= r2.m_begin && r1.m_end >= r2.m_begin && r1.m_end <= r2.m_end)
    {
        return Range{r1.m_begin, r2.m_begin};
    }
    else
    {
#ifndef NDEBUG
        assert(false);
#else
        std::unreachable();
#endif
    }
}

constexpr std::vector<Range> unionOp(const Range& r1, const Range& r2) noexcept
{
    // No crossing.
    if(r1.m_begin >= r2.m_end || r1.m_end <= r2.m_begin)
    {
        return std::vector{r1, r2};
    }

    // Whole r2 in r1.
    if(r1.m_begin < r2.m_begin && r1.m_end > r2.m_end)
    {
        return {r1};
    }
    // Whole r1 in r2.
    else if(r1.m_begin >= r2.m_begin && r1.m_end <= r2.m_end)
    {
        return {r2};
    }
    // r1 begin in r2.
    else if(r1.m_begin >= r2.m_begin && r1.m_end >= r2.m_end)
    {
        return {Range{r2.m_begin, r1.m_end}};
    }
    // r1 end in r2
    else if(r1.m_begin <= r2.m_begin && r1.m_end >= r2.m_begin && r1.m_end <= r2.m_end)
    {
        return {Range{r1.m_begin, r2.m_end}};
    }
    else
    {
#ifndef NDEBUG
        assert(false);
#else
        std::unreachable();
#endif
    }


}

struct PartRange
{
    Range m_xRange;
    Range m_mRange;
    Range m_aRange;
    Range m_sRange;
};

struct Rule2
{
    std::string m_id;
    std::vector<std::tuple<char, Range, std::string>> m_mappings;
    std::string m_default;

    std::vector<std::pair<PartRange, std::string>> operator()(const PartRange& partRange) const noexcept
    {
        constexpr static auto isPartRangeEmpty = [](const PartRange& partRange)
        {
            return  partRange.m_xRange.m_begin == partRange.m_xRange.m_end || 
                    partRange.m_mRange.m_begin == partRange.m_mRange.m_end || 
                    partRange.m_aRange.m_begin == partRange.m_aRange.m_end || 
                    partRange.m_sRange.m_begin == partRange.m_sRange.m_end;
        };
        constexpr static std::array mappings = 
        {
            std::pair{'x', &PartRange::m_xRange},
            std::pair{'m', &PartRange::m_mRange},
            std::pair{'a', &PartRange::m_aRange},
            std::pair{'s', &PartRange::m_sRange}
        };


        std::vector<std::pair<PartRange, std::string>> ret{};
        
        PartRange partRangeCopy = partRange;
        for(const auto[c, range, id] : m_mappings)
        {
            const auto foundMappingIter = std::ranges::find(mappings, c, &std::pair<char, Range PartRange::*>::first);
            assert(foundMappingIter != std::ranges::end(mappings));

            const auto& foundMapping = foundMappingIter->second;

            auto copy = partRangeCopy;
            copy.*foundMapping = intersect(partRangeCopy.*foundMapping, range);

            if(not isPartRangeEmpty(copy))
            {
                ret.emplace_back(copy, id);
            }

            partRangeCopy.*foundMapping = difference(partRangeCopy.*foundMapping, copy.*foundMapping);
        }

        if(not isPartRangeEmpty(partRangeCopy))
        {
            ret.emplace_back(partRangeCopy, m_default);
        }

        return ret;
    }
};

template<typename T>
T toNumber(const std::string_view s) noexcept
{
    std::stringstream ss{std::string{s}};

    T v{};

    ss >> v;

    return v;
}

constexpr static std::size_t min = 1;
constexpr static std::size_t max = 4000;

std::vector<Rule2> parseRulesParagraph2(const std::string_view rulesParagraph) noexcept
{
    auto ruleLineView = rulesParagraph
        | std::views::split(std::string_view{"\n"})
        | std::views::transform([]<typename T>(T&& v) { return std::string_view{std::forward<T>(v)}; });

    std::vector<Rule2> rules{};
    for(const std::string_view ruleLine : ruleLineView)
    {
        const auto foundOpenBraces = std::ranges::find(ruleLine, '{');
        assert(foundOpenBraces != std::ranges::end(ruleLine));

        const auto foundCloseBraces = std::ranges::prev(std::ranges::end(ruleLine));

        const std::string_view ruleId{std::ranges::begin(ruleLine), foundOpenBraces};
        const std::string_view mappingsSubview{std::ranges::next(foundOpenBraces), foundCloseBraces};

        Rule2 rule{.m_id = std::string{ruleId}};
        for(const auto mapping : mappingsSubview | std::views::split(std::string_view{","}))
        {
            const std::string_view mappingView{mapping};
            
            auto mappingPartsView = mappingView
                | std::views::split(std::string_view{":"})
                | std::views::transform([]<typename T>(T&& v){ return std::string_view{std::forward<T>(v)}; });

            const std::vector<std::string_view> mappingParts{std::ranges::begin(mappingPartsView), std::ranges::end(mappingPartsView)};
            
            if(mappingParts.size() == 2)
            {
                const std::string_view mappingIdView{mappingParts[1]};
                const std::string_view mappingCondition{mappingParts[0]};

                const char mappingC = mappingCondition[0];
                const char mappingCommand = mappingCondition[1];
                const auto mappingNumber = toNumber<std::size_t>(mappingCondition.substr(2));

                const std::array commandToReturnValue = {
                    std::pair{'<', std::pair{Range(min, mappingNumber), std::string(mappingIdView)}},
                    std::pair{'>', std::pair{Range(mappingNumber + 1, max + 1), std::string(mappingIdView)}}
                };

                const auto foundReturnValue = std::ranges::find(commandToReturnValue, mappingCommand, &std::pair<char, std::pair<Range, std::string>>::first);
                assert(foundReturnValue != std::ranges::end(commandToReturnValue));

                rule.m_mappings.emplace_back(mappingC, foundReturnValue->second.first, foundReturnValue->second.second);
            }
            else if(mappingParts.size() == 1)
            {
                const std::string_view mappingIdView{mappingParts[0]};
                rule.m_default = std::string(mappingIdView);
            }
        }

        rules.emplace_back(rule);
    }

    return rules;
}


int main()
{
    const auto text = getStreamContents(std::cin);

    const auto&[rulesParagraph, partsParagraph] = parseText(text);

    const auto& rules = parseRulesParagraph2(rulesParagraph);

    constexpr static Range maxRange{.m_begin = min, .m_end = max + 1};
    constexpr static std::string_view successEnd{"A"};
    constexpr static std::string_view failEnd{"R"};
    constexpr static std::string_view start{"in"};


    std::vector<std::pair<PartRange, std::string>> mappings{};
    PartRange currentRange{.m_xRange = maxRange, .m_mRange = maxRange, .m_aRange = maxRange, .m_sRange = maxRange};
    std::vector<PartRange> solutions{};

    mappings.emplace_back(currentRange, std::string{start});
    while(not mappings.empty())
    {
        const auto newMapping = std::move(mappings.back());
        mappings.pop_back();

        if(newMapping.second == successEnd)
        {
            solutions.push_back(newMapping.first);
            continue;
        }
        if(newMapping.second == failEnd)
        {
            continue;
        }

        const auto foundRuleIter = std::ranges::find(rules, newMapping.second, &Rule2::m_id);
        assert(foundRuleIter != std::ranges::end(rules));

        const auto& foundRule = *foundRuleIter;
        std::vector<std::pair<PartRange, std::string>> moreMappings = foundRule(newMapping.first);

        moreMappings.erase(
            std::remove_if(
                std::begin(moreMappings), 
                std::end(moreMappings), 
                [](const auto& mapping) 
                { 
                    const auto&[pr, id] = mapping;
                    return pr.m_xRange.m_begin == pr.m_xRange.m_end and pr.m_mRange.m_begin == pr.m_mRange.m_end and pr.m_aRange.m_begin == pr.m_aRange.m_end && pr.m_sRange.m_begin == pr.m_sRange.m_end; 
                }
            ), 
            std::end(moreMappings)
        );

        for(auto&& mapping : moreMappings)
        {
            mappings.push_back(std::move(mapping));
        }
    }


    

    const std::size_t s = 
        (finalPartRange.m_xRange.m_end - finalPartRange.m_xRange.m_begin) *
        (finalPartRange.m_mRange.m_end - finalPartRange.m_mRange.m_begin) *
        (finalPartRange.m_aRange.m_end - finalPartRange.m_aRange.m_begin) *
        (finalPartRange.m_sRange.m_end - finalPartRange.m_sRange.m_begin);

    std::cout << "Solution: " << s << std::endl;
}