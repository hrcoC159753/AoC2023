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
    std::optional<std::pair<Range, std::string>> m_xRange;
    std::optional<std::pair<Range, std::string>> m_mRange;
    std::optional<std::pair<Range, std::string>> m_aRange;
    std::optional<std::pair<Range, std::string>> m_sRange;
    std::string m_default;

    std::vector<std::pair<PartRange, std::string>> operator()(const PartRange& partRange) const noexcept
    {
        constexpr static auto getNewValue = [](const std::pair<Range, std::string>& pair1, const PartRange& p2, PartRange& p2Assign, Range PartRange::* rangePartRangePtr) noexcept -> std::pair<PartRange, std::string>
        {
            auto p2Copy = p2;
            const auto& p2Range = p2.*rangePartRangePtr;
            auto& p2CopyRange = p2Copy.*rangePartRangePtr;

            p2CopyRange = intersect(pair1.first, p2Range);
            p2Assign.*rangePartRangePtr = difference(p2Range, p2CopyRange);
            return std::pair{std::move(p2Copy), pair1.second};
        };

        PartRange pr = partRange;
        PartRange pra = pr;

        constexpr static auto isPartRangeEmpty = [](const PartRange& partRange)
        {
            return  partRange.m_xRange.m_begin == partRange.m_xRange.m_end || 
                    partRange.m_mRange.m_begin == partRange.m_mRange.m_end || 
                    partRange.m_aRange.m_begin == partRange.m_aRange.m_end || 
                    partRange.m_sRange.m_begin == partRange.m_sRange.m_end;
        };

        std::vector<std::pair<PartRange, std::string>> ret{};
        if(m_xRange.has_value())
        {
            auto value = getNewValue(*m_xRange, pr, pra, &PartRange::m_xRange);
            if(not isPartRangeEmpty(value.first))
            {
                ret.emplace_back(std::move(value));
            }
        }
        if(m_mRange.has_value())
        {
            auto value = getNewValue(*m_mRange, pr, pra, &PartRange::m_mRange);
            if(not isPartRangeEmpty(value.first))
            {
                ret.emplace_back(std::move(value));
            }
        }
        if(m_aRange.has_value())
        {
            auto value = getNewValue(*m_aRange, pr, pra, &PartRange::m_aRange);
            if(not isPartRangeEmpty(value.first))
            {
                ret.emplace_back(std::move(value));            
            }
        }
        if(m_sRange.has_value())
        {
            auto value = getNewValue(*m_sRange, pr, pra, &PartRange::m_sRange);
            if(not isPartRangeEmpty(value.first))
            {
                ret.emplace_back(std::move(value));
            }
        }

        if(not isPartRangeEmpty(pra))
        {
            ret.emplace_back(pra, m_default);
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

std::vector<Rule> parseRulesParagraph(const std::string_view rulesParagraph) noexcept
{
    auto ruleLineView = rulesParagraph
        | std::views::split(std::string_view{"\n"})
        | std::views::transform([]<typename T>(T&& v) { return std::string_view{std::forward<T>(v)}; });

    std::vector<Rule> rules{};
    for(const std::string_view ruleLine : ruleLineView)
    {
        const auto foundOpenBraces = std::ranges::find(ruleLine, '{');
        assert(foundOpenBraces != std::ranges::end(ruleLine));

        const auto foundCloseBraces = std::ranges::prev(std::ranges::end(ruleLine));

        const std::string_view ruleId{std::ranges::begin(ruleLine), foundOpenBraces};
        const std::string_view mappingsSubview{std::ranges::next(foundOpenBraces), foundCloseBraces};

        std::vector<Mapping> mappings{};
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

                mappings.emplace_back(
                    mappingC,
                    std::function<std::optional<std::string>(std::size_t)>(
                        [mappingNumber, mappingCommand, mappingId = std::string{mappingIdView}](const std::size_t n) -> std::optional<std::string>
                        {
                            if(mappingCommand == '<')
                            {
                                if(n < mappingNumber)
                                {
                                    return std::optional{mappingId};
                                }
                            }
                            else if(mappingCommand == '>')
                            {
                                if(n > mappingNumber)
                                {
                                    return std::optional{mappingId};
                                }
                            }
                            
                            return std::nullopt;
                        }
                    )
                );
            }
            else if(mappingParts.size() == 1)
            {
                const std::string_view mappingIdView{mappingParts[0]};
                mappings.emplace_back(
                    std::function<std::optional<std::string>(std::size_t)>{
                        [mappingId = std::string{mappingIdView}](const std::size_t n)
                        {
                            return std::optional{mappingId};
                        }
                    }
                );
            }
        }

        rules.emplace_back(
            std::string{ruleId},
            std::move(mappings)
        );
    }

    return rules;
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

                if(mappingC == 'x')
                {
                    if(mappingCommand == '<')
                    {
                        rule.m_xRange = std::pair{Range(min, mappingNumber), std::string(mappingIdView)};
                    }
                    else if(mappingCommand == '>')
                    {
                        rule.m_xRange = std::pair{Range(mappingNumber + 1, max + 1), std::string(mappingIdView)};
                    }
                    else
                    {
                        std::unreachable();
                    }
                }
                else if(mappingC == 'm')
                {
                    if(mappingCommand == '<')
                    {
                        rule.m_mRange = std::pair{Range(min, mappingNumber), std::string(mappingIdView)};
                    }
                    else if(mappingCommand == '>')
                    {
                        rule.m_mRange = std::pair{Range(mappingNumber + 1, max + 1), std::string(mappingIdView)};
                    }
                    else
                    {
                        std::unreachable();
                    }
                }
                else if(mappingC == 'a')
                {
                    if(mappingCommand == '<')
                    {
                        rule.m_aRange = std::pair{Range(min, mappingNumber), std::string(mappingIdView)};
                    }
                    else if(mappingCommand == '>')
                    {
                        rule.m_aRange = std::pair{Range(mappingNumber + 1, max + 1), std::string(mappingIdView)};
                    }
                    else
                    {
                        std::unreachable();
                    }
                }
                else if(mappingC == 's')
                {
                    if(mappingCommand == '<')
                    {
                        rule.m_sRange = std::pair{Range(min, mappingNumber), std::string(mappingIdView)};
                    }
                    else if(mappingCommand == '>')
                    {
                        rule.m_sRange = std::pair{Range(mappingNumber + 1, max + 1), std::string(mappingIdView)};
                    }
                    else
                    {
                        std::unreachable();
                    }

                }
                else
                {
                    std::unreachable();
                }
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


std::vector<Part> parsePartsPragraph(const std::string_view partsParagraph) noexcept
{
    std::vector<Part> parts;

    auto partLinesView = partsParagraph
        | std::views::split('\n');

    for(const auto partLine : partLinesView)
    {
        std::string_view partLineView{partLine};
        partLineView.remove_prefix(1);
        partLineView.remove_suffix(1);

        auto partAttributesView = partLineView
            | std::views::split(',');

        Part::Params p{};
        for(const auto attributeLine : partAttributesView)
        {
            const std::string_view attributeView{attributeLine};
            const char attributeName = attributeView[0];
            const auto attributeValue = toNumber<std::size_t>(attributeView.substr(2));
            if(attributeName == 'x') { p.x = attributeValue; }
            else if(attributeName == 'm') { p.m = attributeValue; }
            else if(attributeName == 'a') { p.a = attributeValue; }
            else if(attributeName == 's') { p.s = attributeValue; }
            else { std::unreachable(); }
        }

        parts.emplace_back(std::move(p));
    }

    return parts;
}

int main2()
{
    const auto text = getStreamContents(std::cin);

    const auto&[rulesParagraph, partsParagraph] = parseText(text);

    const auto& rules = parseRulesParagraph(rulesParagraph);
    // const auto& parts = parsePartsPragraph(partsParagraph);


    constexpr static std::string_view successEnd{"A"};
    constexpr static std::string_view failEnd{"R"};
    constexpr static std::string_view start{"in"};

    constinit static auto getNextPart = [p = std::optional{Part::Params{.x = 1, .m = 1, .a = 1, .s = 1}}]() mutable noexcept -> std::optional<typename Part::Params>
    {
        constexpr static std::size_t min = 1;
        constexpr static std::size_t max = 4000;

        if(p == std::nullopt)
        {
            return p;
        }

        const auto rv = p;
        auto& pr = *p;

        constexpr std::array valsPtr{&Part::Params::s, &Part::Params::a, &Part::Params::m, &Part::Params::x};
        const auto foundPtrIter = std::ranges::find_if(valsPtr, [&pr](const auto& ptr){ return pr.*ptr < max; });
        if(foundPtrIter == std::ranges::end(valsPtr))
        {
            p = std::nullopt;
            return rv;
        }

        const auto& foundPtr = *foundPtrIter;
        auto& v = pr.*foundPtr;
        ++v;

        std::ranges::for_each(std::ranges::begin(valsPtr), foundPtrIter, [&pr](const auto& ptr) { pr.*ptr = min; });

        return rv;
    };

    std::size_t s{};
    for(auto optPart = getNextPart(); optPart.has_value(); optPart = getNextPart())
    {
        const auto& part = *optPart;
        // std::cout << part.s << ' '  << part.a << ' ' << part.m << ' ' << part.x << std::endl;
        std::string currentRuleId{start};
        while(currentRuleId != successEnd and currentRuleId != failEnd)
        {
            const auto foundRule = std::ranges::find(rules, currentRuleId, &Rule::m_id);
            assert(foundRule != std::ranges::end(rules));

            const auto& rule = *foundRule;
            currentRuleId = rule(part);
        }

        if(currentRuleId == successEnd)
        {
            ++s;
            std::cout << s << std::endl;
        }
    }

    std::cout << "Solution: " << s << std::endl;

    return 0;
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

    PartRange currentRange{.m_xRange = maxRange, .m_mRange = maxRange, .m_aRange = maxRange, .m_sRange = maxRange};

    std::vector<std::pair<PartRange, std::string>> mappings{};
    mappings.emplace_back(currentRange, std::string{start});

    PartRange finalRange{};

    std::size_t s{};
    while(not mappings.empty())
    {
        const auto newMapping = std::move(mappings.back());
        mappings.pop_back();

        if(newMapping.second == successEnd)
        {
            const auto&[partRange, id] = newMapping;
            const auto& xRange = partRange.m_xRange;
            const auto& mRange = partRange.m_mRange;
            const auto& aRange = partRange.m_aRange;
            const auto& sRange = partRange.m_sRange;
            finalRange.m_xRange = difference(finalRange.m_xRange, intersect(finalRange.m_xRange, xRange));
            finalRange.m_mRange = difference(finalRange.m_mRange, intersect(finalRange.m_mRange, mRange));
            finalRange.m_aRange = difference(finalRange.m_aRange, intersect(finalRange.m_aRange, aRange));
            finalRange.m_sRange = difference(finalRange.m_sRange, intersect(finalRange.m_sRange, sRange));
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

    std::cout << "Solution: " << s << std::endl;
}