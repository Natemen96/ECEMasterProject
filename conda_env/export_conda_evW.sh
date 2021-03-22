#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate tf 
conda env export --no-build --name tf > tf_windows.yml