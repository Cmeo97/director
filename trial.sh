#!/bin/bash


declare -a All_Envs=(pinpad)

declare -a All_Tasks=(pinpad_six)

declare -a All_Ts=(2 4 8 16)

declare -a All_Seeds=(1 2 3)


for Env in "${All_Envs[@]}"
do
	for Task in "${All_Tasks[@]}"
	do
		for T in "${All_Ts[@]}"
		do
            target='/home/mila/c/cristian.meo/scratch/director/logdir/'${Env}'/'${Task}'/'${T}
            echo $target
            pushd "$target" > /dev/null
            for f in *
            do
                sbatch /home/mila/c/cristian.meo/HRL/director/example.sh $Env $Task $T $f   
              
            done
		done
	done
done 


