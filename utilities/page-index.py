# pages-index.py
# Makes an index of page, ID and comment from the page.src files
# in the argument folder.
# Optional:
#  -o outputfile will write the sorted index to the output file.
#

import os
import re
import sys
import argparse
import subprocess

def extract_and_sort(input_file, output_file=None):
    data = []
    current_page = None  # Initialize current_page to None

    # Open and read the input file
    with open(input_file, 'r') as file:
        for line in file:
            # Clean the line and remove any trailing whitespace
            line = line.strip()

            if line:
                # Extract the page if present
                page_match = re.search(r'"page":(\d+)', line)
                if page_match:
                    current_page = int(page_match.group(1))  # Update current_page if found

                # Extract the ID
                id_match = re.search(r'"id":(\d+)', line)
                if not id_match:
                    continue
                id = int(id_match.group(1))

                # Extract the comment
                comment_match = re.search(r'"comment":"(.*?)"', line)
                comment = comment_match.group(1) if comment_match else ""

                # Append to data list with the current_page
                if current_page is not None:
                    data.append((current_page, id, comment))

    # Sort data by page and id
    data.sort(key=lambda x: (x[0], x[1]))

    # Prepare output
    output_lines = []
    current_page = None
    for page, id, comment in data:
        if current_page is not None and page != current_page:
            output_lines.append("")  # Add a blank line
        current_page = page
        output_lines.append(f"p{page}b{id}, {comment}")

    # Write to the output file or display to console
    if output_file:
        with open(output_file, 'w') as f:
            f.write("\n".join(output_lines))
    else:
        for line in output_lines:
            print(line)


def main(pagesfolder, output_file=None):
    temp_file = "pages.tmp"

    # Open the temp file to write the combined compressed content
    with open(temp_file, 'w') as temp_out:
        # Iterate through all .src files in the specified folder
        for filename in os.listdir(pagesfolder):
            if filename.endswith(".src"):
                src_path = os.path.join(pagesfolder, filename)
                compressed_file = src_path + ".compressed"

                # Run the compress.py script on the current .src file
                subprocess.run(['python', 'compress.py', src_path, compressed_file])

                # Append the compressed content to the temp file
                with open(compressed_file, 'r') as comp_in:
                    temp_out.write(comp_in.read())

                # Remove the temporary compressed file
                os.remove(compressed_file)

    # Run the page-index.py function on the combined temp file
    extract_and_sort(temp_file, output_file)

    # Remove the temp file
    os.remove(temp_file)


# Ensure that the script can be run as a standalone program.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process multiple .src files, compress them, and create an index.")
    parser.add_argument("pagesfolder", help="The folder containing the .src files.")
    parser.add_argument("-o", "--output", help="The output file to write the index to.")
    
    # parse the command-line arguments and store them in args.
    args = parser.parse_args()

    # Call the main() function.
    main(args.pagesfolder, args.output)
