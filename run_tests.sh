#!/bin/bash

docker run \
    --rm \
    -v ${PWD}:/data-structures \
    -w /data-structures \
        python:3.9.5 \
            python -m unittest discover
