#!/bin/bash


conda activate py39-tf211
export CONDA_PREFIX=/users/cristianmeo/conda/envs/py39-tf211/bin
export XLA_FLAGS=--xla_gpu_cuda_data_dir=$CONDA_PREFIX
echo $CONDA_PREFIX
echo $XLA_FLAGS
#source  ~/.venvs/${conda_env}/bin/activate

env=$1
task=$2
f=$3

echo 'Training director with env: '${env}', task: '${task}' f: '${f}

CUDA_VISIBLE_DEVICES=4 nohup python embodied/agents/director/train.py \
  --logdir /space/cristianmeo/director/logdir/${env}/${task}/${f} \
  --configs ${env} \
  --task ${task} \
> logs/director_training_"${task}""-"$(date +%Y%m%d-%H%M%S).out 2> logs/director_training_"${task}""-"$(date +%Y%m%d-%H%M%S).err 
