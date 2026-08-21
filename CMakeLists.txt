cmake_minimum_required(VERSION 3.20)

file(GLOB_RECURSE SOURCES src/*.c)

if(COMMAND idf_component_register)
    idf_component_register(SRCS ${SOURCES} INCLUDE_DIRS "include" REQUIRES u8g2)
    return()
endif()

project(u8g2-fusion-pixel-font)