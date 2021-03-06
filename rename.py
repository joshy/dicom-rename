import argparse
import os
import sys
from os.path import join
from pathlib import Path
from typing import Optional

import pydicom


def is_dicom_file(file) -> Optional[pydicom.Dataset]:
    try:
        return pydicom.dcmread(file)
    except pydicom.errors.InvalidDicomError:
        # do nothing, not a dicom file
        return None


def find_first_dicom_file_in_dir(path):
    for root, _, files in os.walk(path):
        for f in files:
            ds = is_dicom_file(join(root, f))
            if ds:
                return ds
    return False


def replace_space_with_underscore(description):
    return description.replace(" ", "_")


def _rename_series(path):
    for patientdir in os.listdir(path):
        patientdir_path = join(path, patientdir)
        for studydir in os.listdir(patientdir_path):
            studydir_path = join(patientdir_path, studydir)
            for seriesdir in os.listdir(studydir_path):
                seriesdir_path = join(studydir_path, seriesdir)
                ds = find_first_dicom_file_in_dir(seriesdir_path)
                if ds:
                    try:
                        desc = replace_space_with_underscore(ds.SeriesDescription)
                    except AttributeError:
                        desc = ""
                    new_series_path = join(
                        path,
                        patientdir,
                        studydir,
                        str(ds.SeriesNumber) + "-" + desc + "-" + str(ds.Modality),
                    )
                    print("renaming series from", seriesdir_path, "->", new_series_path)
                    try:
                        os.rename(seriesdir_path, new_series_path)
                    except FileNotFoundError as e:
                        print(e)
            if ds:
                new_studydir_path = join(patientdir_path, str(ds.AccessionNumber))
                print(
                    "renaming study from", studydir_path, "->", new_studydir_path, "\n"
                )
                os.rename(studydir_path, new_studydir_path)


def add_dicom_extension(path):
    files = [x for x in path.glob("**/*") if x.is_file()]
    print("Start renaming {} files".format(len(files)))
    for f in files:
        _, ext = os.path.splitext(f)
        # simple guess if it is a dicom file without loading it
        if ext[-1].isdigit():
            os.rename(f, str(f) + ".dcm")
    print("End renaming {} files".format(len(files)))


def run():
    # call example
    # python rename.py --dir /data/example-dir
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--dir", help="Starting directory")
    parser.add_argument(
        "-rs","--rename-series", help="Rename series number folder with series description", action="store_true"
    )
    args = parser.parse_args()

    if not args.dir:
        print("--dir parameter missing, exiting")
        exit(1)

    parent_dir = Path(args.dir)
    print("Running on dir", parent_dir)
    add_dicom_extension(parent_dir)
    if args.rename_series:
        _rename_series(parent_dir)
    exit(0)


run()
