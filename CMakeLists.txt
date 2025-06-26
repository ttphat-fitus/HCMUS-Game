cmake_minimum_required(VERSION 3.10)
project(HCMUS-Game)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set compiler flags
if(MSVC)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W4")
else()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -O2")
endif()

# Include directories
include_directories(include)

# Find source files
file(GLOB_RECURSE SOURCES 
    "src/*.cpp"
    "main.cpp"
)

# Create executable
add_executable(HCMUS-Game ${SOURCES})

# Set output directory
set_target_properties(HCMUS-Game PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
)

# Link libraries
if(UNIX)
    target_link_libraries(HCMUS-Game pthread)
endif()

# Copy web files to build directory
file(COPY ${CMAKE_SOURCE_DIR}/index.html DESTINATION ${CMAKE_BINARY_DIR}/bin)
file(COPY ${CMAKE_SOURCE_DIR}/style.css DESTINATION ${CMAKE_BINARY_DIR}/bin)
file(COPY ${CMAKE_SOURCE_DIR}/web DESTINATION ${CMAKE_BINARY_DIR}/bin)

# Print build info
message(STATUS "Building HCMUS Battle Royale Game")
message(STATUS "C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "Build Type: ${CMAKE_BUILD_TYPE}")
message(STATUS "Output Directory: ${CMAKE_BINARY_DIR}/bin")

# Install target
install(TARGETS HCMUS-Game
    RUNTIME DESTINATION bin
)

install(FILES 
    ${CMAKE_SOURCE_DIR}/index.html
    ${CMAKE_SOURCE_DIR}/style.css
    DESTINATION share/hcmus-game
)

install(DIRECTORY ${CMAKE_SOURCE_DIR}/web
    DESTINATION share/hcmus-game
)
