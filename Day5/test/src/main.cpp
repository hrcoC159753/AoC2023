#include <gtest/gtest.h>

#include "aoc/day5/day5.h"

using namespace aoc::day5;

TEST(Mappings, MappingsAreIntersection) {
    EXPECT_TRUE(aoc::day5::doMappingsIntersect(Mapping{10, 0, 5}, Mapping{15, 8, 10}));
    EXPECT_FALSE(aoc::day5::doMappingsIntersect(Mapping{10, 0, 5}, Mapping{15, 15, 1}));
    EXPECT_TRUE(aoc::day5::doMappingsIntersect(Mapping{10, 0, 5}, Mapping{15, 14, 1}));
    EXPECT_FALSE(aoc::day5::doMappingsIntersect(Mapping{10, 0, 5}, Mapping{15, 9, 1}));
    EXPECT_TRUE(aoc::day5::doMappingsIntersect(Mapping{10, 0, 5}, Mapping{15, 9, 2}));
    EXPECT_TRUE(aoc::day5::doMappingsIntersect(Mapping{22, 5, 4}, Mapping{31, 19, 4}));
}

TEST(Mappings, MappingComposition) {
    {
        const Mapping m1{10, 0, 5};
        const Mapping m2{15, 8, 10};
        const Mapping expectedMapping{17, 0, 5};

        const auto[optNewMapping, optOldMapping] = aoc::day5::combineMappings(m1, m2);

        EXPECT_TRUE(optNewMapping.has_value());
        EXPECT_FALSE(optOldMapping.has_value());

        const auto newMapping = *optNewMapping;
        EXPECT_EQ(newMapping, expectedMapping);   
    }

    {
        const Mapping m1{11, 0, 6};
        const Mapping m2{2, 14, 4};
        const Mapping expectedNewMapping{2, 3, 3};
        const Mapping expectedOldMapping{11, 0, 3};

        const auto[optNewMapping, optOldMapping] = aoc::day5::combineMappings(m1, m2);
    
        EXPECT_TRUE(optNewMapping.has_value());
        EXPECT_TRUE(optOldMapping.has_value());
    
        const auto newMapping = *optNewMapping;
        EXPECT_EQ(newMapping, expectedNewMapping);   

        const auto oldMapping = *optOldMapping;
        EXPECT_EQ(oldMapping, expectedOldMapping);   
    }

    {
        const Mapping m1{22, 5, 4};
        const Mapping m2{31, 19, 4};
        const Mapping expectedNewMapping{34, 5, 1};
        const Mapping expectedOldMapping{23, 6, 3};

        const auto[optNewMapping, optOldMapping] = aoc::day5::combineMappings(m1, m2);
    
        EXPECT_TRUE(optNewMapping.has_value());
        EXPECT_TRUE(optOldMapping.has_value());
    
        const auto newMapping = *optNewMapping;
        EXPECT_EQ(newMapping, expectedNewMapping);   

        const auto oldMapping = *optOldMapping;
        EXPECT_EQ(oldMapping, expectedOldMapping);   
    }

    {
        const Mapping m1{90, 15, 4};
        const Mapping m2{0, 86, 7};
        const Mapping expectedNewMapping{4, 15, 3};
        const Mapping expectedOldMapping{93, 18, 1};

        const auto[optNewMapping, optOldMapping] = aoc::day5::combineMappings(m1, m2);
    
        EXPECT_TRUE(optNewMapping.has_value());
        EXPECT_TRUE(optOldMapping.has_value());
    
        const auto newMapping = *optNewMapping;
        EXPECT_EQ(newMapping, expectedNewMapping);   

        const auto oldMapping = *optOldMapping;
        EXPECT_EQ(oldMapping, expectedOldMapping);   
    }

    {
        const Mapping m1{1, 101, 3};
        const Mapping m2{50, 0, 3};
        const Mapping expectedNewMapping{51, 101, 2};
        const Mapping expectedOldMapping{3, 103, 1};

        const auto[optNewMapping, optOldMapping] = aoc::day5::combineMappings(m1, m2);
    
        EXPECT_TRUE(optNewMapping.has_value());
        EXPECT_TRUE(optOldMapping.has_value());
    
        const auto newMapping = *optNewMapping;
        EXPECT_EQ(newMapping, expectedNewMapping);   

        const auto oldMapping = *optOldMapping;
        EXPECT_EQ(oldMapping, expectedOldMapping);   
    }

    {
        const Mapping m1{0, 10, 5};
        const Mapping m2{100, 20, 5};

        const auto[optNewMapping, optOldMapping] = aoc::day5::combineMappings(m1, m2);

        EXPECT_FALSE(optNewMapping.has_value());
        EXPECT_TRUE(optOldMapping.has_value());

        const auto oldMapping = *optOldMapping;
        EXPECT_EQ(oldMapping, m1);
    }
}