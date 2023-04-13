#!/bin/bash

cd /build
mkdir infer
cp /run/cpp/CMakeLists.txt /build/infer
cp /run/cpp/infer.cc /build/infer

mkdir infer_build
cd infer_build

cmake ../infer -DTENSORFLOW_SOURCE_DIR=/build/tensorflow
cmake --build . -j