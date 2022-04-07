#!/bin/bash

rm -rf ../.env.example

while read line;
do
    IFS="="
    len=${#envs[@]}
    read -ra envs <<< "${line}"
    first_char=${envs[0]:0:1}
    if [ "$first_char" = "#" ]; then
        echo ${envs[0]} >> ../.env.example
    elif [ -z ${envs[0]} ]; then
        echo ${envs[0]} >> ../.env.example
    else
        echo ${envs[0]}"=" >> ../.env.example
    fi
done < ../.env
