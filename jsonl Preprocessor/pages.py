# Preprocessor for OpenHASP jsonl files.

import os
import sys  # For the command line arguments

def merge_files(src_dir, output_file_path):
    # Open the output file
    with open(output_file_path, 'w') as output_file:
        # Loop over all files in the source directory
        for filename in os.listdir(src_dir):
            # Check if the file has a .src extension
            if filename.endswith('.src'):
                # Open the source file
                with open(os.path.join(src_dir, filename), 'r') as src_file:
                    # Write the contents of the source file to the output file
                    output_file.write(src_file.read())
                    # Write a newline to separate the contents of different files
                    output_file.write('\n')

def replace_values(src_file_path, ini_file_path, out_file_path):
    # Read the substitutions file and build a dictionary of replacements
    replacements = {}
    with open(ini_file_path, 'r') as sub_file:
        for line in sub_file:
            line = line.strip()
            if line and not line.startswith('#'):  # Ignore blank lines and lines starting with a comment
                key, value = line.split(':')
                replacements[key] = value

    # Read the source file, make the replacements, and write the result to the output file
    with open(src_file_path, 'r') as src_file, open(out_file_path, 'w') as out_file:
        for line in src_file:
            for key, value in replacements.items():
                line = line.replace(key, value)
            out_file.write(line)

    # Check the output file for lines containing '@'
    with open(out_file_path, 'r') as out_file:
        for line_number, line in enumerate(out_file, start=1):
            if '@' in line:
                print(f'Found "@" in line {line_number}: {line.strip()}')

def check_duplicates(file_path):
    # Read the file and build a dictionary of line occurrences
    occurrences = {}
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if line:  # Ignore blank lines
                # Check if the line contains a "page" and "id" pair
                if '"page":' in line and '"id":' in line:
                    # Build a key from the "page" and "id" values
                    key = line[line.index('"page":'):line.index('"id":')+len('"id":')+2]
                    # Add the line number to the occurrences
                    if key in occurrences:
                        occurrences[key].append(line_number)
                    else:
                        occurrences[key] = [line_number]

    # Check for duplicates
    for key, line_numbers in occurrences.items():
        if len(line_numbers) > 1:
            print(f'Found duplicate for {key} at lines {line_numbers}')

# Check if a command-line argument has been provided
if len(sys.argv) < 2 or sys.argv[1] in ['help', '?']:
    print('Usage: python pages.py src_dir')
    print('Where src_dir contains the page.src files.')
    sys.exit(1)

# Get the source directory from the command-line arguments
src_dir = sys.argv[1]

# Check if the source directory exists
if not os.path.isdir(src_dir):
    print(f'Error: The directory {src_dir} does not exist.')
    sys.exit(1)
    
# Run the functions
merge_files(src_dir, 'pages.src')  # src_dir, output_file_path
replace_values('pages.src', 'pages.ini', 'pages.jsonl') # src_file_path, ini_file_path, out_file_path
os.remove('pages.src')  # Delete the 'pages.src' file
check_duplicates('pages.jsonl') # file_path
