# Get the parent directory of the current script to import objects from source folder
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

data_dir = os.path.join(parent_dir, r'instrumentacion_low_temperature\data')

# Define the new folder you want to create inside the 'data' directory
new_folder_name = 'new_subfolder'  # Change this to your desired folder name
new_folder_path = os.path.join(data_dir, new_folder_name)

# Create the folder (including intermediate directories if they don't exist)
os.makedirs(new_folder_path, exist_ok=True)

print(f"Created folder: {new_folder_path}")