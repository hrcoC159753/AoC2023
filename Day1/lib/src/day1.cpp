#include "aoc/day1/day1.h"

#include <cstdint>
#include <cctype>
#include <algorithm>
#include <cassert>
#include <ranges>
#include <string_view>
#include <numeric>
#include <functional>

#include <iostream>

namespace
{

constexpr bool isDigit(const char character) noexcept
{
    return static_cast<bool>(std::isdigit(static_cast<int>(character))); 
}

constexpr std::pair<char, char> getFirstAndLastDigitFromALine(const std::string_view line) noexcept
{
    const auto iteratorToFirstDigitPointer = std::ranges::find_if(line, isDigit);
    const auto iteratorToLastDigitPointer = std::ranges::find_if(std::rbegin(line), std::rend(line), isDigit);
    // const auto iteratorToLastDigitPointer = std::ranges::find_last_if(line, isDigit);

    assert(iteratorToFirstDigitPointer != std::ranges::end(line));
    assert(iteratorToLastDigitPointer != std::rend(line));

    return {*iteratorToFirstDigitPointer, *iteratorToLastDigitPointer};
}

constexpr std::pair<std::uint_fast8_t, std::uint_fast8_t> getFirstAndLastDigitFromPairOfCharacters(const std::pair<char, char>& pairOfDigitCharacters) noexcept
{
    const auto& [firstDigitCharacter, secondDigitCharacter] = pairOfDigitCharacters;
    
    assert(isDigit(firstDigitCharacter));
    assert(isDigit(secondDigitCharacter));

    const auto firstDigit = static_cast<std::uint_fast8_t>(firstDigitCharacter - '0');  
    const auto secondDigit = static_cast<std::uint_fast8_t>(secondDigitCharacter - '0');  

    return {firstDigit, secondDigit};
}

constexpr std::size_t getNumberFromPairOfItsDigits(const std::pair<std::uint_fast8_t, std::uint_fast8_t>& pairOfDigits) noexcept
{
    const auto& [firstDigit, secondDigit] = pairOfDigits;
    return firstDigit * 10 + secondDigit;
}

constexpr static std::array MAPPING_OF_DIGIT_WORDS_TO_DIGITS = {
        std::pair{"one",    std::uint_fast8_t{1}},
        std::pair{"two",    std::uint_fast8_t{2}},
        std::pair{"three",  std::uint_fast8_t{3}},
        std::pair{"four",   std::uint_fast8_t{4}},
        std::pair{"five",   std::uint_fast8_t{5}},
        std::pair{"six",    std::uint_fast8_t{6}},
        std::pair{"seven",  std::uint_fast8_t{7}},
        std::pair{"eight",  std::uint_fast8_t{8}},
        std::pair{"nine",   std::uint_fast8_t{9}}
};

constexpr bool isItStartingWithDigitString(const std::string_view view) noexcept
{
    using PairType = decltype(MAPPING_OF_DIGIT_WORDS_TO_DIGITS)::value_type;

    return std::ranges::any_of(
        MAPPING_OF_DIGIT_WORDS_TO_DIGITS, 
        [view](const std::string_view digitWord) noexcept -> bool
        {
            return view.starts_with(digitWord);
        },
        &PairType::first
    );
}

std::pair<std::uint_fast8_t, std::uint_fast8_t> getFirstAndLastDigitFromALinePart2(const std::string_view line) noexcept
{
    struct DigitGetter
    {
        constexpr static std::uint_fast8_t transformDigitToNumber(const std::string_view view) noexcept
        {
            assert(isDigit(view[0]));
            return static_cast<std::uint_fast8_t>(view[0] - '0');
        }

        constexpr static std::uint_fast8_t transformDigitWordToNumber(const std::string_view view) noexcept
        {
            assert(isItStartingWithDigitString(view));
         
            using PairType = decltype(MAPPING_OF_DIGIT_WORDS_TO_DIGITS)::value_type;

            const auto mappingFoundIterator = std::ranges::find_if(
                MAPPING_OF_DIGIT_WORDS_TO_DIGITS, 
                [view](const std::string_view digitWord) noexcept -> bool
                {
                    return view.starts_with(digitWord);
                },
                &PairType::first
            );

            assert(mappingFoundIterator != std::ranges::end(MAPPING_OF_DIGIT_WORDS_TO_DIGITS));

            return mappingFoundIterator->second;
        }

        constexpr bool operator()(const char& c) noexcept
        {
            assert(m_end != nullptr);

            const std::string_view view{&c, m_end};
            assert(view.size() > 0);

            if(isDigit(view[0]))
            {
                m_number = transformDigitToNumber(view);
                return true;
            }

            if(isItStartingWithDigitString(view))
            {
                m_number = transformDigitWordToNumber(view);
                return true;
            }

            return false;
        }

        constexpr std::size_t getNumber() const noexcept
        {
            assert(m_number.has_value());

            return *m_number;
        } 

        constexpr DigitGetter(const char* const end) noexcept
            : m_number{std::nullopt}, m_end{end}
        {

        }

        std::optional<std::uint_fast8_t> m_number{std::nullopt};
        const char* m_end{nullptr};
    };
    
    DigitGetter firstDigitGetter{&line.back() + 1};
    const auto iteratorToFirstDigit = std::ranges::find_if(line, std::ref(firstDigitGetter));

    DigitGetter lastDigitGetter{&line.back() + 1};
    const auto iteratorToLastDigit = 
        std::ranges::find_if(std::rbegin(line), std::rend(line), std::ref(lastDigitGetter));

    assert(iteratorToFirstDigit != std::ranges::end(line));
    assert(iteratorToLastDigit != std::rend(line));

    return {firstDigitGetter.getNumber(), lastDigitGetter.getNumber()};
}

}

namespace aoc::day1
{
    std::size_t solvePart1(const std::string& text) noexcept
    {
        namespace v = std::views;
        namespace r = std::ranges;

        constexpr static auto DELIMETER = '\n';
        constexpr static auto toStringView = [](auto&& v) { return std::string_view{v}; };
        auto rangeOfNumbers = text 
            | v::split(DELIMETER)
            | v::transform(toStringView)
            | v::transform(getFirstAndLastDigitFromALine)
            | v::transform(getFirstAndLastDigitFromPairOfCharacters)
            | v::transform(getNumberFromPairOfItsDigits);

        return std::accumulate(r::begin(rangeOfNumbers), r::end(rangeOfNumbers), std::size_t{});
    }

    std::size_t solvePart2(const std::string& text) noexcept
    {
        namespace v = std::views;
        namespace r = std::ranges;

        constexpr static auto DELIMETER = '\n';
        constexpr static auto toStringView = [](auto&& v) { return std::string_view{v}; };
        auto rangeOfNumbers = text 
            | v::split(DELIMETER)
            | v::transform(toStringView)
            | v::transform(getFirstAndLastDigitFromALinePart2)
            | v::transform(getNumberFromPairOfItsDigits);

        std::size_t sum{};
        for(auto&& num : rangeOfNumbers)
        {
            sum += num;
            // std::cout << num << std::endl;
        }
        return sum;
        return std::accumulate(r::begin(rangeOfNumbers), r::end(rangeOfNumbers), std::size_t{});
    }
}