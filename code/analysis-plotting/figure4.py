# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
from globals import path, sessions, subjects, folder_spots_noboth, threshold_distance, colors_session
from plotting import removeSpines, prettifySpinesTicks

ss = 25
transparency = 0.9
figure_paper_number = "4"

# load all_conserved_spots
all_conserved_spots = pd.read_csv("../../data/all_conserved_spots.csv")

# %% Master arm
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
            file_path_name = (
                f"{path}/spots_locations/{folder_spots_noboth}/S{subject}_{session}.csv"
            )

            subject_conserved = all_conserved_spots[
                all_conserved_spots["subject"] == subject
            ]
            subject_conserved = subject_conserved[
                subject_conserved["session"] == session
            ]

            # check whether subject_conserved is empty
            if not subject_conserved.empty:
                for i, row in subject_conserved.iterrows():
                    x_coordinate = row["x_coord_aligned"]
                    y_coordinate = row["y_coord_aligned"]

                    ax.scatter(
                        (x_coordinate + visualisation_correction[subject][0]),
                        (y_coordinate + visualisation_correction[subject][1]),
                        s=ss + 40,
                        alpha=1,
                        color="white",
                        zorder=8,
                    )
                    ax.scatter(
                        (x_coordinate + visualisation_correction[subject][0]),
                        (y_coordinate + visualisation_correction[subject][1]),
                        s=ss + 40,
                        alpha=1,
                        color="black",
                        zorder=9,
                        facecolors="none",
                        edgecolors="black",
                    )
                    ax.scatter(
                        (x_coordinate + visualisation_correction[subject][0]),
                        (y_coordinate + visualisation_correction[subject][1]),
                        s=ss + 110,
                        alpha=1,
                        color="black",
                        zorder=10,
                        marker="+",
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
                    # put number in plot
                    ax.text(
                        (x_coordinate + visualisation_correction[subject][0]),
                        (y_coordinate + visualisation_correction[subject][1]),
                        str(session),
                        fontsize=20,
                        color=colors_session[session],
                        horizontalalignment="center",
                        verticalalignment="center",
                    )
                    # ax.scatter((x_coordinate + visualisation_correction[subject][0]), (y_coordinate + visualisation_correction[subject][1]), s=ss, alpha=transparency, color = colors_session[session], label = f"Session {str(session)}")

        ax.tick_params(axis="both", which="both", length=0)
        # remove numbers on x and y axis but keep frame
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)

        ax.text(1180, 30, f"P{index + 1}", fontsize=20, color="black")

        ax.set_ylim(ymin=420, ymax=0)

        plt.savefig(
            f"../../figures/figure{figure_paper_number}/figure{figure_paper_number}_sessions_subject{subject}.svg",
            bbox_inches="tight",
            dpi=300,
            transparent=True,
        )

# %% ############################################################################################################
########## Subject 7
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
    file_path_name = (
        f"{path}/spots_locations/{folder_spots_noboth}/S{subject}_{session}.csv"
    )
    subject_conserved = all_conserved_spots[all_conserved_spots["subject"] == subject]
    subject_conserved = subject_conserved[subject_conserved["session"] == session]
    # check whether subject_conserved is empty
    if not subject_conserved.empty:
        for i, row in subject_conserved.iterrows():
            x_coordinate = row["x_coord_aligned"]
            y_coordinate = row["y_coord_aligned"]

            ax.scatter(
                (x_coordinate + visualisation_correction[subject][0]),
                (y_coordinate + visualisation_correction[subject][1]),
                s=ss + 40,
                alpha=1,
                color="white",
                zorder=8,
            )

            ax.scatter(
                (x_coordinate + visualisation_correction[subject][0]),
                (y_coordinate + visualisation_correction[subject][1]),
                s=ss + 40,
                alpha=1,
                color="black",
                zorder=9,
                facecolors="none",
                edgecolors="black",
            )
            ax.scatter(
                (x_coordinate + visualisation_correction[subject][0]),
                (y_coordinate + visualisation_correction[subject][1]),
                s=ss + 110,
                alpha=1,
                color="black",
                zorder=10,
                marker="+",
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
            ax.text(
                (x_coordinate + visualisation_correction[subject][0]),
                (y_coordinate + visualisation_correction[subject][1]),
                str(session),
                fontsize=20,
                color=colors_session[session],
                horizontalalignment="center",
                verticalalignment="center",
            )
            # ax.scatter((x_coordinate + visualisation_correction[subject][0]), (y_coordinate + visualisation_correction[subject][1]), s=ss, alpha=transparency, color = colors_session[session], label = f"Session {str(session)}")

ax.tick_params(axis="both", which="both", length=0)
# remove numbers on x and y axis but keep frame
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)
ax.text(1070, 220, f"P4", fontsize=20, color="black")

ax.set_ylim(ymin=570, ymax=190)
ax.set_xlim(xmin=1080, xmax=0)

plt.savefig(
    f"../figures/figure{figure_paper_number}/figure{figure_paper_number}_sessions_subject{subject}.svg",
    bbox_inches="tight",
    dpi=300,
    transparent=True,
)

# %% Legend
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2
import matplotlib.lines as mlines

# get unique handles
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
# background of legend white

lgnd = ax.legend(
    by_label.values(),
    by_label.keys(),
    loc="lower right",
    fontsize=20,
    frameon=False,
    bbox_to_anchor=(0.95, 0.0),
)
for dot in lgnd.legendHandles:
    dot._sizes = [100]
# change size of dots in legend
# change color of text in legend to white

m_size = 10

legend_elements = [
    mlines.Line2D(
        [0],
        [0],
        color=colors_session[1],
        label="Session 1 only",
        linewidth=m_size,
    ),
    mlines.Line2D(
        [0],
        [0],
        color=colors_session[2],
        label="Session 2 only",
        linewidth=m_size,
    ),
    mlines.Line2D(
        [0],
        [0],
        color=colors_session[3],
        label="Session 3 only",
        linewidth=m_size,
    ),
    mlines.Line2D(
        [0],
        [0],
        color=colors_session[4],
        label="Session 4 only",
        linewidth=m_size,
    ),
    mlines.Line2D(
        [0],
        [0],
        marker="+",
        color=colors_session["conserved"],
        label="Conserved",
        markersize=50,
        linestyle="None",
        linewidth=m_size,
    ),
]

fig, ax = plt.subplots(figsize=(15, 10))
ax.legend(
    handles=legend_elements,
    loc="upper left",
    bbox_to_anchor=(0.05, 0.95),
    fontsize=30,
    frameon=False,
)

removeSpines(ax, sides=["top", "right", "left", "bottom"])
# remove ticks
ax.tick_params(axis="both", which="both", length=0)
# remove numbers on x and y axis but keep frame
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)

plt.savefig(f"../../figures/figure{figure_paper_number}/legend.svg", transparent=True)
# %% ############################################
# Check quality of conserved and sessions
# ############################################
for subject in subjects:
    # get the conserved spots for this subject
    print(f"Subject {subject}")
    subject_conserved = all_conserved_spots[all_conserved_spots["subject"] == subject]
    # print(len(subject_conserved))
    temp_sesh = subject_conserved[
        ["x_coord_aligned", "y_coord_aligned"]
    ].to_numpy()  # print(temp_sessions[combination[1]])
    for index, spot in enumerate(temp_sesh):
        mat_tr = np.int64(temp_sesh - spot)
        mat = np.linalg.norm(mat_tr, axis=1)

        if len(mat[(mat < threshold_distance) & (mat > 0)]) > 0:
            print(spot, mat)  # check by eye


# %% ########################################
# Figure 5b - Number of spots per type per subject
# ########################################
spots_count = {}
spots_per_subject = {}

for index, subject in enumerate(subjects):
    spots_per_subject[subject] = {}
    for session in sessions:
        print("Subject: ", subject, "Session: ", session)
        datasets = {}
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
                if session in spots_count.keys():
                    spots_count[session] += temp_data[2].value_counts().to_dict()[key]
                else:
                    spots_count[session] = temp_data[2].value_counts().to_dict()[key]

                if session in spots_per_subject[subject].keys():
                    spots_per_subject[subject][session] += (
                        temp_data[2].value_counts().to_dict()[key]
                    )
                else:
                    spots_per_subject[subject][session] = (
                        temp_data[2].value_counts().to_dict()[key]
                    )

# %%
spots = 0
for subject in spots_per_subject.keys():
    for session in spots_per_subject[subject].keys():
        spots += spots_per_subject[subject][session]

print(spots)
print(sum(list(spots_count.values())))

order_keys = [1, 2, 3, 4]
# reverse order of keys
order_keys = order_keys[::-1]
# change order of keys
spots_count = {k: spots_count[k] for k in order_keys}

for subject in spots_per_subject.keys():
    for type_spot in order_keys:
        if type_spot not in spots_per_subject[subject].keys():
            spots_per_subject[subject][type_spot] = 0
        else:
            spots_per_subject[subject][type_spot] = spots_per_subject[subject][
                type_spot
            ]

    spots_per_subject[subject] = {k: spots_per_subject[subject][k] for k in order_keys}

# %%
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

fig, ax = plt.subplots(figsize=(15, 10))

for subject_number, subject in enumerate(spots_per_subject.keys()):
    for idx, (type, number) in enumerate(
        zip(spots_per_subject[subject].keys(), spots_per_subject[subject].values())
    ):
        # stacked bar
        ax.bar(
            subject_number + 1,
            number,
            bottom=sum(list(spots_per_subject[subject].values())[:idx]),
            color=colors_session[type],
            alpha=transparency,
        )

# remove numbers on x and y axis but keep frame
ax.set_xlabel("Participant", labelpad=20)

# change position of x label
ax.set_ylabel("Number of spots", labelpad=20)

# change x ticks
ax.set_xticks(range(1, len(subjects) + 1))

prettifySpinesTicks(ax)
removeSpines(ax)

plt.tight_layout()
ax.set_ylim([0, 125])
# ax.set_xlim([-1, 2.4])

plt.savefig(
    f"../../figures/figure{figure_paper_number}/figure{figure_paper_number}b_spots_participants.svg",
    dpi=300,
    transparent=True,
)

# %%
# loop over consersed spots and print the session
for subject in subjects:
    # get the conserved spots for this subject
    print(f"\nSubject {subject}")
    subject_conserved = all_conserved_spots[all_conserved_spots["subject"] == subject]
    for index, row in subject_conserved.iterrows():
        print(f"Session {row['session']}")
# %%
sessions_2 = []
sessions_4 = []

for subject in subjects:
        for idx, (type, number) in enumerate(
        zip(spots_per_subject[subject].keys(), spots_per_subject[subject].values())
    ):
            if type == 2 or type == 1:
                sessions_2.append(number)
            elif type == 4 or type == 3:
                sessions_4.append(number)

# %%
