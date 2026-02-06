#!/bin/bash
printf "\U$(printf '%08x' $((0x1F600 + RANDOM % 80)))\n"
