#!/bin/bash

# This script will take a folder with many files and split + move the contents across multiple folders
# Will not work if destination directory has folders which match the destination prefix name. ie folders which already exist

SOURCE_DIR="sourcedirectory/" # Enter source directory
DESTINATION="destination/" # Enter destination directory
DESTINATION_PREFIX="batch_" # Enter file naming prefix

i=0
totalFiles=$(ls "$SOURCE_DIR" | wc -l)
filesPerFolder=2 # Change this to how many files you want per folder
numberOfFolders=$(( (totalFiles / filesPerFolder) + 1 ))

while [ $i -lt $numberOfFolders ]; do
	mkdir "$DESTINATION/$DESTINATION_PREFIX$i"
	files=$(ls "$SOURCE_DIR" | head -n $filesPerFolder)
	ls "$SOURCE_DIR" | head -n "$filesPerFolder" | xargs -I {} mv "$SOURCE_DIR/{}" "$DESTINATION/$DESTINATION_PREFIX$i/"
   	i=$((i+1))
done

