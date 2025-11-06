import h5py
import numpy as np
import os 
import imageio 
import re
import pandas as pd
def modify_file_name(file_path):
    # Extract the directory and file name
    dir_name, file_name = os.path.split(file_path)

    # Remove all underscores and replace them with spaces
    modified_name = file_name.replace('_', ' ')

    # Remove any characters before the occurrence of a number (including the digit itself)
    modified_name = re.sub(r'^.*?\d+', '', modified_name)

    # Join the directory and modified file name
  
    return modified_name
directory = '/home/pa1077/LIBERO/libero/datasets/libero_object'
for root, _, files in os.walk(directory):
        for file in files:
            
            if file.endswith(".h5") or file.endswith(".hdf5"):
                print(f"Processing {file}")
                dataset_path = os.path.join(root, file)
                f = h5py.File(dataset_path, "r")
                demos = list(f["data"].keys())
                len(demos)
                lengths=[]
                for demo_name in demos:
                    demo=f['data'][demo_name]
                    num_samples=demo.attrs['num_samples']
                    # num_samples = demo['actions'][:].shape[0]
                    lengths.append(num_samples)

                lengths=np.array(lengths)

                print('Number of demos: ', len(demos))
                print('Max length: ', np.max(lengths))
                print('Min length: ', np.min(lengths))
                print('Mean length: ', np.mean(lengths))
                f.keys()
                f['data']['demo_0'].keys()

                for key in f['data']['demo_0']['obs'].keys():
                    print(key, f['data']['demo_0']['obs'][key].shape)


                import cv2

                from PIL import Image
                dirname = os.path.splitext(dataset_path)[0]
                dirname_b= os.path.splitext(dataset_path)[0]
                savepath = os.path.join(dirname, "AGENTVIEW")
                savepath_b = os.path.join(dirname_b, "WRIST")
                os.makedirs(savepath, exist_ok=True)
                os.makedirs(savepath_b, exist_ok=True)
                manifest = {"index": [], "directory": [], "num_frames": [], "text": []}
                manifest_b = {"index": [], "directory": [], "num_frames": [], "text": []}

                
                for i, demo_name in enumerate(demos):
                    print(f"processing {demo_name} {i+1}/{len(demos)}")
                    demo=f['data'][demo_name]
                    images=demo['obs']['agentview_rgb']
                    images_wrist=demo['obs']['eye_in_hand_rgb']
                    #images=np.concatenate([images, images_wrist], axis=2)
                    savepath_c = os.path.join(savepath, demo_name)
                    os.mkdir(savepath_c)
                    savepath_d = os.path.join(savepath_b, demo_name)
                    os.mkdir(savepath_d)

                    #video_writer = imageio.get_writer(f"{savepath}/{demo_name}.mp4", fps=20)
                    for j in range(len(images)):
                        #print(j)
                        img = Image.fromarray(images[j])
                        img.save(savepath_c + '/' + f"{j}.png")
                        img_b = Image.fromarray(images_wrist[j])
                        img_b.save(savepath_d + '/' + f"{j}.png")
                    #video_writer.close()
                    manifest["index"].append(i)
                    manifest["directory"].append(savepath_c)
                    manifest["num_frames"].append(len(images))
                    manifest["text"].append(modify_file_name(dirname))
                    manifest_b["index"].append(i)
                    manifest_b["directory"].append(savepath_d)
                    manifest_b["num_frames"].append(len(images))
                    manifest_b["text"].append(modify_file_name(dirname_b))
                manifest = pd.DataFrame(manifest)
                manifest.to_csv(f"{savepath}/manifest.csv")
                manifest_b = pd.DataFrame(manifest_b)
                manifest_b.to_csv(f"{savepath_b}/manifest.csv")

                f.close()    

