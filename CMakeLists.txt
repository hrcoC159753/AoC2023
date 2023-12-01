cmake_minimum_required(VERSION 3.23)

project(AoC 
    LANGUAGES CXX
    VERSION 2023
)
enable_testing()

set(CMAKE_CXX_STANDARD 23)

find_package(GTest REQUIRED)

add_subdirectory(lib)

add_subdirectory(Day1)

include(GNUInstallDirs)
install(
    TARGETS
        day1
        day1_part1
        day1_part2
    ARCHIVE DESTINATION Day1/${CMAKE_INSTALL_LIBDIR} COMPONENT Day1_Runtime
    RUNTIME DESTINATION Day1/${CMAKE_INSTALL_BINDIR} COMPONENT Day1_Runtime
    FILE_SET HEADERS DESTINATION Day1/${CMAKE_INSTALL_INCLUDEDIR} COMPONENT Day1_Development
)