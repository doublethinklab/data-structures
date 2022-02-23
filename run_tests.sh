#!/bin/bash

docker run \
    --rm \
    -v ${PWD}:/data-structures \
    -w /data-structures \
        doublethinklab/data-structures:dev \
            python -m unittest discover
