cmake_minimum_required(VERSION 3.23)

add_executable(day5_part2)
target_sources(day5_part2
    PRIVATE
        src/main.cpp
)
target_link_libraries(day5_part2
    PRIVATE
        day5
)

add_custom_target(day5_part2_res)
add_dependencies(day5_part2 day5_part2_res)
add_custom_command(
    TARGET day5_part2_res
    POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_LIST_DIR}/res/initial_input2.txt ${CMAKE_CURRENT_BINARY_DIR}/initial_input2.txt
        COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_LIST_DIR}/res/input2.txt ${CMAKE_CURRENT_BINARY_DIR}/input2.txt
)