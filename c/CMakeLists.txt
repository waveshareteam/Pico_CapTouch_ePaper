cmake_minimum_required(VERSION 3.12)
include(pico_sdk_import.cmake)
project(Pico_ePaper_Code)
pico_sdk_init()

#添加编译子目录
add_subdirectory(lib/Config)
add_subdirectory(lib/e-Paper)
add_subdirectory(lib/Driver)
add_subdirectory(lib/Fonts)
add_subdirectory(lib/GUI)

#添加头文件目录
include_directories(./lib/Config)
include_directories(./lib/e-Paper)
include_directories(./lib/Driver)
include_directories(./lib/GUI)

# 生成可执行文件
add_executable(epd 
main.c
)

# enable usb output, disable uart output
pico_enable_stdio_usb(epd 1)
pico_enable_stdio_uart(epd 0)

# create map/bin/hex/uf2 file etc.
pico_add_extra_outputs(epd)

target_link_libraries(epd ePaper Driver GUI Fonts Config pico_stdlib)