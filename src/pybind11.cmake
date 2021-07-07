
include(FetchContent)
FetchContent_Declare(
  pybind11
  GIT_REPOSITORY    https://github.com/pybind/pybind11.git
  GIT_TAG           v2.6.2
  GIT_PROGRESS      TRUE
)
FetchContent_MakeAvailable(pybind11)
include_directories("${pybind11_SOURCE_DIR}/include")
