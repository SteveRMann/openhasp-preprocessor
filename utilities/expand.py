"""
Expand the jsonl file.

Usage:
python expand2.py input_file [-o output_file]
"""

import sys
import re
import os
import argparse

def expand_file(input_file, output_file):
    # Read the entire file into memory
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Open the output file in write mode
    with open(output_file, 'w') as file:
        for line in lines:
            line = line.strip()
            if line:
                if line.startswith("{"):
                    line = re.sub(r'^{', '{\n  ', line, count=1)
                if line.endswith("}"):
                    line = re.sub(r'}$', '\n}\n\n', line, count=1)
                line = re.sub(r',', ',\n  ', line)
                file.write(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Expand a jsonl file.")
    parser.add_argument("input_file", help="The input file to be expanded.")
    parser.add_argument("-o", "--output", help="The output file to write the expanded content to.")
    
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output if args.output else input_file

    # Check if the input file exists
    if not os.path.exists(input_file):
        print(f"Error: The file {input_file} does not exist.")
        sys.exit(1)
    
    # Run the function with the command-line arguments
    expand_file(input_file, output_file)
