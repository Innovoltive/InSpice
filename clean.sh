#!/bin/bash
rm *.erc
rm *.log
rm simulation.hdf5
rm pickled-simulation.data

find ./ -name '*.pyc' -delete

find examples/spice-library -name '*.yaml' -delete
find examples/spice-library -name '*.pickle' -delete
