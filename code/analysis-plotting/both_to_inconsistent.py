# %%
import pandas as pd
from globals import path, sessions, subjects, folder_spots_noboth
import os

path_to_save = f"../../data/spots_locations/{folder_spots_noboth}"
# %%
# Load data

for index, subject in enumerate(subjects):
    for session in sessions:
        spots = {}
        for key in [0, 1, 2]:
            spots[key] = []
        file_path_name = f"{path}/spots_locations/aligned/S{subject}_{session}.csv"
        if os.path.isfile(file_path_name) and os.path.getsize(file_path_name) > 0:
            # open csv file with pandas no header and deal with empty data error
            # check whether the file is empty
            temp_data = pd.read_csv(file_path_name, header=None)

            for i, row in temp_data.iterrows():
                for key in row.keys():
                    # print(row[key])
                    if row[key] == "both":
                        print("HERE")
                        value = "inconsistent"
                    else:
                        value = row[key]
                    spots[key].append(value)

            # print(temp_data)

        # print(session)
        # save to csv
        df = pd.DataFrame(spots)
        df.to_csv(f"{path_to_save}/S{subject}_{session}.csv", index=False, header=None)


# %%
