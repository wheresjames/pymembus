
find_package(libmembus QUIET)

if(libmembus_FOUND)

    message(STATUS "Found libmembus ${libmembus_VERSION}")
    include_directories("${libmembus_INCLUDE_DIRS}")
    link_directories("${libmembus_LIBRARIES}")

else()

    message(STATUS "Fetch libmembus")
    include(FetchContent)
    FetchContent_Declare(
        libmembus
        GIT_REPOSITORY      https://github.com/wheresjames/libmembus.git
        # GIT_TAG             v0.1.5
        GIT_TAG             main
        GIT_PROGRESS        TRUE
    )
    FetchContent_MakeAvailable(libmembus)

    if(NOT libmembus_POPULATED)
        message(FATAL_ERROR "libmembus not found")
    endif()

    set(DEPENDCHAIN ${DEPENDCHAIN} libmembus)

    include_directories(${libmembus_SOURCE_DIR}/src/main/headers)
    link_directories(${libmembus_BINARY_DIR}/lib)

endif()
