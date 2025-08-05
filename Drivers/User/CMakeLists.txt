file(GLOB SOURCES "Src/*.c")
add_library(user_driver STATIC ${SOURCES})


target_include_directories(user_driver
        PUBLIC
        "${CMAKE_CURRENT_SOURCE_DIR}/Inc"

)

target_link_libraries(user_driver
        PRIVATE
        stm32cubemx
)