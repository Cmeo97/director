#!/bin/bash


declare -a All_Envs=(pinpad)

declare -a All_Tasks=(pinpad_six)

declare -a All_Ts=(2 4 8 16)

for Env in "${All_Envs[@]}"
do
	for Task in "${All_Tasks[@]}"
	do
		for T in "${All_Ts[@]}"
		do
            target='/home/mila/c/cristian.meo/scratch/director/logdir/'${Env}'/'${Task}'/'${T}
            #echo $target
            pushd "$target" > /dev/null
            declare -a All_Files=(*)
            #echo ${All_Files[@]}
            workdir='/home/mila/c/cristian.meo/HRL/director'
            pushd "$workdir" > /dev/null
            for f in "${All_Files[@]}"
            do
                sbatch example.sh $Env $Task $T $f   
            done
		done
	done
done 





declare -a All_Envs=(pinpad)

declare -a All_Tasks=(pinpad_five)

declare -a All_Ts=(2 4 8 16)

for Env in "${All_Envs[@]}"
do
	for Task in "${All_Tasks[@]}"
	do
		for T in "${All_Ts[@]}"
		do
            target='/home/mila/c/cristian.meo/scratch/director/logdir/'${Env}'/'${Task}'/'${T}
            #echo $target
            pushd "$target" > /dev/null
            declare -a All_Files=(*)
            #echo ${All_Files[@]}
            workdir='/home/mila/c/cristian.meo/HRL/director'
            pushd "$workdir" > /dev/null
            for f in "${All_Files[@]}"
            do
                sbatch example.sh $Env $Task $T $f   
            done
		done
	done
done 



declare -a All_Envs=(loconav)

declare -a All_Tasks=(loconav_ant_maze_xl loconav_ant_maze_m)

declare -a All_Ts=(2 4 8 16)

for Env in "${All_Envs[@]}"
do
	for Task in "${All_Tasks[@]}"
	do
		for T in "${All_Ts[@]}"
		do
            target='/home/mila/c/cristian.meo/scratch/director/logdir/'${Env}'/'${Task}'/'${T}
            #echo $target
            pushd "$target" > /dev/null
            declare -a All_Files=(*)
            #echo ${All_Files[@]}
            workdir='/home/mila/c/cristian.meo/HRL/director'
            pushd "$workdir" > /dev/null
            for f in "${All_Files[@]}"
            do
                sbatch example.sh $Env $Task $T $f   
            done
		done
	done
done 


#declare -a All_Envs=(dmc_vision)
#
#declare -a All_Tasks=(dmc_walker_walk)
#
#declare -a All_Ts=(2 4 8 16)
#
#for Env in "${All_Envs[@]}"
#do
#	for Task in "${All_Tasks[@]}"
#	do
#		for T in "${All_Ts[@]}"
#		do
#            target='/home/mila/c/cristian.meo/scratch/director/logdir/'${Env}'/'${Task}'/'${T}
#            #echo $target
#            pushd "$target" > /dev/null
#            declare -a All_Files=(*)
#            #echo ${All_Files[@]}
#            workdir='/home/mila/c/cristian.meo/HRL/director'
#            pushd "$workdir" > /dev/null
#            for f in "${All_Files[@]}"
#            do
#                sbatch example.sh $Env $Task $T $f   
#            done
#		done
#	done
#done 
#