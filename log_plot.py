import os
import json
import pandas as pd
from plotnine import *
import numpy as np
from scipy.ndimage import gaussian_filter1d as gaussian
from scipy.signal import convolve
logdir = "/home/mila/c/cristian.meo/scratch/director/logdir"



def smooth(x,window_len=20,window='hanning'):

 
    s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y




def compute_mean_std(data):
    len_max = 0
    for i in range(len(data)):
        len_ = len(data[i])
        if len_ > len_max:
            len_max = len_
            i_max = i

    data_ = []
    longest_data = np.array(data[i_max]).reshape(-1, 1)
    for i in range(len(data)):
        if len(data[i]) == 0:
            continue
        else:
            data_.append(data[i])
    processed_data = data_
    _data = longest_data
    
    for i in range(len(processed_data)):
        if len(processed_data[i]) < len_max:
            _data = np.concatenate((_data, np.concatenate((np.array(processed_data[i]), _data[len(processed_data[i]):, 0]), 0).reshape(-1, 1)), axis=1)
            
    mean = np.mean(_data, 1)
    std = np.std(_data, 1)
    return mean, std, i_max






# iterate over envs folders
for env_folder in os.listdir(logdir):
    env_folder_path = os.path.join(logdir, env_folder)
    if not os.path.isdir(env_folder_path):
        continue

    # iterate over tasks folders
    for task_folder in os.listdir(env_folder_path):
        task_folder_path = os.path.join(env_folder_path, task_folder)
        if not os.path.isdir(task_folder_path):
            continue

        exp_T_metrics_dictionary = {}

        #iterate over experiments folders
        
        for T in ['2', '4', '8', '16']: #os.listdir(task_folder_path):
            experiment_T_folder_path = os.path.join(task_folder_path, T)
            if not os.path.isdir(experiment_T_folder_path):
                continue
            if T == 'plots':
                continue
            exp_metrics_dictionary = {}
            #iterate over experiments folders
            for exp_n, experiment_folder in enumerate(os.listdir(experiment_T_folder_path)):
                experiment_folder_path = os.path.join(experiment_T_folder_path, experiment_folder)
                if not os.path.isdir(experiment_folder_path):
                    continue

                # iterate over metrics for the first experiment to check if they are present in the other experiments
                metrics_file_path = os.path.join(experiment_folder_path, 'metrics.jsonl')
                if not os.path.isfile(metrics_file_path):
                    continue
                with open(metrics_file_path) as f:
                    metrics_data = f.readlines()
                metrics_data = [json.loads(line) for line in metrics_data] 
                metrics = []
                #for i in range(25):
                #    [metrics.append(key) for key in metrics_data[i].keys() if key not in metrics]
                
                for metric in ['episode/score']: #metrics:
                    if metric not in exp_metrics_dictionary.keys(): 
                        exp_metrics_dictionary[metric] = {'values':[[]], 'steps':[[]]}
                    else:
                        exp_metrics_dictionary[metric]['values'].append([])
                        exp_metrics_dictionary[metric]['steps'].append([])

                for i, line in enumerate(metrics_data):
                    for metric in line.keys():
                        if metric == 'episode/score':
                            exp_metrics_dictionary[metric]['values'][int(exp_n)].append(line[metric])  
                            exp_metrics_dictionary[metric]['steps'][int(exp_n)].append(line['step']) 
            max_steps = 0 
            for i in range(len(exp_metrics_dictionary['episode/score']['steps'])):
                steps = np.array(exp_metrics_dictionary['episode/score']['steps'][i][-1])
                if steps > max_steps:
                    max_steps = steps
                    #print('max_steps:', max_steps)

                #print('data collected for experiment:', experiment_folder, 'T:', T)
                #print(exp_metrics_dictionary['episode/score']['steps'][int(exp_n)][-1])
                  ## In this way I should have a dictionary with {'metric1':[value1_exp1, value2_exp1, etc..], 'metric2':[value_exp1, ...]}
            mean, std, i_max = compute_mean_std(exp_metrics_dictionary['episode/score']['values'])
            mean_ = np.concatenate((np.array([0]), mean), 0)
            std_ = np.concatenate((np.array([0]), std), 0)
            exp_T_metrics_dictionary[str(T)] = {'mean_return':mean_, 'std':std_, 'steps': (np.arange(mean.shape[0]+1)/(mean.shape[0]+1)*max_steps).astype(np.int32)}

            


        print('data collected for task:', task_folder)
        # create a folder for plots
        plot_folder_path = os.path.join(task_folder_path, 'plots')
        os.makedirs(plot_folder_path, exist_ok=True)

        for metric in ['episode/score']:  #exp_metrics_dictionary.keys():
            if '/' in metric:
                metric_ = metric.replace('/', '-')
            else:
                metric_ = metric
            plot_file_path_png = os.path.join(plot_folder_path, metric_+'.png')
            plot_file_path_pdf = os.path.join(plot_folder_path, metric_+'.pdf')            
           
            if  len(exp_T_metrics_dictionary) > 1:
                means = []
                stds = []
                steps = []
                for T in  ['2', '4', '8', '16']:
                    means.append(smooth(exp_T_metrics_dictionary[T]['mean_return']))
                    stds.append(smooth(exp_T_metrics_dictionary[T]['std']))
                    steps.append(smooth(exp_T_metrics_dictionary[T]['steps']))

                data = pd.DataFrame({'steps': np.concatenate([np.arange(means[i].shape[0])/means[i].shape[0]*steps[i] for i in range(len(means))]),
                    'mean_return': np.concatenate(means),
                    'T': pd.Categorical(np.repeat(np.array([2,4,8,16]), [means[i].shape[0] for i in range(len(means))])),
                    'std': np.concatenate(stds)})

                ## Create the plot using plotnine
                plot = (ggplot(data, aes(x='steps', y='mean_return', group='T'))
                        + geom_line(aes(color='T'), size=1)
                        + geom_ribbon(aes(ymin='mean_return-std', ymax='mean_return+std', fill='T'), alpha=0.3)
                        + labs(title=f'{env_folder}_{task_folder}_Returns', x='Steps', y='Mean Return')
                        + theme_bw()
                        + theme(axis_text=element_text(size=12),  # Adjust font size of axis labels
                                axis_ticks=element_line(size=1),
                                axis_title=element_text(size=14), 
                                plot_title=element_text(size=16, weight='bold'))
                        )

                ggsave(plot, plot_file_path_png, dpi = 300)
                ggsave(plot, plot_file_path_pdf,  dpi = 300)


            #else:
            #    print(np.array(exp_metrics_dictionary[metric]['steps'])[0].shape)
            #    print(np.array(exp_metrics_dictionary[metric]['values'])[0].shape)
            #    if np.isnan(np.array(exp_metrics_dictionary[metric]['values'])[0]).any():
            #        print(metric+" contains NaN values")
            #        continue
            #    if np.isinf(np.array(exp_metrics_dictionary[metric]['values'])[0]).any():
            #        print(metric+" contains inf values")
            #        continue
            #    plot_df = pd.DataFrame({'step':np.array(exp_metrics_dictionary[metric]['steps'])[0], metric: np.array(exp_metrics_dictionary[metric]['values'])[0]})
#
            #    p = (ggplot(plot_df, aes(x='step', y=metric)) + 
            #         geom_line() +
            #         labs(x='Step', y=metric, title=env_folder+'/'+task_folder+'/'+metric)
                #        )
#
                #    plot_file_path_pdf = os.path.join(plot_folder_path, metric_+'.pdf')

                #ggsave(p, plot_file_path_png, dpi = 300)
                #ggsave(p, plot_file_path_pdf,  dpi = 300)
                


