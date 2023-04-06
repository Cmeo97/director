import os
import json
import pandas as pd
from plotnine import *
import numpy as np

logdir = "logdir"

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

        exp_metrics_dictionary = {}
        
        #iterate over experiments folders
        for exp_n, experiment_folder in enumerate(os.listdir(task_folder_path)):
            experiment_folder_path = os.path.join(task_folder_path, experiment_folder)
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
            for i in range(25):
                [metrics.append(key) for key in metrics_data[i].keys() if key not in metrics]
            
            for metric in metrics:
                if metric not in exp_metrics_dictionary.keys(): 
                    exp_metrics_dictionary[metric] = {'values':[[]], 'steps':[[]]}
                else:
                    exp_metrics_dictionary[metric]['values'].append([])
                    exp_metrics_dictionary[metric]['steps'].append([])

            for i, line in enumerate(metrics_data):
                for metric in line.keys():
                    exp_metrics_dictionary[metric]['values'][int(exp_n-1)].append(line[metric])  
                    exp_metrics_dictionary[metric]['steps'][int(exp_n-1)].append(line['step'])  
                    ## In this way I should have a dictionary with {'metric1':[value1_exp1, value2_exp1, etc..], 'metric2':[value_exp1, ...]}

        print('data collected for task:', task_folder)
        # create a folder for plots
        plot_folder_path = os.path.join(task_folder_path, 'plots')
        os.makedirs(plot_folder_path, exist_ok=True)

        exp_task_dictionary_mean = {}
        exp_task_dictionary_std = {}
        for metric in exp_metrics_dictionary.keys():
            if '/' in metric:
                metric_ = metric.replace('/', '-')
            else:
                metric_ = metric
            plot_file_path_png = os.path.join(plot_folder_path, metric_+'.png')
            plot_file_path_pdf = os.path.join(plot_folder_path, metric_+'.pdf')

            if os.path.isfile(plot_file_path_png):
                print(metric_+' plot already exists')
            else:
                if len(exp_metrics_dictionary[metric]['values']) > 1:
                    print(len(exp_metrics_dictionary[metric]['steps'][0]))
                    print(len(exp_metrics_dictionary[metric]['steps'][1]))
                    print(len(exp_metrics_dictionary[metric]['steps'][2]))
               
                    exp_task_dictionary_mean[metric] = np.mean(exp_metrics_dictionary[metric]['values'], 0)
                    print(exp_task_dictionary_mean[metric].shape)
                    exp_task_dictionary_std[metric] = np.std(exp_metrics_dictionary[metric]['values'], 0)
                    plot_df = pd.DataFrame({'step':np.array(exp_metrics_dictionary[metric]['steps'][0]), metric: exp_task_dictionary_mean[metric]})

                    p = (ggplot(plot_df, aes(x='step', y=metric)) + 
                         geom_line() +
                         geom_ribbon(aes(ymin=exp_task_dictionary_mean[metric]- exp_task_dictionary_std[metric], ymax= exp_task_dictionary_mean[metric]+ exp_task_dictionary_std[metric]), alpha=0.2) + 
                         labs(x='Step', y=metric, title=env_folder+'/'+task_folder+'/'+metric)
                        )
                else:
                    print(np.array(exp_metrics_dictionary[metric]['steps'])[0].shape)
                    print(np.array(exp_metrics_dictionary[metric]['values'])[0].shape)
                    if np.isnan(np.array(exp_metrics_dictionary[metric]['values'])[0]).any():
                        print(metric+" contains NaN values")
                        continue
                    if np.isinf(np.array(exp_metrics_dictionary[metric]['values'])[0]).any():
                        print(metric+" contains inf values")
                        continue
                    plot_df = pd.DataFrame({'step':np.array(exp_metrics_dictionary[metric]['steps'])[0], metric: np.array(exp_metrics_dictionary[metric]['values'])[0]})

                    p = (ggplot(plot_df, aes(x='step', y=metric)) + 
                         geom_line() +
                         labs(x='Step', y=metric, title=env_folder+'/'+task_folder+'/'+metric)
                        )

                    plot_file_path_pdf = os.path.join(plot_folder_path, metric_+'.pdf')

                ggsave(p, plot_file_path_png, dpi = 300)
                ggsave(p, plot_file_path_pdf,  dpi = 300)
                


