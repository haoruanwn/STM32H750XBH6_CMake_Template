file(GLOB SOURCES "Src/*.c")
add_library(user_library STATIC ${SOURCES})


target_include_directories(user_library
        PUBLIC
        "${CMAKE_CURRENT_SOURCE_DIR}/Inc"


)

target_link_libraries(user_library
        PRIVATE
        stm32cubemx
)