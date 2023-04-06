#!/bin/bash

#SBATCH --job-name=director_example
#SBATCH --partition=long                        
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:rtx8000:2
#SBATCH --mem=120G                                     


#conda_env=${1}

# 1. Load the required modules
module load anaconda/3
#module load cuda/11.0/cudnn/8.0  
#module load tensorflow
conda activate ~/.conda/envs/mamba/envs/py39-tf211
export CONDA_PREFIX=/home/mila/c/cristian.meo/.conda/envs/mamba/envs/py39-tf211/bin
export XLA_FLAGS=--xla_gpu_cuda_data_dir=$CONDA_PREFIX
echo $CONDA_PREFIX
echo $XLA_FLAGS
#source  ~/.venvs/${conda_env}/bin/activate

env=$1
task=$2
T=$3
f=$4

python embodied/agents/director/train.py \
  --logdir ~/scratch/director/logdir/${env}/${task}/${T}/${f} \
  --env_skill_duration ${T} \
  --train_skill_duration ${T} \
  --configs ${env} \
  --task ${task} \
> logs/director_training_"${task}""-"$(date +%Y%m%d-%H%M%S).out 2> logs/director_training_"${task}""-"$(date +%Y%m%d-%H%M%S).err 
