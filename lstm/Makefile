TRAIN_IMAGE = lstm_train:local
INFER_BUILD_IMAGE = lstm_infer_build:local

RESOLUTION_BYTE = ${RESOLUTION_BYTE:-8}
RESOLUTION_NUM = ${RESOLUTION_NUM:-3}
INPUT_SIZE = ${INPUT_SIZE:-40}

.PHONY: train train_image build_infer_image

all: train build_infer

train: model.tflite

model.tflite: train.py train_image
	docker run -it -e RESOLUTION_BYTE=$(RESOLUTION_BYTE) -e RESOLUTION_NUM=$(RESOLUTION_NUM) -e INPUT_SIZE=$(INPUT_SIZE) --rm -v $(PWD):/work -w /work $(TRAIN_IMAGE) train.py
	docker run -it -e RESOLUTION_BYTE=$(RESOLUTION_BYTE) -e RESOLUTION_NUM=$(RESOLUTION_NUM) -e INPUT_SIZE=$(INPUT_SIZE) --rm -v $(PWD):/work -w /work $(TRAIN_IMAGE) test.py

train_image: train.Dockerfile
	docker build -t  $(TRAIN_IMAGE) -f train.Dockerfile .

build_infer_image: infer.Dockerfile
	docker build --build-arg RESOLUTION_BYTE=$(RESOLUTION_BYTE) --build-arg RESOLUTION_NUM=$(RESOLUTION_NUM) --build-arg INPUT_SIZE=$(INPUT_SIZE) -t $(INFER_BUILD_IMAGE) -f infer.Dockerfile .
	echo "Built $(INFER_BUILD_IMAGE)"
