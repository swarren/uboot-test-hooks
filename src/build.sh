#!/bin/sh

gcc -o phidgets-relay \
    -I "${HOME}/phidgets/include" \
    phidgets-relay.c \
    -L "${HOME}/phidgets/lib" -lphidget21 \
    -lusb-1.0 -lpthread -ldl -lm
