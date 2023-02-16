# %%
import pandas as pd
from globals import subjects, path, sessions
import os

# load all_conserved_spots
all_conserved_spots = pd.read_csv(f"{path}/all_conserved_spots.csv")

# %% Master arm
path_to_save = f"../../data/spots_locations/per_participant"
for subject in subjects:
    spots = {}
    for session in sessions:
        file_path_name = f"{path}/spots_locations/aligned/S{subject}_{session}.csv"
        if os.path.isfile(file_path_name) and os.path.getsize(file_path_name) > 0:
            # open csv file with pandas no header and deal with empty data error
            # check whether the file is empty
            temp_data = pd.read_csv(file_path_name, header=None)
            for key in temp_data.to_dict().keys():
                if key in spots.keys():
                    spots[key].append(temp_data[key].to_list())
                else:
                    spots[key] = []
                    spots[key].append(temp_data[key].to_list())

    # remove nested list
    for key in spots.keys():
        spots[key] = [item for sublist in spots[key] for item in sublist]

    # save to csv
    df = pd.DataFrame(spots)
    df.to_csv(f"{path_to_save}/S{subject}.csv", index=False)

# %%
print(spots)
# get out of list

# %%
