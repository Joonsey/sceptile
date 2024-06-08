#!/bin/bash

# Define the repository URL and the folder path within the repo
REPO_URL="https://github.com/spMohanty/PlantVillage-Dataset.git"
FOLDER_PATH="raw/color"
OUTPUT_DIR="data"

# Clone the repository (with --depth 1 to minimize download size)
git clone --depth 1 $REPO_URL temp_repo

# Create the output directory
mkdir -p $OUTPUT_DIR

# Move the specific folder to the output directory
mv temp_repo/$FOLDER_PATH/* $OUTPUT_DIR

# Remove the cloned repository
rm -rf temp_repo

# Notify the user of completion
echo
echo "Downloaded the data successfully!! :D"
