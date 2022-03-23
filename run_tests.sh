#!/bin/bash

docker run \
    --rm \
    -v ${PWD}:/data-structures \
    -w /data-structures \
    -e TEST=1 \
        doublethinklab/data-structures:dev \
            python -m unittest discover
