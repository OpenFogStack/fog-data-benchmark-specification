/*
 * Sensor load generator.
 * This load generator takes a set of parameters from environment variables and
 * generates a sensor reading in a given interval. The sensor reading is written
 * to stdout. The sensor reading is converted to an unsigned integer in base16.
 * The threshold is always MAX_UINT/2, with MAX_UINT depending on the chosen
 * sensor resolution.
 *
 * The following environment variables are used:
 * - RESOLUTION_BYTE: The resolution of the sensor in bytes. Default: 8 (64 bit)
 * - RESOLUTION_NUM: Number of data points to generate. Default: 3
 * - SAMPLING_RATE: Sensor sampling rate in Hz. Default: 100
 * - THRESHOLD_P: Probability of a sensor reading being above the threshold.  Default: 0.15


 * Copyright (c) Tobias Pfandzelter. All rights reserved.
 * Licensed under the MIT license. See LICENSE file in the project root for details.
 */

package main

import (
	"fmt"
	"log"
	"math/rand"
	"os"
	"os/signal"
	"strconv"
	"syscall"
	"time"
)

func main() {
	// get all the parameters from environment variables
	// if not set, use default values

	resolution_byte := 8
	resolution_num := 3
	sampling_rate := 100
	threshold_p := 0.15

	if os.Getenv("RESOLUTION_BYTE") != "" {
		resolution_byte, _ = strconv.Atoi(os.Getenv("RESOLUTION_BYTE"))
	}
	if os.Getenv("RESOLUTION_NUM") != "" {
		resolution_num, _ = strconv.Atoi(os.Getenv("RESOLUTION_NUM"))
	}
	if os.Getenv("SAMPLING_RATE") != "" {
		sampling_rate, _ = strconv.Atoi(os.Getenv("SAMPLING_RATE"))
	}
	if os.Getenv("THRESHOLD_P") != "" {
		threshold_p, _ = strconv.ParseFloat(os.Getenv("THRESHOLD_P"), 64)
	}

	// set up signal handler
	// catch SIGINT and SIGTERM -> exit
	interrupt := make(chan os.Signal, 1)
	signal.Notify(interrupt, syscall.SIGINT, syscall.SIGTERM)

	// set up a ticker
	t := time.NewTicker(time.Second / time.Duration(sampling_rate))

	// forever:
	// generate a sensor reading and put it on stdout
	// catch SIGINT and SIGTERM -> exit
	for {
		select {
		case <-interrupt:
			os.Exit(0)
		case <-t.C:
			s := make([][]byte, resolution_num)
			for i := 0; i < resolution_num; i++ {
				// generate a sensor reading
				// generate RESOLUTION_BYTE random bytes
				s[i] = make([]byte, resolution_byte)
				_, err := rand.Read(s[i])
				if err != nil {
					log.Fatal(err)
				}
			}

			// set all MSB to 1 if the sensor reading is above the threshold
			if rand.Float64() < threshold_p {
				for i := 0; i < resolution_num; i++ {

					s[i][0] |= 0x80
					fmt.Print("1 ")
				}
			} else {
				for i := 0; i < resolution_num; i++ {
					s[i][0] &= 0x7f
					fmt.Print("0 ")
				}
			}

			// write sensor reading to stdout
			fmt.Printf("%d ", time.Now().UnixNano())
			// convert to base16
			for i := 0; i < resolution_num; i++ {
				fmt.Printf("%x ", s[i])
			}
			fmt.Println()
		}
	}
}
