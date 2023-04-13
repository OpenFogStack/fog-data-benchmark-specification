ARG RESOLUTION_BYTE
ARG RESOLUTION_NUM
ARG INPUT_SIZE

FROM python:3.9-slim

RUN pip install tensorflow==2.12.0 tensorflow-io==0.32.0 scikit-learn==1.2.2

RUN mkdir /run
WORKDIR /run

COPY infer.py /run/infer.py
COPY model.tflite /run/model.tflite

ENV RESOLUTION_BYTE=${RESOLUTION_BYTE}
ENV RESOLUTION_NUM=${RESOLUTION_NUM}
ENV INPUT_SIZE=${INPUT_SIZE}

ENTRYPOINT [ "python3", "infer.py" ]