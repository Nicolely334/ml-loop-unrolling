cmake_minimum_required(VERSION 3.13)
project(MLUnrollPass)

find_package(LLVM REQUIRED CONFIG)

message(STATUS "Found LLVM ${LLVM_PACKAGE_VERSION}")
message(STATUS "Using LLVMConfig.cmake in: ${LLVM_DIR}")

include_directories(${LLVM_INCLUDE_DIRS})
add_definitions(${LLVM_DEFINITIONS})

add_library(MLUnrollPass MODULE MLUnrollPass.cpp)

# platform-specific settings
if(APPLE)
    set_target_properties(MLUnrollPass PROPERTIES
        LINK_FLAGS "-undefined dynamic_lookup"
    )
endif()
