# %%
import numpy as np
import os
import pandas as pd
import itertools
from globals import threshold_distance

path = "/Users/ivan/Documents/aaa_online_stuff/coding/python/phd/expt17_spots/data"

sessions = range(1, 5)
subjects = [3, 4, 6, 7, 8, 9, 10, 11]


def euclidean_distance(x, y):
    return np.sqrt(np.sum((x - y) ** 2))


# %%
spots_locations_path = path + "/spots_locations"
images_path = path + "/arm_images"
analysis_instances = ["original", "aligned"]

# create a pandas dataframe to store the original vs aligned data
all_raw_aligned = pd.DataFrame(
    columns=[
        "session",
        "subject",
        "x_coord_original",
        "y_coord_original",
        "x_coord_aligned",
        "y_coord_aligned",
        "x_coord_difference",
        "y_coord_difference",
        "x_coord_corrected",
        "y_coord_corrected",
        "type",
    ]
)

for subject in subjects:
    for session in sessions:
        print("Subject: ", subject, "Session: ", session)
        datasets = {}
        temp_data_frame = []
        spot_types = {}
        for analysis_instance in analysis_instances:
            file_path_name = (
                f"{path}/spots_locations/{analysis_instance}/S{subject}_{session}.csv"
            )
            if os.path.isfile(file_path_name) and os.path.getsize(file_path_name) > 0:
                # open csv file with pandas no header and deal with empty data error
                # check whether the file is empty
                temp_data = pd.read_csv(file_path_name, header=None)
                print(temp_data)
                datasets[f"x_coord_{analysis_instance}"] = temp_data[0]
                datasets[f"y_coord_{analysis_instance}"] = temp_data[1]
                spot_types[f"{analysis_instance}"] = temp_data[2]
                # change column names

        # check whether spots types is empty
        if spot_types:
            if spot_types["original"].equals(spot_types["aligned"]):
                # add session, subject and analysis_instance columns
                datasets["session"] = np.repeat(
                    session, len(datasets["x_coord_original"])
                )
                datasets["subject"] = np.repeat(
                    subject, len(datasets["x_coord_original"])
                )
                datasets["type"] = temp_data[2]
                datasets["x_coord_difference"] = (
                    datasets["x_coord_original"] - datasets["x_coord_aligned"]
                )
                datasets["y_coord_difference"] = (
                    datasets["y_coord_original"] - datasets["y_coord_aligned"]
                )

                datasets["x_coord_corrected"] = (
                    datasets["x_coord_difference"] + datasets["x_coord_aligned"]
                )
                datasets["y_coord_corrected"] = (
                    datasets["y_coord_difference"] + datasets["y_coord_aligned"]
                )

                # append datasets to all_diff
                temp_data_frame = pd.DataFrame(datasets)
                all_raw_aligned = pd.concat(
                    [all_raw_aligned, temp_data_frame], ignore_index=True
                )
            else:
                print(
                    f"Spot numbers aligned vs conserved are not the same. Subject: {subject}, Session: {session}"
                )
        elif not spot_types:
            print("Original and aligned are empty")

# # save the dataframe to a csv file
all_raw_aligned.to_csv(f"{path}/all_raw_aligned.csv", index=False)


# %%
# subtract the aligned from the original column 1 and column 2 with pandas
# compare spot_types["original"]  and spot_types["aligned"]
total_spots_conserved = 0
conserved_spots = {}
threshold_distance = 6
# create a pandas dataframe to store the conserved spots
all_conserved_spots = pd.DataFrame(
    columns=[
        "session",
        "subject",
        "x_coord_original",
        "y_coord_original",
        "x_coord_aligned",
        "y_coord_aligned",
        "x_coord_difference",
        "y_coord_difference",
        "x_coord_corrected",
        "y_coord_corrected",
        "type",
    ]
)
for subject in subjects:
    # subject = 7
    conserved_spots[subject] = []
    temp_df = all_raw_aligned[(all_raw_aligned["subject"] == subject)]

    temp_sessions = {}
    for session in sessions:
        temp_sessions[session] = temp_df[temp_df["session"] == session]

    combinations = list(itertools.combinations(sessions, 2))
    for combination in combinations:
        # print(combination)
        temp_sesh1 = temp_sessions[combination[0]][
            ["x_coord_aligned", "y_coord_aligned"]
        ].to_numpy()  # print(temp_sessions[combination[0]])
        temp_sesh2 = temp_sessions[combination[1]][
            ["x_coord_aligned", "y_coord_aligned"]
        ].to_numpy()  # print(temp_sessions[combination[1]])
        for index, spot in enumerate(temp_sesh1):
            mat_tr = np.int64(temp_sesh2 - spot)
            mat = np.linalg.norm(mat_tr, axis=1)
            # remove index from mat
            if len(mat[(mat < threshold_distance) & (mat > 0)]) > 0:
                temp_sesh1_type = temp_sessions[combination[0]].iloc[index]["type"]
                temp_sesh2_type = temp_sessions[combination[1]][
                    (mat < threshold_distance) & (mat > 0)
                ]["type"]
                print(
                    f"Subject: {subject}",
                    f"Distance : {round(mat[(mat < threshold_distance) & (mat > 0)][0], 2)} //",
                    f"Type {temp_sesh1_type} session {combination[0]} //",
                    f"Type {temp_sesh2_type.values[0]} session {combination[1]}",
                )

                # get index of boolean array
                index_sesh2 = np.where((mat < threshold_distance) & (mat > 0))[0][0]
                print(temp_sessions[combination[0]].iloc[index])
                conserved_spots[subject].append(
                    (
                        temp_sessions[combination[0]].iloc[index : index + 1],
                        temp_sessions[combination[1]].iloc[
                            index_sesh2 : index_sesh2 + 1
                        ],
                    )
                )
                total_spots_conserved += 1

                # save temp_sessions[combination[0]].iloc[index] to a pandas dataframe
                all_conserved_spots = pd.concat(
                    [
                        all_conserved_spots,
                        temp_sessions[combination[0]].iloc[index : index + 1],
                    ],
                    ignore_index=True,
                )
                all_conserved_spots = pd.concat(
                    [
                        all_conserved_spots,
                        temp_sessions[combination[1]].iloc[
                            index_sesh2 : index_sesh2 + 1
                        ],
                    ],
                    ignore_index=True,
                )

# %%
# save the dataframe to a csv file
print(all_conserved_spots)
all_conserved_spots.to_csv(f"{path}/all_conserved_spots.csv", index=False)

# %%
# get spots where type is cold
# get unique values type column all_raw_aligned
type_spots = all_raw_aligned["type"].unique()

for type in type_spots:
    all_raw_aligned_type = all_raw_aligned[all_raw_aligned["type"] == type]
    print(f"{type}: {len(all_raw_aligned_type)}")


# %%
all_raw_aligned_type
# %%
# legacy code
#     for index, session_pair in enumerate(zip(sessions, sessions[1:])):
#         conservation_sessions = []
#         if index % 2 == 0:
#             conserved_spots[subject][f"{session_pair[0]}_{session_pair[1]}"] = []
#             conservation_sessions.append(all_raw_aligned[(all_raw_aligned["subject"] == subject) & (all_raw_aligned["session"] == session_pair[0])])
#             conservation_sessions.append(all_raw_aligned[(all_raw_aligned["subject"] == subject) & (all_raw_aligned["session"] == session_pair[1])])

#     # print(conservation_sessions)
#     n_spots = [len(sesh) for sesh in conservation_sessions]
#     # print(n_spots)
#     # add n_spots
#     max_responses = max(n_spots)
#     max_responses_index = n_spots.index(max_responses)
#     min_responses = min(n_spots)
#     min_responses_index = n_spots.index(min_responses)

#     spots_sesh_most = conservation_sessions[max_responses_index][['x_coord_corrected', 'y_coord_corrected']]
#     spots_sesh_most = spots_sesh_most.to_numpy()
#     spots_sesh_least = conservation_sessions[min_responses_index][['x_coord_corrected', 'y_coord_corrected']]
#     spots_sesh_least = spots_sesh_least.to_numpy()

#     # find the closest spot in the session with the most spots
#     for spot in spots_sesh_least:
#         mat_tr = np.int64(spots_sesh_most - spot)
#         mat = np.linalg.norm(mat_tr, axis=1)
#         # check whether any values are less than 10
#         if np.any(mat < threshold_distance):
#             # get the index of the spot
#             index = np.where(mat < threshold_distance)[0][0]
#             # get the spot
#             conserved_spot = spots_sesh_most[index]
#             print(index)
#             print(conservation_sessions[max_responses_index].iloc[index])
#             print(conserved_spot)
#             # add the spot to the dictionary
#             conserved_spots[subject][f"{session_pair[0]}_{session_pair[1]}"].append(conserved_spot)
#         # conserved_spots[subject][f"{session_pair[0]}_{session_pair[1]}"].append(mat)


# %%
