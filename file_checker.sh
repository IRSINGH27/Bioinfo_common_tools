#!/bin/bash

# Check if the required number of arguments was provided
if [ $# -lt 2 ]; then
  echo "Usage: find_file.sh FILE_NAME DIRECTORY"
  exit 1
fi

# Recursively search for the file in the specified directory
if file_path=$(find "$2" -type f -name "$1" -exec bash -c 'echo {}' \;); then
  # File was found
  echo "File was found in $(dirname "$file_path")"
else
  # File was not found
  echo "File was not found"
fi

