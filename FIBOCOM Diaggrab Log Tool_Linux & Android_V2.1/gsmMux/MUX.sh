#!/bin/bash
read -p "please input ACM:"  ACM

read -p "you want ? MUX" a
if [ $a = 2 ] 
then
./gsmMuxd -p /dev/$ACM -b 115200 -s /dev/mux -w /dev/ptmx /dev/ptmx

elif [ $a = 3 ] 
then
  ./gsmMuxd -p /dev/$ACM -b 115200 -s /dev/mux -w /dev/ptmx /dev/ptmx /dev/ptmx

elif [ $a = 4 ] 
then
  ./gsmMuxd -p /dev/$ACM -b 115200 -s /dev/mux -w /dev/ptmx /dev/ptmx /dev/ptmx /dev/ptmx

else 
    echo -e "you are wrong"

fi
