#!/bin/bash

for i in `seq 1 100`; do
  ./do-second.sh
  sleep 1
done
