
#====================================================================
# https://github.com/scikit-build/scikit-build-sample-projects


#====================================================================
set(DEPENDCHAIN "")
include(../python.cmake)
include(../pybind11.cmake)
include(../libmembus.cmake)


#====================================================================
# Library

set(BINARY ${PROJECT_NAME})

include_directories("${CMAKE_CURRENT_SOURCE_DIR}/headers")
file(GLOB_RECURSE SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/cpp/*.cpp")

add_library(${BINARY} MODULE ${SOURCES})
set_target_properties(${BINARY} PROPERTIES PREFIX "")
set_target_properties(${BINARY} PROPERTIES SUFFIX "${PYTHON_MODULE_EXTENSION}")
set_target_properties(${BINARY} PROPERTIES MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")

if(DEPENDCHAIN)
    add_dependencies(${BINARY} ${DEPENDCHAIN})
endif()

target_link_libraries(${BINARY} PRIVATE $<$<PLATFORM_ID:Windows>:lib>membus_static)

if(UNIX AND NOT APPLE)
    target_link_libraries(${BINARY} PRIVATE pthread rt)
endif()

add_custom_command(TARGET ${BINARY} POST_BUILD
                    COMMAND ${CMAKE_COMMAND} -E copy
                        "$<TARGET_FILE:${BINARY}>" "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}")


#====================================================================
# Install

install(TARGETS ${BINARY} LIBRARY DESTINATION "${PYINSTALL}/${PROJECT_NAME}")
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/py/__init__.py" DESTINATION "${PYINSTALL}/${PROJECT_NAME}")
# install(TARGETS libmembus LIBRARY DESTINATION "${PYINSTALL}/${PROJECT_NAME}")

