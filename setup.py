from setuptools import setup, find_packages

setup(
    name="dicom-rename",
    version="1.0.0",
    url="https://github.com/joshy/dicom-rename.git",
    author="Joshy Cyriac",
    author_email="j.cyriac@gmail.com",
    description="Rename dicom data according to series description and add a .dcm suffix",
    packages=find_packages(),
    entry_points={"console_scripts": ["dicom-rename = rename.__main__:main"]},
)
