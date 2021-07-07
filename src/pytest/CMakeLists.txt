
#====================================================================
include(../python.cmake)


#====================================================================
set(TARGET ${PROJECT_NAME}-test)
set(BINARY ${PROJECT_BINARY_DIR}/lib/test.py)

add_custom_target(${TARGET} ALL
                    DEPENDS ${PROJECT_NAME}
                    COMMENT "Building ${TARGET}" VERBATIM)

enable_testing()
add_test(NAME ${TARGET}
            WORKING_DIRECTORY "${PROJECT_BINARY_DIR}/lib"
            COMMAND ${PYEXE} ${BINARY})

set_tests_properties(${TARGET} PROPERTIES TIMEOUT 10)

# Copy test file
add_custom_command(TARGET ${TARGET} POST_BUILD
                COMMAND ${CMAKE_COMMAND} -E copy "${CMAKE_CURRENT_SOURCE_DIR}/py/test.py" "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}")

# Execute test
add_custom_command(TARGET ${TARGET} POST_BUILD
                COMMAND ${CMAKE_CTEST_COMMAND} -C $<CONFIG> --output-on-failure --stop-on-failure --force-new-ctest-process) # --verbose)

