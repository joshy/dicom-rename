# dicom-rename
Small utility for renaming directories and series based on dicom metadata

Assumed directory structure before renaming
```
 * Top-level dir
   \- PatientID-Dir
      \- AccessionNumber
         \- SeriesNumber
```

After renaming
```
 * Top-level dir
   \- PatientID-Dir
      \- AccessionNumber
         \-SeriesNumber-SeriesDescription-ModalityShortCode
```

# Installation

Git clone this repo and in the folder run
```
pip install -e .
```
will install it as a runnable script.