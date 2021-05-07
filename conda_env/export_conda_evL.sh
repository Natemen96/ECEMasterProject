#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate data_gen 
# conda env export --no-build --name tf > conda_env/rl_linux.yml
conda env export --name data_gen -f conda_env/rl_window.yml --from-history