cmake_minimum_required(VERSION 3.23)

project(AoC_lib LANGUAGES CXX)

set(RELATIVE_RESOURCE_DIR "res")
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/template/include/aoc/res.h.in
    ${CMAKE_CURRENT_BINARY_DIR}/include/aoc/res.h
    @ONLY
)

add_library(aoc)
target_sources(aoc
    PRIVATE
        src/aoc.cpp
    PUBLIC
        FILE_SET HEADERS
        TYPE HEADERS
        BASE_DIRS
            include
            ${CMAKE_CURRENT_BINARY_DIR}/include
        FILES
            include/aoc/aoc.h
            ${CMAKE_CURRENT_BINARY_DIR}/include/aoc/res.h
)

install(
    TARGETS
        aoc
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR} COMPONENT Aoc_Development
    ARCHIVE FILE_SET HEADERS DESTINATION ${CMAKE_INSTALL_LIBDIR} COMPONENT Aoc_Development
)
