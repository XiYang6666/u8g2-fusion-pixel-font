cmake_minimum_required(VERSION 3.20)
project(u8g2-fusion-pixel-font)

file(GLOB_RECURSE SOURCES src/*.c)
idf_component_register(SRCS ${SOURCES}
        INCLUDE_DIRS "include"
        REQUIRES u8g2
)