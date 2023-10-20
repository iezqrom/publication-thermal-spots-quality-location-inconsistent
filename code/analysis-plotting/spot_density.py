# %%
import pandas as pd
import matplotlib.pyplot as plt
from globals import path, sessions, subjects, folder_spots_noboth, colours_types
import os

# %%
# Load density data
file_path_name = (
    f"{path}/forearm_area.csv"
)
if os.path.isfile(file_path_name):
    # open csv with headers in rows
    forearm_area = pd.read_csv(file_path_name, header=None)

# ignore first column
forearm_area = forearm_area.iloc[:, 1:]
forearm_area = forearm_area.to_dict(orient="list")
    
# %%
# Load spot data
spots_count = {}
spots_per_subject = {}
for index, subject in enumerate(subjects):
    for session in sessions:
        file_path_name = (
            f"{path}/spots_locations/{folder_spots_noboth}/S{subject}_{session}.csv"
        )
        if os.path.isfile(file_path_name) and os.path.getsize(file_path_name) > 0:
            # open csv file with pandas no header and deal with empty data error
            # check whether the file is empty
            temp_data = pd.read_csv(file_path_name, header=None)

            # count type column in temp_data
            for key in temp_data[2].value_counts().to_dict().keys():
                # check whether key is in spots_count
                if key in spots_count.keys():
                    spots_count[key] += temp_data[2].value_counts().to_dict()[key]
                else:
                    spots_count[key] = temp_data[2].value_counts().to_dict()[key]

            # add to spots_per_subject
            if subject in spots_per_subject.keys():
                for key in temp_data[2].value_counts().to_dict().keys():
                    # check whether key is in spots_count
                    if key in spots_per_subject[subject].keys():
                        spots_per_subject[subject][key] += (
                            temp_data[2].value_counts().to_dict()[key]
                        )
                    else:
                        spots_per_subject[subject][key] = (
                            temp_data[2].value_counts().to_dict()[key]
                        )
            else:
                spots_per_subject[subject] = temp_data[2].value_counts().to_dict()

# %%
# Calculate density
spots_density = {}
for index, subject in enumerate(spots_per_subject.keys()):
    spots_density[subject] = {}
    for type_spot in spots_per_subject[subject].keys():
        spots_density[subject][type_spot] = (
            round(spots_per_subject[subject][type_spot] / forearm_area[(index+1)][0], 4)
        )
# %%
# mean density by type
mean_density = {}
for type_spot in spots_count.keys():
    mean_density[type_spot] = []

for subject in spots_density.keys():
    for type_spot in spots_density[subject].keys():
        mean_density[type_spot].append(spots_density[subject][type_spot])

# mean density by type
for type_spot in mean_density.keys():
    mean_density[type_spot] = round(sum(mean_density[type_spot]) / len(mean_density[type_spot]), 4)

for type_spot in mean_density.keys():
    print(type_spot, mean_density[type_spot], 'spots per cm2')

# %%
