#!/bin/bash

# File to modify
file="scribboleth.html"

# Get the new version from the first argument
new_version=$1

# If no new version is provided, just display the current version
if [ -z "$new_version" ]; then
    # Find the line with curVersion and print the version number
    grep "let curVersion" "$file" | sed -n 's/.*"\(.*\)".*/\1/p'
    exit 0
fi

# Use sed to replace the version number in the file
sed -i "s/let curVersion = ".*"/let curVersion = \"$new_version\"/" "$file"

echo "Version updated to $new_version"

