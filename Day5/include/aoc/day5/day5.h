#pragma once

#include <cstdint>
#include <string_view>
#include <vector>
#include <string>
#include <optional>
#include <compare>

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


struct MappingInfo
{
    std::string m_source;
    std::string m_destination;
    std::vector<Mapping> m_mappings;
};



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