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

int main()
{
    const auto text = getStreamContents(std::cin);

    const auto&[rulesParagraph, partsParagraph] = parseText(text);

    const auto& rules = parseRulesParagraph(rulesParagraph);
    const auto& parts = parsePartsPragraph(partsParagraph);


    constexpr static std::string_view successEnd{"A"};
    constexpr static std::string_view failEnd{"R"};
    constexpr static std::string_view start{"in"};

    std::size_t s{};
    for(const Part& part : parts)
    {
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
            s += part['x'] + part['m'] + part['a'] + part['s'];
        }
    }

    std::cout << "Solution: " << s << std::endl;

    return 0;
}