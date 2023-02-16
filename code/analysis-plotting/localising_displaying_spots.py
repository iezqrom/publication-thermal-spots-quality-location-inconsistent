### This code displays and image, then it grabs the position of the pixel when you click on the image
# It saves the positions in a csv file

from tkinter import *
from tkinter import filedialog as tkfd

import numpy as np
from PIL import Image, ImageDraw, ImageTk
import csv
import os
import sys

counter = 0
library = {"x_coord": [], "y_coord": [], "type": []}
keys = library.keys()
path = "/Users/ivan/Documents/aaa_online_stuff/coding/python/phd/expt17_spots/data"


def windowHandler(file_path_name, analysis_instance):
    root = Tk()

    ### Getting image
    img = Image.open(f"{file_path_name}")
    basewidth = 1100  # change if want image to be bigger or smaller
    wpercent = basewidth / float(img.size[0])
    hsize = int((float(img.size[1]) * float(wpercent)))
    image = img.resize((basewidth, hsize), Image.ANTIALIAS)
    # image.save(f'{file_path_name}.jpg')

    ### Configuration of the frame

    root.geometry("{}x{}".format(basewidth, hsize))

    # setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    canvas = Canvas(frame, bd=0)
    canvas.grid(row=0, column=0, sticky=N + S + E + W)

    frame.pack(fill=BOTH, expand=1)

    # adding the image
    image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, image=image, anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))

    global type_spot
    type_spot = "cold"
    root.title(
        f"Analysis instance: {analysis_instance} / Spot type: {type_spot.upper()}"
    )
    # function to be called when mouse is clicked
    def printcoords(event):
        # outputting x and y coords to console
        global type_spot
        global library
        print(event.x, event.y)
        library["x_coord"].append(event.x)
        library["y_coord"].append(event.y)
        library["type"].append(type_spot)
        print(type_spot)

    # function to change title when letter c is pressed
    def changeTitleSpot(event):
        global type_spot
        global library
        type_spot = "cold"
        if event.char == "c":
            type_spot = "cold"
        elif event.char == "w":
            type_spot = "warm"
        elif event.char == "g":
            type_spot = "incongruous"
        elif event.char == "s":
            type_spot = "inconsistent"
        elif event.char == "b":
            type_spot = "both"
        # terminate python
        elif event.char == "e":
            sys.exit()

        root.title(
            f"Analysis instance: {analysis_instance} / Spot type: {type_spot.upper()}"
        )

        if event.char == "q":
            root.destroy()

    # mouseclick event
    canvas.bind("<Button 1>", printcoords)
    # key press event
    letters = ["c", "w", "g", "s", "q", "b", "e"]
    for letter in letters:
        root.bind(letter, changeTitleSpot)

    root.mainloop()

    return library


def saveData(library, file_path_name):
    of1 = open(file_path_name, "w")
    data_writer = csv.writer(of1)

    print(f"Saving data to {file_path_name}")
    for i in np.arange(len(library["x_coord"])):
        data_writer.writerow(
            [library["x_coord"][i], library["y_coord"][i], library["type"][i]]
        )
    of1.close()


def get_int(string):
    return int("".join(filter(str.isdigit, string)))


def checkSubjectStart(spots_locations_path):
    subjects = [3, 4, 6, 7, 8, 9, 10, 11]
    last_session = 1
    all_files = os.listdir(f"{spots_locations_path}/original/")
    if len(all_files) == 0:
        return subjects, last_session
    else:
        csv_files = [f for f in all_files if f.endswith(".csv")]
        # split files
        splitted_names = [f.split("_") for f in csv_files]
        # remove strings from list
        subjects_csvs = [get_int(f[0]) for f in splitted_names]
        last_subject = max(subjects_csvs)
        sessions_last_subject = [get_int(f[0]) == last_subject for f in splitted_names]

        last_subject_session = []
        for i, f in enumerate(sessions_last_subject):
            if f:
                # split name
                splitted_name = csv_files[i].split("_")
                # get session
                session = get_int(splitted_name[1])
                last_subject_session.append(session)

        last_session = max(last_subject_session)

        # get index of last_subject from subjects
        last_subject_index = subjects.index(last_subject)

        # remove all values in subjects before last_subject
        subjects = subjects[last_subject_index:]

        return subjects, last_session


if __name__ == "__main__":
    ## Define variables
    spots_locations_path = path + "/spots_locations"
    images_path = path + "/arm_images"
    analysis_instances = ["original", "aligned"]

    subjects, start_session = checkSubjectStart(spots_locations_path)

    # get .csv files in the folder
    files = os.listdir(f"{images_path}/aligned")
    files = [f for f in files if f.endswith(".csv")]

    ## Check and create folders
    # print(os.path.exists(spots_locations_path))
    if not os.path.exists(spots_locations_path):
        os.mkdir(spots_locations_path)
        for analysis_instance in analysis_instances:
            os.mkdir(f"{spots_locations_path}/{analysis_instance}")

    ## Loop through all the images
    for subject in subjects:
        sessions = range(start_session, 5)
        for session in sessions:
            n_spots = []
            while True:
                for analysis_instance in analysis_instances:
                    print(
                        f"Subject: {subject} / Session: {session} / Analysis instance: {analysis_instance}"
                    )
                    if analysis_instance == "original":
                        file_format = "png"
                    elif analysis_instance == "aligned":
                        file_format = "jpg"

                    name_path_file = f"{images_path}/{analysis_instance}/S{subject}_{session}.{file_format}"
                    # name_path_file = f"{path}/{analysis_instance}/S3_1.{file_format}"
                    library = windowHandler(name_path_file, analysis_instance)
                    n_spots.append(len(library["x_coord"]))
                    print(library)

                    name_path_file = f"{spots_locations_path}/{analysis_instance}/S{subject}_{session}.csv"
                    # name_path_file = f"{path}/{analysis_instance}/subject3_session1.csv"
                    saveData(library, name_path_file)
                    library = {"x_coord": [], "y_coord": [], "type": []}
                if n_spots[0] == n_spots[1]:
                    break
                else:
                    print(
                        f"Different number of spots in original and aligned images for subject {subject} and session {session}. Please, try again"
                    )
                    n_spots = []
