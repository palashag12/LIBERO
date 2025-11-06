import os
import yaml
import re
import glob
import h5py  # Optional: only needed if you plan to open HDF5 files

def modify_file_name(file_path):
    # Extract the directory and file name
    dir_name, file_name = os.path.split(file_path)

    # Remove all underscores and replace them with spaces
    #modified_name = file_name.replace('_', ' ')

    # Remove any characters before the occurrence of a number (including the digit itself)
    #modified_name = re.sub(r'^.*?\d+', '', file_name)

    # Join the directory and modified file name
  
    return file_name
# Specify the directory containing HDF5 files
directory = "/home/pa1077/LIBERO/libero/datasets/libero_object"

# Create file patterns for HDF5 files (both .h5 and .hdf5 extensions)
pattern_h5 = os.path.join(directory, "*.h5")
pattern_hdf5 = os.path.join(directory, "*.hdf5")

# Get a list of all HDF5 files in the directory
hdf5_files = glob.glob(pattern_h5) + glob.glob(pattern_hdf5)

# Iterate through the list of HDF5 files
for file_path in hdf5_files:
    print(f"Processing file: {file_path}")
    dataset_name = modify_file_name(file_path) + "_AGENTVIEW"
    datapath_train = os.path.join(os.path.splitext(file_path)[0], "AGENTVIEW")
    wandb_project = dataset_name
    hydra_job_name = dataset_name

    # Variable for the output YAML file path
    output_dir = "/home/pa1077/LIV/liv/cfgs/dataset/libero_object"  # Change this to your desired directory
    output_filename = dataset_name + ".yaml"
    output_path = os.path.join(output_dir, output_filename)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    data = {
        "dataset": dataset_name,
        "datapath_train": datapath_train,
        "hdf5_train_file": file_path,
        "wandbproject": wandb_project,
        "hydra": {
            "job": {
                "name": hydra_job_name
            }
        }
    }

    # Custom YAML dumper to preserve comments
    class MyDumper(yaml.Dumper):
        def increase_indent(self, flow=False, indentless=False):
            return super(MyDumper, self).increase_indent(flow, False)

    def yaml_represent_none(self, _):
        return self.represent_scalar('tag:yaml.org,2002:null', "# @package _global_")

    top_comment = "# @package _global_"

    yaml.add_representer(type(None), yaml_represent_none)
    yaml_content = yaml.dump(data, Dumper=MyDumper, default_flow_style=False, sort_keys=False)

    with open(output_path, "w") as file:
        file.write(top_comment + "\n" + yaml_content)

    dataset_name = modify_file_name(file_path) + "_WRIST"
    datapath_train = os.path.join(os.path.splitext(file_path)[0], "WRIST")
    wandb_project = dataset_name
    hydra_job_name = "train_liv_" + dataset_name

    # Variable for the output YAML file path
    output_dir = "/home/pa1077/LIV/liv/cfgs/dataset/libero_object"  # Change this to your desired directory
    output_filename = dataset_name + ".yaml"
    output_path = os.path.join(output_dir, output_filename)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    data = {
        
        "dataset": dataset_name,
        "datapath_train": datapath_train,
        "wandbproject": wandb_project,
        "hydra": {
            "job": {
                "name": hydra_job_name
            }
        }
    }
    top_comment = "# @package _global_"
    yaml.add_representer(type(None), yaml_represent_none)
    yaml_content = yaml.dump(data, Dumper=MyDumper, default_flow_style=False, sort_keys=False)

    with open(output_path, "w") as file:
        file.write(top_comment + "\n" + yaml_content)
    print(f"YAML file saved to: {output_path}")
 



    
