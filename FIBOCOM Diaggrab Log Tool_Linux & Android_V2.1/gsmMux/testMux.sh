#!/bin/sh
./gsmMuxd -p /dev/ttyUSB0 -b 115200 -s /dev/mux -w /dev/ptmx  /dev/ptmx  -d
