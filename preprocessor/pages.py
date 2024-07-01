# Preprocessor for OpenHASP jsonl files.

import os
import sys  # For the command line arguments
import re  # In the Replace_Values function.
from collections import defaultdict  # For chk_ini_file



#Look for duplicate keys in the ini file.
def chk_ini_file(file_path):
    if not os.path.isfile(file_path):
        print(f'Error: {file_path} not found.')
        sys.exit(1)
    
    key_occurrences = defaultdict(list)
    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f, start=1):
            normalized_line = line.strip()
            if normalized_line and not normalized_line.startswith('#'):
                if ':' in normalized_line:
                    key = normalized_line.split(':')[0].strip().lower()
                    key_occurrences[key].append(line_num)

    duplicates = {key: nums for key, nums in key_occurrences.items() if len(nums) > 1}
    
    if not duplicates:
        pass
    else:
        print(f"Error: Duplicate keys found in {file_path}:")
        for key, positions in duplicates.items():
            print(f"'{key}' found at lines: {positions}")
        sys.exit(1)




#Merge all of the page.src files in the argument input folder
def merge_files(src_dir, output_file_path):
    with open(output_file_path, 'w') as output_file:
        for filename in os.listdir(src_dir):
            if filename.endswith('.src'):
                with open(os.path.join(src_dir, filename), 'r') as src_file:
                    for line in src_file:
                        if not line.startswith('#'):
                            output_file.write(line)
                    output_file.write('\n')




#Expand all lines by adding line breaks
def expand_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            line = line.strip()
            if line:
                if line.startswith("{"):
                    line = re.sub(r'^{', '{\n  ', line, count=1)  # Ignore nested braces
                if line.endswith("}"):
                    line = re.sub(r'}$', '\n}\n\n', line, count=1)  # Ignore nested braces
                
                # Regex to match commas not inside quotes
                line = re.sub(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', ',\n  ', line)
                file.write(line)



def remove_blank_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    non_empty_lines = [line.strip() for line in lines if line.strip()]

    with open(file_path, 'w') as file:
        for line in non_empty_lines:
            file.write(line + '\n')




def check_custom_format(file_path):
    with open(file_path, 'r') as file:
        inside_block = False
        block_lines = []
        for line_number, line in enumerate(file, start=1):
            if line.strip() == '{':
                inside_block = True
                block_lines = []
            elif line.strip() == '}':
                inside_block = False
                for i in range(len(block_lines) - 1):
                    if not block_lines[i].strip().endswith(','):
                        print(f"Error in {file_path} on line {line_number - len(block_lines) + i}: Line inside block does not end with a comma")
                        sys.exit(1)
                    if block_lines[i].count('"') % 2 != 0:
                        print(f"Error in {file_path} on line {line_number - len(block_lines) + i}: Line inside block does not have an even number of quotes")
                        sys.exit(1)
                if block_lines and block_lines[-1].strip().endswith(','):
                    print(f"Error in {file_path} on line {line_number - 1}: Last line inside block ends with a comma")
                    sys.exit(1)
                if block_lines and block_lines[-1].count('"') % 2 != 0:
                    print(f"Error in {file_path} on line {line_number - 1}: Last line inside block does not have an even number of quotes")
                    sys.exit(1)
            elif inside_block:
                block_lines.append(line)
            elif line.strip() and not line.strip().startswith('#'):
                print(f"Error in {file_path} on line {line_number}: Line is not inside a data block")
                sys.exit(1)



def check_braces(file_path):
    brace_counter = 0
    last_open_brace_line = None
    last_close_brace_line = 0

    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if line:
                if line.startswith("{"):
                    if brace_counter > 0:
                        print(f"Error in {file_path} on line {last_open_brace_line}: Unmatched opening brace (no closing brace)")
                        return
                    brace_counter += 1
                    last_open_brace_line = line_number
                elif line.startswith("}"):
                    if brace_counter < 1:
                        print(f"Error in {file_path} on line {last_close_brace_line + 1}: Unmatched closing brace (no opening brace)")
                        return
                    brace_counter -= 1
                    last_close_brace_line = line_number

    if brace_counter > 0:
        print(f"Error in {file_path} on line {last_open_brace_line}: Unmatched opening brace (no closing brace)")



def replace_variables(src_file_path, ini_file_path, out_file_path):
    replacements = {}
    with open(ini_file_path, 'r') as sub_file:
        for line in sub_file:
            line = line.split('#')[0].strip()
            if line:
                key, value = line.split(':')
                replacements[key.strip()] = value.strip()

    with open(src_file_path, 'r') as src_file, open(out_file_path, 'w') as out_file:
        for line in src_file:
            for key, value in replacements.items():
                line = re.sub(re.escape(key), value, line, flags=re.IGNORECASE)
            out_file.write(line)

    with open(out_file_path, 'r') as out_file:
        for line_number, line in enumerate(out_file, start=1):
            if '@' in line:
                print(f'Found "@" in line {line_number}: {line.strip()}')



#Looking for duplicate page:id keys.
def chkduplicates(file_path):
    page_id_pairs = {}
    last_page = None

    with open(file_path, 'r') as file:
        page = id = None
        inside_block = False
        
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            
            if line:
                if line == "{":
                    inside_block = True
                    page = id = None
                elif line == "}":
                    inside_block = False
                    if id is not None and page is None:
                        print(f"Error in {file_path} on line {line_number}: 'id' defined without 'page'")
                        sys.exit(1)
                    if page is not None:
                        last_page = page
                elif inside_block:
                    if line.startswith('"page"'):
                        page = line.split(":")[1].strip().strip(',')
                    elif line.startswith('"id"'):
                        id = line.split(":")[1].strip().strip(',')
                    if page is None:
                        page = last_page
                    if page is not None and id is not None:
                        pair = (page, id)
                        if pair in page_id_pairs:
                            print(f"Error in {file_path} on line {line_number}: Duplicate page:id pair {pair}")
                            print(f"First occurrence was on line {page_id_pairs[pair]}")
                            sys.exit(1)
                        else:
                            page_id_pairs[pair] = line_number
                            page = id = None
                elif not inside_block and line and not line.startswith('#'):
                    print(f"Error in {file_path} on line {line_number}: Line is not inside a data block")
                    sys.exit(1)





if len(sys.argv) < 2 or sys.argv[1] in ['help', '?']:
    print('Usage: python pages.py src_dir')
    print('Where src_dir contains the page.src files.')
    sys.exit(1)

src_dir = sys.argv[1]

if not os.path.isdir(src_dir):
    print(f'Error: The directory {src_dir} does not exist.')
    sys.exit(1)
    
chk_ini_file('pages.ini')
merge_files(src_dir, 'pages.tmp')
expand_file('pages.tmp')
remove_blank_lines('pages.tmp')
check_custom_format('pages.tmp')
check_braces('pages.tmp')
replace_variables('pages.tmp', 'pages.ini', 'pages.jsonl')
os.remove('pages.tmp')
chkduplicates('pages.jsonl')
