"""
Expand the jsonl file.

Usage:
python expand2.py file_path
"""

import sys
import re
import os


# Check if a command-line argument has been provided
if len(sys.argv) < 2 or sys.argv[1] in ['help', '?']:
    print('Usage: python expand.py file_path')
    sys.exit(1)
                
# Get the file_path from the command-line arguments
file_path = sys.argv[1]

# Check if the input file exists
if not os.path.exists(file_path):
    print(f"Error: The file {file_path} does not exist.")
    sys.exit(1)
    
    
    
def expand_file(file_path):
    # Read the entire file into memory
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Open the file in write mode to overwrite it
    with open(file_path, 'w') as file:
        for line in lines:
            line = line.strip()
            if line:
                if line.startswith("{"):
                    line = line.replace("{", "{\n  ", 1)
                if line.endswith("}"):
                    line = line.replace("}", "\n}\n\n", 1)
                line = line.replace(",", ",\n  ")
                file.write(line)


# Run the function with the command-line arguments
expand_file(file_path)
