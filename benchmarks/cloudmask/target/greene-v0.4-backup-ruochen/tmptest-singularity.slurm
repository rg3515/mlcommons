#!/bin/bash

#SBATCH --job-name=cloudmask-gpu-greene-epoch-test1
#SBATCH --nodes=1
#SBATCH --gres=gpu:v100:1
#SBATCH --time=00:30:00
#SBATCH --mem=64G
#SBATCH -o outputs/%u-%j.out
#SBATCH -e outputs/%u-%j.err

export USER_SCRATCH=/scratch/$USER/github-fork
export PROJECT_DIR=$USER_SCRATCH/mlcommons/benchmarks/cloudmask
export PYTHON_DIR=$USER_SCRATCH/ENV3
export PROJECT_DATA=/scratch/$USER/data


nvidia-smi
cms gpu watch --gpu=0 --delay=0.5 --dense > outputs/gpu0.log &

#    /scratch/work/public/singularity/cuda11.8.86-cudnn8.7-devel-ubuntu22.04.2.sif \


singularity exec --nv \
    --overlay $PROJECT_DIR/target/greene_v0.5/tmptest-overlay-image:ro \
    $PROJECT_DIR/target/greene_v0.5/cloudmask.sif \
    /bin/bash \
    -c "source /ext3/env.sh; \
    source $PYTHON_DIR/bin/activate; \
    cd $PROJECT_DIR/target/greene_v0.5; \
    python slstr_cloud.py --config config_simple.yaml"

seff $SLURM_JOB_ID
