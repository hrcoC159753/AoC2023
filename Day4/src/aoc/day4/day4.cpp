#include "aoc/day4/day4.h"

#include <ranges>
#include <algorithm>
#include <cstdint>
#include <string_view>
#include <string>
#include <optional>
#include <utility>
#include <vector>
#include <cassert>
#include <concepts>
#include <sstream>
#include <numeric>

#include <iostream>

namespace
{

struct Card
{
    std::size_t m_id;
    std::vector<std::size_t> m_winningNumbers;
    std::vector<std::size_t> m_numbers;
};

template<typename T>
std::ostream& operator<<(std::ostream& os, const std::vector<T>& vec)
{
    os << '{';
    for(auto&& elem : vec)
    {
        os << elem << ", ";
    }
    os << "}";
    return os;
}

std::ostream& operator<<(std::ostream& os, const Card& card)
{
    os << '{' << card.m_id << ", " << card.m_winningNumbers << ", " << card.m_numbers << '}';
    return os;
}

std::string_view trim(std::string_view in) noexcept
{
    auto left = in.begin();
    for (;; ++left) 
    {
        if (left == in.end())
        {
            return std::string_view();
        }
        if (!::isspace(*left))
        {
            break;
        }
    }
    auto right = in.end() - 1;
    for (; right > left && ::isspace(*right); --right);
    return std::string_view(left, std::distance(left, right) + 1);
}

template<typename T>
requires std::default_initializable<T> and std::unsigned_integral<T>
constexpr T toNumber(const std::string_view numberView) noexcept
{
    std::stringstream ss{std::string{numberView}};
    T returnValue{};
    ss >> returnValue;
    return returnValue;
}

template<typename T>
inline T peek(T&& e) noexcept
{
    std::cout << '\'' << e << '\'' << std::endl;
    return std::forward<T>(e);
}

constexpr static bool isEmptyString(const std::string_view view) noexcept
{
    return view.size() == 0;
}

constexpr static bool isNonEmptyString(const std::string_view view) noexcept
{
    return !isEmptyString(view);
}

std::vector<Card> parseToCards(const std::string_view text) noexcept
{
    namespace v = std::views;
    namespace r = std::ranges;

    constexpr static auto toStringView = [](auto&& v){ return std::string_view{std::forward<decltype(v)>(v)}; };

    constexpr static auto toLineSplit = [](const std::string_view line) -> std::pair<std::string_view, std::string_view>
    {
        auto lineSplitView = line 
            | v::split(':')
            | v::transform(toStringView)
            | v::transform(::trim);

        std::vector<std::string_view> lineSplit{
            std::ranges::begin(lineSplitView),
            std::ranges::end(lineSplitView)
        };
            
        assert(lineSplit.size() == 2);

        return std::pair{lineSplit[0], lineSplit[1]}; 
    };

    constexpr static auto cardPartViewToCardId = [](const std::string_view cardPartViewInput) -> std::size_t 
    {
        auto cardPartView = cardPartViewInput
            | v::split(' ')
            | v::transform(toStringView)
            | v::transform(::trim)
            | v::filter(isNonEmptyString);
                
        const std::vector<std::string_view> cardPartSplit{
            r::begin(cardPartView),
            r::end(cardPartView)
        };
        
        assert(cardPartSplit.size() == 2);
        const std::string_view cardNumber = cardPartSplit[1];

        return toNumber<std::size_t>(cardNumber);
    };

    constexpr static auto numberLineToNumberVector = [](const std::string_view numberLine) -> std::vector<std::size_t>
    {
        auto numbersView = numberLine
            | v::split(' ')
            | v::transform(toStringView)
            | v::transform(::trim)
            | v::filter(isNonEmptyString)
            | v::transform(::toNumber<std::size_t>);
        
        return std::vector<std::size_t>{
            r::begin(numbersView), 
            r::end(numbersView)
        };
    };

    constexpr static auto numberPartViewToNumbers = [](const std::string_view numberPartView) -> std::pair<std::vector<std::size_t>, std::vector<std::size_t>>
    {
        auto allNumbersSplitView = numberPartView
            | v::split('|')
            | v::transform(toStringView)
            | v::transform(::trim);
        
        const std::vector<std::string_view> allNumberSplit{
            r::begin(allNumbersSplitView),
            r::end(allNumbersSplitView)
        };

        assert(allNumberSplit.size() == 2);
        const std::string_view winningNumbersLineView = allNumberSplit[0];
        const std::string_view numbersLineView = allNumberSplit[1];

        return std::pair<std::vector<std::size_t>, std::vector<std::size_t>>{
            numberLineToNumberVector(winningNumbersLineView),
            numberLineToNumberVector(numbersLineView)
        };
    };

    auto cardView = text 
        | v::split('\n') 
        | v::transform(toStringView)
        | v::transform(
            [](const std::string_view line) noexcept
            {
                
                const auto[cardPartView, numberPartView] = toLineSplit(line);

                const std::size_t cardId = cardPartViewToCardId(cardPartView);
                auto [winningNumbers, numbers] = numberPartViewToNumbers(numberPartView);

                return Card{cardId, winningNumbers, numbers};
            }
        );

    return std::vector<Card>
    {
        r::begin(cardView),
        r::end(cardView)
    };
}

constexpr static std::size_t countSameElements(const std::vector<std::size_t>& first, const std::vector<std::size_t>& second) noexcept
{
    std::size_t count{};

    for(const auto& elem : first)
    {
        if(std::ranges::find(second, elem) != std::ranges::end(second))
        {
            count++;
        }
    }

    return count;
}

constexpr static std::size_t numberOfSameElementsToSolution(const std::size_t numberOfSameElements) noexcept
{
    return static_cast<std::size_t>(1u << numberOfSameElements) >> 1u;
}

}

namespace aoc::day4::part1
{

std::size_t solve(const std::string_view text) noexcept
{
    namespace v = std::views;
    namespace r = std::ranges;

    const std::vector<Card> cards = parseToCards(text);

    auto solutions = cards
        | v::transform([](const Card& card) { return countSameElements(card.m_winningNumbers, card.m_numbers); })
        | v::transform(numberOfSameElementsToSolution);

    return std::accumulate(r::begin(solutions), r::end(solutions), std::size_t{});
}

}

namespace aoc::day4::part2
{

std::size_t solve(const std::string_view text) noexcept
{
    return 2;
}

}