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