cmake_minimum_required(VERSION 3.20)

file(GLOB_RECURSE SOURCES src/*.c)

if (COMMAND idf_component_register)
    idf_component_register(SRCS ${SOURCES} INCLUDE_DIRS "include" REQUIRES u8g2)
    target_compile_definitions(${COMPONENT_LIB}
            PRIVATE

    )
    target_compile_options(${COMPONENT_LIB}
            PRIVATE
            -include u8g2_fusion_pixel_font.h
    )
    return()
endif ()

project(u8g2-fusion-pixel-font)