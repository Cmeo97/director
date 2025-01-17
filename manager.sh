




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
            for seed in "${All_Seeds[@]}"
            do
                sbatch example.sh $Env $Task $T $seed
            done
		done
	done
done 


declare -a All_Envs=(pinpad)

declare -a All_Tasks=(pinpad_five)

declare -a All_Ts=(2 4 8 16)

declare -a All_Seeds=(1 2 3)


for Env in "${All_Envs[@]}"
do
	for Task in "${All_Tasks[@]}"
	do
		for T in "${All_Ts[@]}"
		do
            for seed in "${All_Seeds[@]}"
            do
                sbatch example.sh $Env $Task $T $seed
            done
		done
	done
done 

declare -a All_Envs=(loconav)

declare -a All_Tasks=(loconav_ant_maze_xl loconav_ant_maze_m)

declare -a All_Ts=(4 8 16)

declare -a All_Seeds=(1 2 3)


for Env in "${All_Envs[@]}"
do
	for Task in "${All_Tasks[@]}"
	do
		for T in "${All_Ts[@]}"
		do
            for seed in "${All_Seeds[@]}"
            do
                sbatch example.sh $Env $Task $T $seed
            done
		done
	done
done 


declare -a All_Envs=(loconav)

declare -a All_Tasks=(loconav_ant_maze_xl loconav_ant_maze_m)

declare -a All_Ts=(2)

declare -a All_Seeds=(1 2)


for Env in "${All_Envs[@]}"
do
	for Task in "${All_Tasks[@]}"
	do
		for T in "${All_Ts[@]}"
		do
            for seed in "${All_Seeds[@]}"
            do
                sbatch example.sh $Env $Task $T $seed
            done
		done
	done
done 

#declare -a All_Envs=(dmc_vision)
#
#declare -a All_Tasks=(dmc_walker_walk)
#
#declare -a All_Ts=(4 8 16)
#
#declare -a All_Seeds=(1 2 3)
#
#
#for Env in "${All_Envs[@]}"
#do
#	for Task in "${All_Tasks[@]}"
#	do
#		for T in "${All_Ts[@]}"
#		do
#            for seed in "${All_Seeds[@]}"
#            do
#                sbatch example.sh $Env $Task $T $seed
#            done
#		done
#	done
#done 
#
#
#
#
#
#