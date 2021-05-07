#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate data_gen 
conda env export --name data_gen -f conda_env/rl_window.yml --no-build