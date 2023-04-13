FROM debian@sha256:0a78ed641b76252739e28ebbbe8cdbd80dc367fba4502565ca839e5803cfd86e

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    git \
    g++ \
    cmake \
    clang-tools \
    clang-format \
    libflatbuffers-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
RUN git clone https://github.com/tensorflow/tensorflow.git tensorflow_src --depth 1 --branch v2.12.0
RUN mkdir tflite_build
WORKDIR /build/tflite_build
# change CMAKELIST.txt for tensorflow lite
RUN perl -0777 -i.original -pe 's/${TFLITE_SOURCE_DIR}/profiling/telemetry/profiler.cc/${TFLITE_SOURCE_DIR}/profiling/telemetry/profiler.cc\n  ${TFLITE_SOURCE_DIR}/profiling/telemetry/telemetry.cc/igs' /build/tensorflow_src/tensorflow/lite/CMakeLists.txt
# build tensorflow lite
RUN cmake ../tensorflow_src/tensorflow/lite
RUN cmake --build . -j

ENTRYPOINT [ "/bin/bash", "entrypoint.sh" ]