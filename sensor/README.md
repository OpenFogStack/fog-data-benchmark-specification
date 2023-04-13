# Sensor Data Generator

 Sensor load generator.
 This load generator takes a set of parameters from environment variables and
 generates a sensor reading in a given interval.
 The sensor reading is written to stdout.
 The sensor reading is converted to an unsigned integer in base16.
 The threshold is always `MAX_UINT/2`, with `MAX_UINT` depending on the chosen sensor resolution.

 The following environment variables are used:

- `RESOLUTION_BYTE`: The resolution of the sensor in bytes. Default: 8 (64 bit)
- `RESOLUTION_NUM`: Number of data points to generate. Default: 3 (X, Y, Z)
- `SAMPLING_RATE`: Sensor sampling rate in Hz. Default: 100
- `THRESHOLD_P`: Probability of a sensor reading being above the threshold.  Default: 0.15
