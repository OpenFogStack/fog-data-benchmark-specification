# Seismic LSTM Model Inference

We provide a trained LSTM model to infer data about seismic events.
Note that this is purely for demonstrative purposes, in order to accurately emulate processing delay and performance impact of ML inference in our benchmark.
We make no claims on the accuracy of the inference results (although they are probably not good).

## Prerequisites

Use Docker to train the models.
Make is required to build everything.

## Training

Create the model with `make`.

Set the following parameters as environment variables:

- `RESOLUTION_BYTE`: The resolution of the sensor in bytes. Default: 8 (64 bit)
- `RESOLUTION_NUM`: Number of data points to generate. Default: 3 (X, Y, Z)
- `INPUT_SIZE`: Number of data points to consider as data input. Default: 40

Note that the input data size can be derived from the number of samples combined in aggregate reports of a sensor ($N_\mathrm{agg}$), sensor sampling rate ($f$), and LSTM input data size ($t_\mathrm{LSTM}$): $\frac{f}{N_\mathrm{agg}} \times t_\mathrm{LSTM}$

The training script trains the model on random data.

## Inference

Inference is available through a Docker image.
Run `make build_infer_image` to create the image.
Then run the image as a container with:

    ```sh
    docker run -it --rm lstm_infer_build:local
    ```

Communication is currently through `stdin` and `stdout`, i.e., enter your data in `stdin` in the format:

```text
[point1] [point2] ... [pointN]
[point1] [point2] ... [pointN]
[point1] [point2] ... [pointN]
...
[point1] [point2] ... [pointN]
```

With `N` equal to `RESOLUTION_NUM`, in float or integer format.
Every `INPUT_SIZE` lines, an inference result is output on `stdout`.
