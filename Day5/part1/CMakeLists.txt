cmake_minimum_required(VERSION 3.23)

add_executable(day5_part1)
target_sources(day5_part1
    PRIVATE
        src/main.cpp
)
target_link_libraries(day5_part1
    PRIVATE
        day5
)

add_custom_target(day5_part1_res)
add_dependencies(day5_part1 day5_part1_res)
add_custom_command(
    TARGET day5_part1_res
    POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_LIST_DIR}/res/initial_input1.txt ${CMAKE_CURRENT_BINARY_DIR}/initial_input1.txt
        COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_LIST_DIR}/res/input1.txt ${CMAKE_CURRENT_BINARY_DIR}/input1.txt
)