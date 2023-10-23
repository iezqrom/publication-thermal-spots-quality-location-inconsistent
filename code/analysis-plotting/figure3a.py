# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
from globals import path, sessions, subjects, folder_spots_noboth, colours_types

ss = 25
transparency = 0.9

figure_paper_number = "3a"
# %% get data from txt file
file_adtest_path = f"{path}/adtest.txt"
adtest_df = pd.read_csv(file_adtest_path, sep=",", header=None)

ads_p = {}
for index, subject in enumerate(subjects):
    ads_p[subject] = {}
    print(adtest_df.iloc[index, 1])
    ads_p[subject]["ad"] = round(adtest_df.iloc[index, 2], 2)

print(ads_p)

# %%

ads_p[3]["p"] = 0.060
ads_p[4]["p"] = 0.150
ads_p[6]["p"] = 0.001
ads_p[7]["p"] = 0.007
ads_p[8]["p"] = 0.056
ads_p[9]["p"] = 0.0001
ads_p[10]["p"] = "n/a"
ads_p[10]["ad"] = "n/a"
ads_p[11]["p"] = 0.077

# sessions = df['session_number'].unique()
# %% ############################################################################################################
########## All subjects except for 7 #########################################################################################
############################################################################################################
visualisation_correction = {pp: [] for pp in subjects}
visualisation_correction[3] = [0, 20]
visualisation_correction[4] = [40, 35]

visualisation_correction[6] = [10, 20]
visualisation_correction[7] = [0, 175]
visualisation_correction[8] = [0, -25]
visualisation_correction[9] = [0, 50]
visualisation_correction[10] = [0, -5]
visualisation_correction[11] = [0, 65]

image = cv2.imread(f"../../data/arm_images/aligned/S3_1.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

edges = cv2.Canny(gray, threshold1=50, threshold2=125)
# colour edeges light blue
edges[0:100, 250:] = 0
edges[0:20, 140:] = 0
edges[185:295, 200:] = 0
edges[360:, :] = 0

edges[90:142, 490:] = 0

edges[305:580, 50:120] = 0

edges[0:100, 0:50] = 0

edges[100:165, 670:750] = 0
edges[100:173, 800:900] = 0

edges[340:, 300:380] = 0
edges[350:, 500:580] = 0
edges[330:, 800:900] = 0
edges[335:, 680:790] = 0

for index, subject in enumerate(subjects):
    if subject != 7:
        fig, ax = plt.subplots(figsize=(15, 10))

        ax.imshow(edges, vmin=0, vmax=400, cmap="Greys")
        ax.invert_xaxis()

        for session in sessions:
            print("Subject: ", subject, "Session: ", session)
            datasets = {}
            # for analysis_instance in analysis_instances:
            file_path_name = (
                f"{path}/spots_locations/{folder_spots_noboth}/S{subject}_{session}.csv"
            )
            if os.path.isfile(file_path_name) and os.path.getsize(file_path_name) > 0:
                # open csv file with pandas no header and deal with empty data error
                # check whether the file is empty
                temp_data = pd.read_csv(file_path_name, header=None)
                # print(temp_data)
                for i, row in temp_data.iterrows():
                    type_spot = row[2]

                    x_coordinate = row[0]
                    y_coordinate = row[1]
                    type_spot = row[2]
                    ax.scatter(
                        (x_coordinate + visualisation_correction[subject][0]),
                        (y_coordinate + visualisation_correction[subject][1]),
                        s=ss,
                        alpha=transparency,
                        color=colours_types[type_spot],
                        label=f"Session {str(session)}",
                    )

        ax.tick_params(axis="both", which="both", length=0)
        # remove numbers on x and y axis but keep frame
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)

        # print(pp)
        if ads_p[subject]["p"] == 0.0001:
            p_sign = "<"
        else:
            p_sign = "="
        ax.text(
            180,
            400,
            "AD = "
            + str(ads_p[subject]["ad"])
            + f"\np {p_sign} "
            + str(ads_p[subject]["p"]),
            fontsize=20,
            color="black",
        )
        ax.text(1180, 30, f"P{index + 1}", fontsize=20, color="black")
        ax.set_ylim(ymin=420, ymax=0)

        plt.savefig(
            f"../../figures/figure{figure_paper_number}/edges/figure{figure_paper_number}_subject{subject}.svg",
            bbox_inches="tight",
            transparent=True,
        )

# %% ############################################################################################################
########## Subject 7 #########################################################################################
############################################################################################################
image = cv2.imread(f"../../data/arm_images/aligned/S3_1.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

edges = cv2.Canny(gray, threshold1=50, threshold2=125)
# zoom_factor = 1
edges_zoomed = cv2.resize(edges, None, fx=1, fy=1.5)
edges_zoomed[0:20, 140:] = 0
edges_zoomed[0:100, 800:] = 0
edges_zoomed[155:220, 520:] = 0
edges_zoomed[550:, :] = 0
edges_zoomed[0:100, 0:100] = 0
edges_zoomed[190:210, 480:550] = 0
edges_zoomed[200:260, 800:900] = 0
# edges_zoomed[0:100, 0:50] = 0

edges_zoomed[200:240, 680:750] = 0
edges_zoomed[300:450, 400:1000] = 0

edges_zoomed[500:, 300:380] = 0
edges_zoomed[510:, 500:580] = 0
edges_zoomed[490:, 800:900] = 0
edges_zoomed[500:, 680:790] = 0
edges_zoomed[455:, 50:120] = 0

subject = 7
fig, ax = plt.subplots(figsize=(15, 10))

ax.imshow(edges_zoomed, vmin=0, vmax=400, cmap="Greys")
ax.invert_xaxis()

for session in sessions:
    print("Subject: ", subject, "Session: ", session)
    datasets = {}
    # for analysis_instance in analysis_instances:
    file_path_name = (
        f"{path}/spots_locations/{folder_spots_noboth}/S{subject}_{session}.csv"
    )

    if os.path.isfile(file_path_name) and os.path.getsize(file_path_name) > 0:
        # open csv file with pandas no header and deal with empty data error
        # check whether the file is empty
        temp_data = pd.read_csv(file_path_name, header=None)
        # print(temp_data)
        for i, row in temp_data.iterrows():
            type_spot = row[2]

            x_coordinate = row[0]
            y_coordinate = row[1]
            ax.scatter(
                (x_coordinate + visualisation_correction[subject][0]),
                (y_coordinate + visualisation_correction[subject][1]),
                s=ss,
                alpha=transparency,
                color=colours_types[type_spot],
                label=f"Session {str(session)}",
            )

ax.tick_params(axis="both", which="both", length=0)
# remove numbers on x and y axis but keep frame
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)

pp = 7
ax.text(
    170,
    558,
    "AD = " + str(ads_p[pp]["ad"]) + f"\np {p_sign} " + str(ads_p[pp]["p"]),
    fontsize=20,
    color="black",
)
ax.text(1070, 220, f"P4", fontsize=20, color="black")
ax.invert_xaxis()
ax.set_ylim(ymin=570, ymax=190)
ax.set_xlim(xmin=1080, xmax=0)

plt.savefig(
    f"../../figures/figure{figure_paper_number}/edges/figure{figure_paper_number}_subject{subject}.svg",
    bbox_inches="tight",
    transparent=True,
)

# %% ############################################################################################################
########## Legend #########################################################################################
############################################################################################################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2
import matplotlib.lines as mlines


m_size = 50

legend_elements = [
    mlines.Line2D(
        [0],
        [0],
        marker=".",
        color=colours_types["cold"],
        label=list(colours_types.keys())[0].capitalize(),
        markersize=m_size,
        linestyle="None",
    ),
    mlines.Line2D(
        [0],
        [0],
        marker=".",
        color=colours_types["warm"],
        label=list(colours_types.keys())[1].capitalize(),
        markersize=m_size,
        linestyle="None",
    ),
    mlines.Line2D(
        [0],
        [0],
        marker=".",
        color=colours_types["inconsistent"],
        label=list(colours_types.keys())[2].capitalize(),
        markersize=m_size,
        linestyle="None",
    ),
    mlines.Line2D(
        [0],
        [0],
        marker=".",
        color=colours_types["incongruous"],
        label=list(colours_types.keys())[3].capitalize(),
        markersize=m_size,
        linestyle="None",
    ),
]

fig, ax = plt.subplots(figsize=(15, 10))
ax.legend(
    handles=legend_elements, loc="upper left", bbox_to_anchor=(0.05, 0.95), fontsize=30
)

# remove all axis and ticks and labels
ax.tick_params(axis="both", which="both", length=0)
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)
ax.set_frame_on(False)

plt.savefig(f"../../figures/figure{figure_paper_number}/legend.svg")

# %%
