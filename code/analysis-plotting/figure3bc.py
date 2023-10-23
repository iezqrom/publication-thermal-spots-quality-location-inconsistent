# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2
from globals import path, sessions, subjects, folder_spots_noboth, colours_types
import os
from plotting import prettifySpinesTicks, removeSpines

mc = "black"
plt.rcParams.update(
    {
        "font.size": 40,
        "axes.labelcolor": "{}".format(mc),
        "xtick.color": "{}".format(mc),
        "ytick.color": "{}".format(mc),
        "font.family": "sans-serif",
    }
)

ss = 50
transparency = 0.9
figure_paper_number = "3bc"
# %%
visualisation_correction = {pp: [] for pp in subjects}
visualisation_correction[3] = [0, 20]
visualisation_correction[4] = [40, 35]

visualisation_correction[6] = [10, 20]
visualisation_correction[7] = [0, 175]
visualisation_correction[8] = [0, -25]
visualisation_correction[9] = [0, 50]
visualisation_correction[10] = [0, -5]
visualisation_correction[11] = [0, 65]

# %% ###############################################
### Figure all spots
############################################################################################################
fig, ax = plt.subplots(figsize=(15, 10))

image = cv2.imread(f"../../data/arm_images/aligned/S3_1.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray, threshold1=50, threshold2=125)
edges[0:100, 250:] = 0
edges[0:20, 140:] = 0
edges[185:295, 200:] = 0
edges[360:, :] = 0

edges[90:142, 490:] = 0

edges[0:100, 0:50] = 0

edges[100:165, 670:750] = 0
edges[100:173, 800:900] = 0

edges[340:, 300:380] = 0
edges[350:, 500:580] = 0
edges[330:, 800:900] = 0
edges[335:, 680:790] = 0
ax.imshow(edges, vmin=0, vmax=400, cmap="Greys")

for index, subject in enumerate(subjects):
    for session in sessions:
        # print("Subject: ", subject, "Session: ", session)
        datasets = {}
        # for analysis_instance in analysis_instances:
        file_path_name = (
            f"{path}/spots_locations/{folder_spots_noboth}/S{subject}_{session}.csv"
        )
        if os.path.isfile(file_path_name) and os.path.getsize(file_path_name) > 0:
            # open csv file with pandas no header and deal with empty data error
            # check whether the file is empty
            temp_data = pd.read_csv(file_path_name, header=None)
            if subject == 7:
                mean_y_seven = np.mean(temp_data[1])
                print(mean_y_seven)
                temp_data[1] = temp_data[1] - mean_y_seven
                temp_data[1] = temp_data[1] * 0.3
                temp_data[1] = temp_data[1] + (mean_y_seven * 0.3)
            # if subject != 7:
            for i, row in temp_data.iterrows():
                type_spot = row[2]
                # if type_spot != 'both':
                x_coordinate = row[0]
                y_coordinate = row[1]
                type_spot = row[2]

                ax.scatter(
                    (x_coordinate + visualisation_correction[subject][0]),
                    (y_coordinate + visualisation_correction[subject][1]),
                    s=ss,
                    alpha=transparency,
                    color=colours_types[type_spot],
                )

ax.tick_params(axis="both", which="both", length=0)
# remove numbers on x and y axis but keep frame
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)

ax.invert_xaxis()
# removeSpines(ax, sides=['left', 'right', 'top', 'bottom'])

plt.savefig(
    f"../../figures/figure{figure_paper_number}/figure{figure_paper_number}A_edges_all.svg",
    bbox_inches="tight",
    transparent=True,
)

# %% ###############################################
### QUADRANTS
############################################################################################################
qdf = pd.read_csv("../../data/quadrant_test.csv")
print(qdf["Participant"])
# %%
quadrants = {}
sum = []
for zone in range(1, 5):
    quadrants[zone] = qdf[qdf["Zone"] == zone]
    sum.append(quadrants[zone]["Frequency"].sum())
    # quadrants[zone]['Frequency'] to list
    print(quadrants[zone]["Frequency"].tolist())

# %% ###############################################
### Figure bar plot all spots QUADRANTS
############################################################################################################
lwD = 7
widthtick = 10
lenD = 20
ss = 50
transparency = 0.9

mc = "black"
plt.rcParams.update(
    {
        "font.size": 40,
        "axes.labelcolor": "{}".format(mc),
        "xtick.color": "{}".format(mc),
        "ytick.color": "{}".format(mc),
        "font.family": "sans-serif",
    }
)

fig, ax = plt.subplots(figsize=(15, 7))
plt.bar(
    [1, 2, 3, 4], sum, edgecolor="black", fill=False, width=1, lw=widthtick, zorder=0
)

# remove ticks
ax.tick_params(axis="both", which="both", length=0)

# change position of x label
ax.xaxis.set_label_coords(0.3, -0.15)
ax.set_ylabel("Number of spots\nacross participants", labelpad=20)
# remove numbers on x axis but keep label
ax.axes.get_xaxis().set_ticks([])

# write numbers 1-4 at the bottom of each bar
for idx, number in enumerate(range(4, 0, -1)):
    ax.text(idx + 1 - 0.08, 0 + 15, str(number), color="black")

plt.tight_layout()

ax.set_yticks([0, 50, 100, 150])
ax.set_ylim([0, 150])

prettifySpinesTicks(ax)
removeSpines(ax)

plt.savefig(
    f"../../figures/figure{figure_paper_number}/figure{figure_paper_number}A_quadrants_spots_all.svg",
    transparent=True,
)
# %%
# Load data
df = pd.read_csv("../../data/table_clark_evans.csv")
subjects = list(df.columns)[1:]
asterisks = {1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 2, 8: 2}
# %%
fig, ax = plt.subplots(figsize=(15, 10))

offset = 0.4
for idx, number in enumerate(subjects):
    # print(sum(total_number[:idx]))
    # ax.bar(0, sum(total_number[:idx]), color=colours_types[type.lower()], alpha=transparency, label=type)
    # stacked bar
    # ax.bar(number, df[number][0], color='k', alpha=transparency)
    ax.plot(
        [idx - offset, idx + offset], [df[number][0], df[number][0]], color="k", lw=lwD
    )

    # draw asterisk in the middle of the bar
    if asterisks[int(number)] == 4:
        adjusting = 1.3
    elif asterisks[int(number)] == 2:
        adjusting = 1.15
    ax.text(
        float(number) - adjusting,
        df[number][0],
        "*" * asterisks[int(number)],
        fontsize=30,
        color="grey",
    )

# remove ticks
ax.tick_params(axis="both", which="both", length=0)
ax.set_xticks(np.arange(0, 7.01, 1))
ax.set_xticklabels([int(x) for x in np.arange(1, 8.1, 1)])

# remove numbers on x and y axis but keep frame
ax.set_xlabel("Participant", labelpad=20)

# change position of x label
ax.set_ylabel("Aggregation Index\n(R)", labelpad=20)

# horizontal line
ax.axhline(y=1, color="lightgrey", linewidth=lwD, linestyle="--")

prettifySpinesTicks(ax)
removeSpines(ax)

plt.tight_layout()
ax.set_ylim([0, 2])

plt.savefig(
    f"../../figures/figure{figure_paper_number}/figure{figure_paper_number}B_aggregation.svg",
    transparent=True,
    dpi=300,
)

# %%
