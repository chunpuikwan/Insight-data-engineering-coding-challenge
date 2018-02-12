#!/bin/bash

# Make sure the python files are executable
chmod a+x src/script.py

# Execute the following command from the root directory
python src/script.py input/itcont.txt input/percentile.txt output/repeat_donors.txt
