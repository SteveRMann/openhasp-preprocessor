# Preprocessor for OpenHASP jsonl files.

import os
import sys  # For the command line arguments
import re  # In the Replace_Values function.

# import defaultdict from collections to keep track of line occurrences
from collections import defaultdict


def chk_ini_file(file_path):
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f'Error: {file_path} not found.')
        sys.exit(1)
  
    # Use defaultdict(list) to store each key and the line numbers where it appears.  
    key_occurrences = defaultdict(list)
    
    with open(file_path, 'r') as f:
        # Read the file line-by-line, strip whitespace, and record the line numbers where each key appears.
        for line_num, line in enumerate(f, start=1):
            # Normalize the input by stripping leading/trailing whitespace
            normalized_line = line.strip()
            # print(f"Line {line_num}: '{normalized_line}'")  # Debug print

            if normalized_line and not normalized_line.startswith('#'):  # Ignore empty lines and comments
                if ':' in normalized_line:
                    key = normalized_line.split(':')[0].strip().lower()
                    key_occurrences[key].append(line_num)

    duplicates = {key: nums for key, nums in key_occurrences.items() if len(nums) > 1}
    
    if not duplicates:
        pass  # Placeholder for no-action
    else:
        print(f"Error: Duplicate keys found in {file_path}:")
        for key, positions in duplicates.items():
            print(f"'{key}' found at lines: {positions}")
        sys.exit(1)  # Exit if duplicates are found



def merge_files(src_dir, output_file_path):
    # Open the output file
    with open(output_file_path, 'w') as output_file:
        # Loop over all files in the source directory
        for filename in os.listdir(src_dir):
            # Check if the file has a .src extension
            if filename.endswith('.src'):
                # Open the source file
                with open(os.path.join(src_dir, filename), 'r') as src_file:
                    # Read the source file line by line
                    for line in src_file:
                        # Skip lines that begin with #
                        if not line.startswith('#'):
                            # Write the line to the output file
                            output_file.write(line)
                    # Write a newline to separate the contents of different files
                    output_file.write('\n')


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


def remove_blank_lines(file_path):
    # Read the entire file into memory
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Filter out blank lines
    non_empty_lines = [line.strip() for line in lines if line.strip()]

    # Open the file in write mode to overwrite it
    with open(file_path, 'w') as file:
        for line in non_empty_lines:
            file.write(line + '\n')  # Add a newline after each line






def check_custom_format(file_path):
    # Open the file
    with open(file_path, 'r') as file:
        # Initialize a flag to indicate whether we're inside a block
        inside_block = False
        # Initialize a list to hold the lines of the current block
        block_lines = []
        # Read the file line by line
        for line_number, line in enumerate(file, start=1):
            # Check if the line starts a block
            if line.strip() == '{':
                inside_block = True
                block_lines = []
            # Check if the line ends a block
            elif line.strip() == '}':
                inside_block = False
                # Check all lines of the block except the last one
                for i in range(len(block_lines) - 1):
                    if not block_lines[i].strip().endswith(','):
                        print(f"Error in {file_path} on line {line_number - len(block_lines) + i}: Line inside block does not end with a comma")
                        sys.exit(1)
                    # Check for even number of quotes
                    if block_lines[i].count('"') % 2 != 0:
                        print(f"Error in {file_path} on line {line_number - len(block_lines) + i}: Line inside block does not have an even number of quotes")
                        sys.exit(1)
                # Check the last line of the block
                if block_lines and block_lines[-1].strip().endswith(','):
                    print(f"Error in {file_path} on line {line_number - 1}: Last line inside block ends with a comma")
                    sys.exit(1)
                # Check for even number of quotes in the last line
                if block_lines and block_lines[-1].count('"') % 2 != 0:
                    print(f"Error in {file_path} on line {line_number - 1}: Last line inside block does not have an even number of quotes")
                    sys.exit(1)
            # If we're inside a block, add the line to the block lines
            elif inside_block:
                block_lines.append(line)
            # If we're not inside a block and the line is not empty or a comment, raise an error
            elif line.strip() and not line.strip().startswith('#'):
                print(f"Error in {file_path} on line {line_number}: Line is not inside a data block")
                sys.exit(1)



def check_braces(file_path):
    # Initialize a counter for the braces and variables to hold the line numbers of the last opening and closing braces
    brace_counter = 0
    last_open_brace_line = None
    last_close_brace_line = 0  # Initialize to 0

    # Open the file
    with open(file_path, 'r') as file:
        # Read the file line by line
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if line:
                if line.startswith("{"):
                    # If there's already an unmatched opening brace, raise an error
                    if brace_counter > 0:
                        print(f"Error in {file_path} on line {last_open_brace_line}: Unmatched opening brace (no closing brace)")
                        return
                    # Increment the counter and store the line number
                    brace_counter += 1
                    last_open_brace_line = line_number
                elif line.startswith("}"):
                    # If there's already an unmatched closing brace, raise an error
                    if brace_counter < 1:
                        print(f"Error in {file_path} on line {last_close_brace_line + 1}: Unmatched closing brace (no opening brace)")
                        return
                    # Decrement the counter and store the line number
                    brace_counter -= 1
                    last_close_brace_line = line_number

    # If the counter is positive after reading the entire file, there is an opening brace without a matching closing brace
    if brace_counter > 0:
        print(f"Error in {file_path} on line {last_open_brace_line}: Unmatched opening brace (no closing brace)")

                    

def replace_variables(src_file_path, ini_file_path, out_file_path):
    # Read the substitutions file and build a dictionary of replacements.
    # replacements is an empty dictionary to store key-value pairs.
    replacements = {}
    with open(ini_file_path, 'r') as sub_file:
        for line in sub_file:
            line = line.split('#')[0].strip()  # Ignore in-line comments and strip whitespace
            if line:  # Ignore blank lines
                key, value = line.split(':')
                replacements[key.strip()] = value.strip()

    # Read the source file, make the replacements, and write the result to the output file
    with open(src_file_path, 'r') as src_file, open(out_file_path, 'w') as out_file:
        for line in src_file:
            for key, value in replacements.items():
                # Perform case-insensitive replacement using re.sub
                line = re.sub(re.escape(key), value, line, flags=re.IGNORECASE)
            out_file.write(line)

    # Check the output file for lines containing '@'
    # If found, then there is an unresolved variable.
    with open(out_file_path, 'r') as out_file:
        for line_number, line in enumerate(out_file, start=1):
            if '@' in line:
                print(f'Found "@" in line {line_number}: {line.strip()}')




def chkduplicates(file_path):
    # Initialize a dictionary to hold the page:id pairs and their line numbers
    page_id_pairs = {}

    # Read the entire file into memory
    with open(file_path, 'r') as file:
        page = id = None
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if line:
                if line.startswith("{"):
                    # Reset page and id at the start of each block
                    page = id = None
                elif line.startswith('"page"'):
                    page = line.split(":")[1].strip().strip(',')
                elif line.startswith('"id"'):
                    id = line.split(":")[1].strip().strip(',')
                if page is not None and id is not None:
                    # Keep the page and id values in their original order
                    pair = (page, id)
                    if pair in page_id_pairs:
                        print(f"Error in {file_path} on line {line_number}: Duplicate page:id pair {pair}")
                        print(f"First occurrence was on line {page_id_pairs[pair]}")
                        sys.exit(1)
                    else:
                        # Store the line number along with the pair
                        page_id_pairs[pair] = line_number
                        # Reset page and id for the next pair
                        page = id = None
            
            

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
chk_ini_file('pages.ini')
merge_files(src_dir, 'pages.tmp')  # src_dir, output_file_path
expand_file('pages.tmp')
remove_blank_lines("pages.tmp")
check_custom_format('pages.tmp')
check_braces('pages.tmp')
replace_variables('pages.tmp', 'pages.ini', 'pages.jsonl') # src_file_path, ini_file_path, out_file_path
os.remove('pages.tmp')  # Delete the 'pages.tmp' file
chkduplicates('pages.jsonl')
