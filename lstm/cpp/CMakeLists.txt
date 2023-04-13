cmake_minimum_required(VERSION 3.16)
project(minimal C CXX)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DTFLITE_DISABLE_TELEMETRY=1")

set(TENSORFLOW_SOURCE_DIR "" CACHE PATH
  "Directory that contains the TensorFlow project" )
if(NOT TENSORFLOW_SOURCE_DIR)
  get_filename_component(TENSORFLOW_SOURCE_DIR
    "${CMAKE_CURRENT_LIST_DIR}/../../../../" ABSOLUTE)
endif()

add_subdirectory(
  "${TENSORFLOW_SOURCE_DIR}/tensorflow/lite"
  "${CMAKE_CURRENT_BINARY_DIR}/tensorflow-lite" EXCLUDE_FROM_ALL)

add_executable(infer infer.cc)
target_link_libraries(infer tensorflow-lite)