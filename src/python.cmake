
#====================================================================
# https://scikit-build.readthedocs.io/en/latest/cmake-modules/PythonExtensions.html

set(NEWPY "YES")

if("${PYVER}" STREQUAL "")
    set(PYVER "=${PYTHON_VERSION_STRING}")
endif()

message(STATUS "PYVER: ${PYVER}")

if(${PYVER} MATCHES "=")
    string(REPLACE "=" "" PYVER "${PYVER}")
    if(NOT "${PYVER}" STREQUAL "")
        set(PYEQ "EXACT")
    endif()    
endif()


if(${NEWPY})
    find_package (Python3 ${PYVER} ${PYEQ} COMPONENTS Interpreter Development)
    if(NOT Python3_FOUND OR NOT Python3_Development_FOUND)
        if("${PYEQ}" STREQUAL "")
            message(FATAL_ERROR "Python not found : ${PYVER}")
        else()
            message(STATUS "!!!! Exact Python version not found : ${PYVER}")
            find_package (Python3 COMPONENTS Interpreter Development)
            if(NOT Python3_FOUND OR NOT Python3_Development_FOUND)
                message(FATAL_ERROR "Python not found : ${PYVER}")
            endif()
        endif()
    endif()
    set(PYINC ${Python3_INCLUDE_DIRS})
    set(PYLIB ${Python3_LIBRARY_DIRS})
    set(PYMAJOR ${Python3_VERSION_MAJOR})
    set(PYMINOR ${Python3_VERSION_MINOR})
else()
    find_package(PythonExtensions REQUIRED)
    python_extension_module(${BINARY})
    set(PYINC ${PYTHON_INCLUDE_DIR})
    get_filename_component(PYLIB ${PYTHON_LIBRARY} DIRECTORY)
    set(PYMAJOR ${PYTHON_VERSION_MAJOR})
    set(PYMINOR ${PYTHON_VERSION_MINOR})
endif()

include_directories(${PYINC})
link_directories(${PYLIB})

if(WIN32)
    set(PYINSTALL "lib/site-packages")
else()
    if(NOT ${PYMINOR})
        set(PYINSTALL "lib/python${PYMAJOR}/site-packages")
    else()
        set(PYINSTALL "lib/python${PYMAJOR}.${PYMINOR}/site-packages")
    endif()
endif()
