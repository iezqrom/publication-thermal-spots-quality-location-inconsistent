# %%
import pandas as pd
import matplotlib.pyplot as plt
from globals import path, sessions, subjects, folder_spots_noboth, colours_types
import os
from plotting import prettifySpinesTicks, removeSpines

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

figure_paper_number = "2"

# %%
# Load data
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
order_keys = ["cold", "warm", "inconsistent", "incongruous"]
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

# %% ########################################
# Figure 2b - Number of spots per type
# ########################################
fig, ax = plt.subplots(figsize=(15, 10))

for idx, (type, number) in enumerate(zip(spots_count.keys(), spots_count.values())):
    # stacked bar
    ax.bar(
        0,
        number,
        bottom=sum(list(spots_count.values())[:idx]),
        color=colours_types[type],
        label=type.capitalize(),
        alpha=transparency,
    )

# reverse order of legend
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1], loc="upper right", frameon=False)
# remove spines top and right
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
# remove ticks
ax.tick_params(axis="both", which="both", length=0)
# remove numbers on x and y axis but keep frame
# ax.axes.get_xaxis().set_visible(False)
ax.set_xlabel("All participants", labelpad=20)
# change position of x label
ax.xaxis.set_label_coords(0.3, -0.15)
ax.set_ylabel("Number of spots", labelpad=20)
# remove numbers on x axis but keep label
ax.axes.get_xaxis().set_ticks([])

prettifySpinesTicks(ax)
removeSpines(ax)

plt.tight_layout()
ax.set_ylim([0, 400])
ax.set_xlim([-1, 2.4])

plt.savefig(
    f"../../figures/figure{figure_paper_number}/figure{figure_paper_number}b.svg",
    dpi=300,
    transparent=True,
)

# %% ########################################
# Figure 2c - Number of spots per type per subject
# ########################################
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
            color=colours_types[type],
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
    f"../../figures/figure{figure_paper_number}/figure{figure_paper_number}c.svg",
    dpi=300,
    transparent=True,
)

# %%
for subject_number, subject in enumerate(spots_per_subject.keys()):
    for idx, (type, number) in enumerate(
        zip(spots_per_subject[subject].keys(), spots_per_subject[subject].values())
    ):
        print(f"Subject {subject_number+1} & {type} & {number} \\\\")
# %%
