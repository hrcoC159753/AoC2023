#pragma once

#include <cstdint>
#include <string_view>
#include <vector>
#include <string>
#include <optional>
#include <compare>
#include <cassert>
#include <queue>
#include <iostream>

#include "cpp_utils/cpp_utils.h"

namespace aoc::day5
{

namespace part1
{
std::size_t solve(std::string_view text) noexcept;
}

namespace part2
{
std::size_t solve(const std::string_view text) noexcept;
std::size_t solve2(const std::string_view text) noexcept;
}

struct Seeds
{
    std::vector<std::size_t> m_seedNumbers;
};



struct Mapping
{
    std::size_t m_destinationNumber;
    std::size_t m_sourceNumber;
    std::size_t m_size;

    friend constexpr std::strong_ordering operator<=>(const Mapping&, const Mapping&) = default;
};


constexpr inline bool doMappingsIntersect(const Mapping& m1, const Mapping& m2) noexcept
{
    const auto& m1db = m1.m_destinationNumber;
    const auto m1de = m1.m_destinationNumber + m1.m_size - 1;
    const auto& m2sb = m2.m_sourceNumber;
    const auto m2se = m2.m_sourceNumber + m2.m_size - 1;

    /* m1db---------------------m1de                                        */
    /*                                    m2sb-----------------m2se         */
    const bool conditionOne = m1de < m2sb;

    /* m2sb---------------------m2se                                        */
    /*                                    m1db-----------------m1de         */
    const bool conditionTwo = m1db > m2se;

    return !(conditionOne || conditionTwo);
}

constexpr inline bool doRangesIntersect(
    const std::size_t firstRangeBegin,
    const std::size_t firstRangeEnd,
    const std::size_t secondRangeBegin,
    const std::size_t secondRangeEnd) noexcept
{
    return !(firstRangeEnd < secondRangeBegin || firstRangeBegin > secondRangeEnd);
}

constexpr inline std::pair<std::optional<Mapping>, std::optional<Mapping>> combineMappings(const Mapping& m1, const Mapping& m2) noexcept
{
    if(!doMappingsIntersect(m1, m2))
    {
        return std::pair{std::nullopt, std::optional{m1}};
    }

    const auto& m1db = m1.m_destinationNumber; 
    const auto m1de = m1.m_destinationNumber + m1.m_size - 1; 
    const auto& m1sb = m1.m_sourceNumber; 
    const auto m1se = m1.m_sourceNumber + m1.m_size - 1; 

    const auto& m2db = m2.m_destinationNumber; 
    const auto m2de = m2.m_destinationNumber + m2.m_size - 1; 
    const auto& m2sb = m2.m_sourceNumber;
    const auto m2se = m2.m_sourceNumber + m2.m_size - 1; 

    /*              m1db-----------------------------------m1de             */
    /*   m2sb--------------------------------------------------------m2se   */
    if(m1db >= m2sb && m1de <= m2se)
    {
        const std::size_t offsetFromBeginning = (m1db - m2sb);
        return std::pair{
            std::optional{ Mapping{m2db + offsetFromBeginning, m1sb, m1de - m1db + 1} }, 
            std::nullopt
        };
    } 
    /*  m1db-------------------------------------m1de           */
    /*           m2sb-------------------------------------m2se  */
    else if(m1db < m2sb and m1de < m2se)
    {
        const std::size_t offsetFromBeginning = (m2sb - m1db);
        return std::pair{
            std::optional{ Mapping{m2db, m1sb + offsetFromBeginning, m1de - m2sb + 1} }, 
            std::optional{ Mapping{m1db, m1sb, m2sb - m1db} }
            
        };
    }
    /*      m1db-------------------------------------m1de  */
    /*  m2sb-------------------------------------m2se  */
    else
    {
        const std::size_t offsetFromBeginning = (m1db - m2sb);
        return std::pair{
            std::optional{ Mapping{m2db + offsetFromBeginning, m1sb, m2se - m1db + 1} }, 
            std::optional{ Mapping{m1db + (m2se - m1db + 1), m1sb + (m2se - m1db) + 1, m1de - m2se} }
        };
    }
}

constexpr inline std::optional<Mapping> compose(const Mapping& m1, const Mapping& m2) noexcept
{
    const auto& m1sb = m1.m_sourceNumber;
    const auto m1se = m1.m_sourceNumber + m1.m_size - 1;
    const auto& m1db = m1.m_destinationNumber;
    const auto m1de = m1.m_destinationNumber + m1.m_size - 1;

    const auto& m2sb = m2.m_sourceNumber;
    const auto m2se = m2.m_sourceNumber + m2.m_size - 1;
    const auto& m2db = m2.m_destinationNumber;
    const auto m2de = m2.m_destinationNumber + m2.m_size - 1;

    if(!doRangesIntersect(m1db, m1de, m2sb, m2se))
    {
        return std::nullopt;
    }

    /*              m1db-----------------------------------m1de             */
    /*   m2sb--------------------------------------------------------m2se   */
    if(m1db >= m2sb && m1de <= m2se)
    {
        const std::size_t offsetFromBeginning = (m1db - m2sb);
        return std::optional{ Mapping{m2db + offsetFromBeginning, m1sb, m1de - m1db + 1} };
    } 
    /*  m1db-------------------------------------m1de           */
    /*           m2sb-------------------------------------m2se  */
    else if(m1db < m2sb && m1de < m2se)
    {
        const std::size_t offsetFromBeginning = (m2sb - m1db);
        return std::optional{ Mapping{m2db, m1sb + offsetFromBeginning, m1de - m2sb + 1} };
    }
    /*      m1db-------------------------------------m1de  */
    /*  m2sb-------------------------------------m2se  */
    else if(m1db > m2sb && m1de > m2se)
    {
        const std::size_t offsetFromBeginning = (m1db - m2sb);
        return std::optional{ Mapping{m2db + offsetFromBeginning, m1sb, m2se - m1db + 1} };
    }
    /*      m1db------------------------------------------------------------m1de    */
    /*              m2sb-------------------------------------m2se                   */
    else if(m1db <= m2sb && m1de >= m2se)
    {
        return std::optional{ Mapping{m2db, m1sb + (m2sb - m1db), m2se - m2sb + 1} };        
    }
    else
    {
        assert(false);
    }

    return std::nullopt;
}

constexpr inline std::optional<std::vector<Mapping>> difference(
    const Mapping& m1,
    const Mapping& m2
)
{
    const auto& m1sb = m1.m_sourceNumber;
    const auto m1se = m1.m_sourceNumber + m1.m_size - 1;
    const auto& m1db = m1.m_destinationNumber;
    const auto m1de = m1.m_destinationNumber + m1.m_size - 1;

    const auto& m2sb = m2.m_sourceNumber;
    const auto m2se = m2.m_sourceNumber + m2.m_size - 1;
    const auto& m2db = m2.m_destinationNumber;
    const auto m2de = m2.m_destinationNumber + m2.m_size - 1;

    if(!doRangesIntersect(m1db, m1de, m2sb, m2se))
    {
        return std::optional{std::vector{m1}};
    }
    /*   m1db--------------------------------------------------------m1de   */
    /*   m2sb--------------------------------------------------------m2se   */
    if(m1db == m2sb && m1de == m2se)
    {
        return std::nullopt;
    }
    /*              m1db-----------------------------------m1de             */
    /*   m2sb--------------------------------------------------------m2se   */
    else if(m1db > m2sb && m1de < m2se)
    {
        return std::nullopt;
    } 
    /*  m1db-------------------------------------m1de           */
    /*           m2sb-------------------------------------m2se  */
    else if(m1db <= m2sb && m1de <= m2se)
    {
        return std::optional{ std::vector{Mapping{m1db, m1sb, m2sb - m1db}} };
    }
    /*      m1db-------------------------------------m1de  */
    /*  m2sb-------------------------------------m2se  */
    else if(m1db >= m2sb && m1de >= m2se)
    {
        return std::optional{ std::vector{Mapping{m1db + (m2se - m1db) + 1, m1sb + (m2se - m1db) + 1, m1de - m2se}} };
    }
    /*      m1db------------------------------------------------------------m1de    */
    /*              m2sb-------------------------------------m2se                   */
    else if(m1db < m2sb && m1de > m2se)
    {
        return std::optional{ 
            std::vector{
                Mapping{m1db, m1sb, m2sb - m1db},
                Mapping{m1db + (m2se - m1db) + 1, m1sb + (m2se - m1db) + 1, m1de - m2se}
            } 
            };
    }
    else
    {
        assert(false);
    }

    return std::nullopt;
}

constexpr inline std::optional<std::vector<Mapping>> reverseDifference(
    const Mapping& m1,
    const Mapping& m2
)
{
    return difference(
        Mapping{m1.m_sourceNumber, m1.m_destinationNumber, m1.m_size},
        Mapping{m2.m_sourceNumber, m2.m_destinationNumber, m1.m_size}
    );
}

struct MappingInfo
{
    std::string m_source;
    std::string m_destination;
    std::vector<Mapping> m_mappings;
};

constexpr inline bool operator==(const MappingInfo& m1, const MappingInfo& m2) noexcept
{
    constexpr auto setEqual = [](const std::vector<Mapping>& mappings1, const std::vector<Mapping>& mappings2) noexcept
    {
        const bool firstCondition = std::ranges::all_of(
            mappings1, 
            [&](const Mapping& m){
                return std::ranges::find(mappings2, m) != std::ranges::end(mappings2);
            }
        );
    
        const bool secondCondition = std::ranges::all_of(
            mappings2, 
            [&](const Mapping& m){
                return std::ranges::find(mappings1, m) != std::ranges::end(mappings1);
            }
        );

        return firstCondition && secondCondition; 
    };

    return m1.m_source == m2.m_source && m1.m_destination == m2.m_destination && setEqual(m1.m_mappings, m2.m_mappings);
}

inline MappingInfo compose(const MappingInfo& m1, const MappingInfo& m2) noexcept
{
    assert(m1.m_destination == m2.m_source);

    std::vector<Mapping> newMappings{};

    for(const Mapping& m1Mapping : m1.m_mappings)
    {
        for(const Mapping& m2Mapping : m2.m_mappings)
        {
            const std::optional<Mapping> optNewMapping = compose(m1Mapping, m2Mapping);
            if(optNewMapping.has_value())
            {
                newMappings.push_back(*optNewMapping);
            }
        }
    }

    std::cout << "NewMappings: " << newMappings.size() << std::endl;

    std::vector<Mapping> leftoverMappings{};
    for(const Mapping& m1Mapping : m1.m_mappings)
    {
        std::queue<Mapping> needToCheck{};
        needToCheck.push(m1Mapping);

        while(!needToCheck.empty())
        {
            const Mapping& newMapping = needToCheck.front();
            bool didItPassAll = true;
            for(const Mapping& m2Mapping : m2.m_mappings)
            {
                const std::optional<std::vector<Mapping>> optDifference = difference(newMapping, m2Mapping);
                if(const bool hasDifference = optDifference.has_value(); hasDifference)
                {
                    const std::vector<Mapping>& difference = *optDifference;
                    if(difference.size() == 1 and difference[0] == newMapping)
                    {
                        continue;
                    }

                    didItPassAll = false;
                    for(const Mapping& mapping : difference)
                    {
                        needToCheck.push(mapping);
                    }
                }
                else
                {
                    didItPassAll = false;
                }
            }

            if(didItPassAll && std::ranges::find(leftoverMappings, newMapping) == std::ranges::end(leftoverMappings) && newMapping.m_size != 0)
            {
                leftoverMappings.push_back(newMapping);
            }
            needToCheck.pop();
        }
    }

    std::cout << "Leftover Mappings 1: " << leftoverMappings.size() << std::endl;

    for(const Mapping& m2Mapping : m2.m_mappings)
    {
        const Mapping reverseM2Mapping = Mapping{m2Mapping.m_sourceNumber, m2Mapping.m_destinationNumber, m2Mapping.m_size};
        std::queue<Mapping> needToCheck{};
        needToCheck.push(reverseM2Mapping);

        while(!needToCheck.empty())
        {
            const Mapping& newMapping = needToCheck.front();
            bool didItPassAll = true;
            for(const Mapping& m1Mapping : m1.m_mappings)
            {
                const Mapping& reverseM1Mapping = Mapping{m1Mapping.m_sourceNumber, m1Mapping.m_destinationNumber, m1Mapping.m_size};
                const std::optional<std::vector<Mapping>> optDifference = difference(newMapping, reverseM1Mapping);
                if(const bool hasDifference = optDifference.has_value(); hasDifference)
                {
                    const std::vector<Mapping>& difference = *optDifference;
                    if(difference.size() == 1 and difference[0] == newMapping)
                    {
                        continue;
                    }

                    didItPassAll = false;
                    for(const Mapping& mapping : difference)
                    {
                        needToCheck.push(mapping);
                    }
                }
                else
                {
                    didItPassAll = false;
                }
            }

            const Mapping newMappingForLeftovers{newMapping.m_sourceNumber, newMapping.m_destinationNumber, newMapping.m_size};
            if(didItPassAll && std::ranges::find(leftoverMappings, newMappingForLeftovers) == std::ranges::end(leftoverMappings) && newMappingForLeftovers.m_size != 0)
            {
                leftoverMappings.push_back(newMappingForLeftovers);
            }
            needToCheck.pop();
        }
    }
    
    for(const Mapping& leftover : leftoverMappings)
    {
        newMappings.push_back(leftover);
    }

    std::cout << "FinalMappings: " << newMappings.size() << std::endl;

    return MappingInfo
    {
        m1.m_source,
        m2.m_destination,
        std::move(newMappings)
    };
}


struct Data
{
    Seeds m_seeds;
    std::vector<MappingInfo> m_mappingInfos;
};

inline std::ostream& operator<<(std::ostream& os, const Seeds& seeds)
{
    using cpp_utils::operator<<;
    os << seeds.m_seedNumbers;

    return os;
}
inline std::ostream& operator<<(std::ostream& os, const Mapping& mapping)
{
    os << '{' << mapping.m_destinationNumber << ',' << ' ' << mapping.m_sourceNumber << ',' << ' ' << mapping.m_size << '}';

    return os;
}
inline std::ostream& operator<<(std::ostream& os, const MappingInfo& mappingInfo)
{
    using cpp_utils::operator<<;
    os << '{' << mappingInfo.m_source << ',' << ' ' << mappingInfo.m_destination << ',' << ' ' << mappingInfo.m_mappings << '}';

    return os;
}
inline std::ostream& operator<<(std::ostream& os, const Data& data)
{
    using cpp_utils::operator<<;
    os << '{' << data.m_seeds << ',' << ' ' << data.m_mappingInfos << '}'; 
    return os;
}

}