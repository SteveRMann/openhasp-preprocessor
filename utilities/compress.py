"""
compress the unnecessary whitespace from a jsonl file

Usage:
python compress.py inputfile outputfile
 
"""

import re
import sys

# Check if a command-line argument has been provided
if len(sys.argv) < 3 or sys.argv[1] in ['help', '?']:
    print('Usage: python compress.py inputfile outputfile')
    sys.exit(1)

# Get the input file and output file from the command-line arguments
infile, outfile = sys.argv[1], sys.argv[2]


with open(infile, 'r') as f:
    content = f.read()

content = re.sub(r',\r?\n', ',', content) # This replaces a comma followed by a newline with just a comma
content = re.sub(r',  ', ',', content) # This replaces a comma followed by 2-spaces with just a comma
content = re.sub(r', ', ',', content) # This replaces a comma followed by a space with just a comma
content = re.sub(r',\n  ', ',', content)  # New substitution rule This replaces a comma followed by a newline and two spaces with just a comma
content = re.sub(r'\r?\n\r?\n', '\r\n', content)  # This replaces two consecutive newlines with a single newline
content = re.sub(r'{\r?\n', '{', content) # This replaces a curly brace { followed by a newline with just a curly brace {
content = re.sub(r'\( ', '{', content) # This replaces an open parenthesis ( followed by a space with a curly brace {
content = re.sub(r'\r?\n}', '}', content) # This replaces a newline followed by a curly brace } with just a curly brace }

# Remove all blank lines
content = re.sub(r'^\s*$', '', content, flags=re.MULTILINE)

with open(outfile, 'w') as f:
    f.write(content)
