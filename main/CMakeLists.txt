cmake_minimum_required(VERSION 3.25)
project(main)

set(CMAKE_CXX_STANDARD 14)

include_directories(.)

add_executable(main
        main.cpp
        TicTacToe.h)
