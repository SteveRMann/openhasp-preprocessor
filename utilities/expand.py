"""
Expand the jsonl file.

Usage:
python expand.py inputfile outputfile
"""

import json
import sys
import re


# Check if a command-line argument has been provided
if len(sys.argv) < 3 or sys.argv[1] in ['help', '?']:
    print('Usage: python expand.py inputfile outputfile')
    sys.exit(1)
                
# Get the input file and output file from the command-line arguments
infile, outfile = sys.argv[1], sys.argv[2]

def format_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        for line in input_file:
            line = line.strip()
            if line:
                if line.startswith("{"):
                    line = line.replace("{", "{\n", 1)
                if line.endswith("}"):
                    line = line.replace("}", "\n}\n\n", 1)
                line = line.replace(",", ",\n  ")
                output_file.write(line)

# Run the function with the command-line arguments
format_file(infile, outfile)
