import h5py
import os
import shutil

def clone_hdf5_files(directory):
    """
    Clones all HDF5 files in a directory, placing copies in the same directory
    with "_copy" appended to the original filenames.

    Args:
        directory (str): The path to the directory containing HDF5 files.
    """
    for filename in os.listdir(directory):
        if filename.endswith(".h5") or filename.endswith(".hdf5"):
            source_path = os.path.join(directory, filename)
            base_name, ext = os.path.splitext(filename)
            destination_path = os.path.join(directory, f"{base_name}_copy{ext}")
            shutil.copy2(source_path, destination_path)

if __name__ == "__main__":
    target_directory = "/home/pa1077/LIBERO/libero/datasets/libero_object"  # Current directory, change if needed
    clone_hdf5_files(target_directory)