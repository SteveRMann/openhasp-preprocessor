# Merge all .src files in a folder into a single output file.
import os

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

# Test the function
merge_files('pages', 'pages-merged.src')
