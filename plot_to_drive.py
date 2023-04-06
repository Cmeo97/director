from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
gauth = GoogleAuth()           
drive = GoogleDrive(gauth) 
import glob
import os



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

        print('data collected for task:', task_folder)
        # create a folder for plots
        plot_folder_path = os.path.join(task_folder_path, 'plots')
    

        plots = []
        for file in glob.glob("*.png"):
            plots.append(file)
        for file in glob.glob("*.pdf"):
            plots.append(file)
        
       
        for upload_file in plots:
        	gfile = drive.CreateFile({'parents': [{'id': '1pzschX3uMbxU0lB5WZ6IlEEeAUE8MZ-t'}]})
        	# Read file and set it as the content of this instance.
        	gfile.SetContentFile(upload_file)
        	gfile.Upload() # Upload the file.