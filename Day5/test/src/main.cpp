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

TEST(Mappings, combineMappings) {
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

TEST(Mappings, compose) {
    {
        const Mapping m1{10, 0, 5};
        const Mapping m2{15, 8, 10};
        const Mapping expectedMapping{17, 0, 5};

        const auto optNewMapping = aoc::day5::compose(m1, m2);

        EXPECT_TRUE(optNewMapping.has_value());

        const auto newMapping = *optNewMapping;
        EXPECT_EQ(newMapping, expectedMapping);   
    }

    {
        const Mapping m1{11, 0, 6};
        const Mapping m2{2, 14, 4};
        const Mapping expectedNewMapping{2, 3, 3};

        const auto optNewMapping = aoc::day5::compose(m1, m2);
    
        EXPECT_TRUE(optNewMapping.has_value());
    
        const auto newMapping = *optNewMapping;
        EXPECT_EQ(newMapping, expectedNewMapping);   
    }

    {
        const Mapping m1{22, 5, 4};
        const Mapping m2{31, 19, 4};
        const Mapping expectedNewMapping{34, 5, 1};

        const auto optNewMapping = aoc::day5::compose(m1, m2);
    
        EXPECT_TRUE(optNewMapping.has_value());
    
        const auto newMapping = *optNewMapping;
        EXPECT_EQ(newMapping, expectedNewMapping);   
    }

    {
        const Mapping m1{11, 1, 6};
        const Mapping m2{100, 13, 2};
        const Mapping expectedNewMapping{100, 3, 2};

        const auto optNewMapping = aoc::day5::compose(m1, m2);

        EXPECT_TRUE(optNewMapping.has_value());

        const auto newMapping = *optNewMapping;
        EXPECT_EQ(newMapping, expectedNewMapping);
    }

    {
        const Mapping m1{0, 10, 5};
        const Mapping m2{100, 20, 5};

        const auto optNewMapping = aoc::day5::compose(m1, m2);

        EXPECT_FALSE(optNewMapping.has_value());
    }

    {
        const Mapping m1{10, 1, 3};
        const Mapping m2{20, 10, 3};
        const Mapping expectedNewMapping{20, 1, 3};

        const auto optNewMapping = aoc::day5::compose(m1, m2);

        EXPECT_TRUE(optNewMapping.has_value());
        const auto newMapping = *optNewMapping;
        EXPECT_EQ(newMapping, expectedNewMapping);
    }
}

TEST(Mappings, rdifference) 
{
    {
        const Mapping m1{10, 0, 5};
        const Mapping m2{15, 8, 10};
        const Mapping expectedMapping{17, 0, 5};

        const auto optNewMapping = aoc::day5::compose(m1, m2);

        EXPECT_TRUE(optNewMapping.has_value());

        const auto newMapping = *optNewMapping;
        EXPECT_EQ(newMapping, expectedMapping);

        const auto restMapping = aoc::day5::difference(m1, m2);

        EXPECT_FALSE(restMapping.has_value()); 
    }

    {
        const Mapping m1{11, 0, 6};
        const Mapping m2{2, 14, 4};
        const Mapping expectedNewMapping{2, 3, 3};
        const std::vector<Mapping> expectedRestMapping{Mapping{11, 0, 3}};

        const auto optNewMapping = aoc::day5::compose(m1, m2);
    
        EXPECT_TRUE(optNewMapping.has_value());
    
        const auto newMapping = *optNewMapping;
        EXPECT_EQ(newMapping, expectedNewMapping);

        const auto optRestMapping = aoc::day5::difference(m1, m2);
        EXPECT_TRUE(optRestMapping.has_value());

        const auto& restMapping = *optRestMapping;

        EXPECT_TRUE(
            std::ranges::all_of(
                restMapping, 
                [&](const Mapping& m){
                    return std::ranges::find(expectedRestMapping, m) != std::ranges::end(expectedRestMapping);
                }
            )
        );
        EXPECT_TRUE(
            std::ranges::all_of(
                expectedRestMapping, 
                [&](const Mapping& m){
                    return std::ranges::find(restMapping, m) != std::ranges::end(restMapping);
                }
            )
        );   
    }

    {
        const Mapping m1{22, 5, 4};
        const Mapping m2{31, 19, 4};
        const Mapping expectedNewMapping{34, 5, 1};
        const std::vector<Mapping> expectedRestMapping{Mapping{23, 6, 3}};

        const auto optNewMapping = aoc::day5::compose(m1, m2);
    
        EXPECT_TRUE(optNewMapping.has_value());
    
        const auto newMapping = *optNewMapping;
        EXPECT_EQ(newMapping, expectedNewMapping);

        const auto optRestMapping = aoc::day5::difference(m1, m2);
        EXPECT_TRUE(optRestMapping.has_value());

        const auto& restMapping = *optRestMapping;

        EXPECT_TRUE(
            std::ranges::all_of(
                restMapping, 
                [&](const Mapping& m){
                    return std::ranges::find(expectedRestMapping, m) != std::ranges::end(expectedRestMapping);
                }
            )
        );
        EXPECT_TRUE(
            std::ranges::all_of(
                expectedRestMapping, 
                [&](const Mapping& m){
                    return std::ranges::find(restMapping, m) != std::ranges::end(restMapping);
                }
            )
        );  
    }

    {
        const Mapping m1{11, 1, 6};
        const Mapping m2{100, 13, 2};
        const Mapping expectedNewMapping{100, 3, 2};
        const std::vector<Mapping> expectedRestMapping{Mapping{11, 1, 2}, Mapping{15, 5, 2}};

        const auto optNewMapping = aoc::day5::compose(m1, m2);
    
        EXPECT_TRUE(optNewMapping.has_value());
    
        const auto newMapping = *optNewMapping;
        EXPECT_EQ(newMapping, expectedNewMapping);

        const auto optRestMapping = aoc::day5::difference(m1, m2);
        EXPECT_TRUE(optRestMapping.has_value());

        const auto& restMapping = *optRestMapping;

        EXPECT_TRUE(
            std::ranges::all_of(
                restMapping, 
                [&](const Mapping& m){
                    return std::ranges::find(expectedRestMapping, m) != std::ranges::end(expectedRestMapping);
                }
            )
        );
        EXPECT_TRUE(
            std::ranges::all_of(
                expectedRestMapping, 
                [&](const Mapping& m){
                    return std::ranges::find(restMapping, m) != std::ranges::end(restMapping);
                }
            )
        );  
    }

    {
        const Mapping m1{0, 10, 5};
        const Mapping m2{100, 20, 5};
        const std::vector<Mapping> expectedRestMapping{m1};

        const auto optNewMapping = aoc::day5::compose(m1, m2);

        EXPECT_FALSE(optNewMapping.has_value());

        const auto optRestMapping = aoc::day5::difference(m1, m2);
        EXPECT_TRUE(optRestMapping.has_value());

        const auto& restMapping = *optRestMapping;

        EXPECT_TRUE(
            std::ranges::all_of(
                restMapping, 
                [&](const Mapping& m){
                    return std::ranges::find(expectedRestMapping, m) != std::ranges::end(expectedRestMapping);
                }
            )
        );
        EXPECT_TRUE(
            std::ranges::all_of(
                expectedRestMapping, 
                [&](const Mapping& m){
                    return std::ranges::find(restMapping, m) != std::ranges::end(restMapping);
                }
            )
        );  

    }

    {
        const Mapping m1{10, 1, 3};
        const Mapping m2{20, 10, 3};
        const Mapping expectedNewMapping{20, 1, 3};

        const auto optNewMapping = aoc::day5::compose(m1, m2);

        EXPECT_TRUE(optNewMapping.has_value());
        const auto newMapping = *optNewMapping;
        EXPECT_EQ(newMapping, expectedNewMapping);

        const auto optRestMapping = aoc::day5::difference(m1, m2);
        EXPECT_FALSE(optRestMapping.has_value());

    }
}

TEST(MappingInfo, equals)
{
    const MappingInfo m1
    {
        "x",
        "y",
        std::vector<Mapping>
        {
            {11, 1, 4},
            {20, 7, 3}
        }
    };
    const MappingInfo m2
    {
        "x",
        "y",
        std::vector<Mapping>
        {
            {11, 1, 4},
            {20, 7, 3}
        }
    };

    ASSERT_EQ(m1, m2);
}

TEST(MappingInfo, compose) 
{
    const MappingInfo m1
    {
        "x",
        "y",
        std::vector<Mapping>
        {
            {11, 1, 4},
            {20, 7, 3}
        }
    };

    const MappingInfo m2
    {
        "y",
        "z",
        std::vector<Mapping>
        {
            {100, 9, 4},
            {30, 14, 7}
        }
    };

    const MappingInfo expectedMappingInfo
    {
        "x",
        "z",
        std::vector<Mapping>
        {
            {100, 9, 2},
            {102, 1, 2},
            {13, 3, 1},
            {30, 4, 1},
            {31, 15, 5},
            {36, 7, 1},
            {21, 8, 2}
        }
    };

    const MappingInfo newMappingInfo = compose(m1, m2);
    EXPECT_EQ(newMappingInfo, expectedMappingInfo);
} 
