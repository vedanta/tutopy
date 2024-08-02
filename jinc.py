#!/usr/bin/env python3
"""
JINC: Jupyter Interactive Notebook Creator

This script converts a Python source file with specially formatted comments
into a Jupyter notebook (.ipynb) file.

J: Jupyter
I: Interactive
N: Notebook
C: Creator
"""

import nbformat as nbf
import argparse
import sys
import os

def create_notebook_cells(script):
    cells = []
    current_cell = {"type": None, "content": []}
    description = None

    for line in script.split('\n'):
        if line.startswith('#  DESCRIPTION'):
            description = line[14:].strip()  # Extract description
            continue
        elif line.startswith('# MARKDOWN CELL'):
            if current_cell["type"]:
                cells.append(current_cell)
            current_cell = {"type": "markdown", "content": []}
        elif line.startswith('# CODE CELL'):
            if current_cell["type"]:
                cells.append(current_cell)
            current_cell = {"type": "code", "content": []}
        else:
            if current_cell["type"] == "markdown":
                current_cell["content"].append(line.lstrip('# '))
            else:
                current_cell["content"].append(line)

    if current_cell["type"]:
        cells.append(current_cell)

    return cells, description

def create_notebook(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            script_content = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        sys.exit(1)
    except IOError:
        print(f"Error: There was an issue reading the file '{input_file}'.")
        sys.exit(1)

    # Create a new notebook
    nb = nbf.v4.new_notebook()

    # Parse the script and create cells
    cells, description = create_notebook_cells(script_content)

    # Add description as the first markdown cell if available
    if description:
        nb.cells.append(nbf.v4.new_markdown_cell(f"# Description\n\n{description}"))

    # Add cells to the notebook
    for cell in cells:
        if cell["type"] == "markdown":
            nb.cells.append(nbf.v4.new_markdown_cell('\n'.join(cell["content"])))
        elif cell["type"] == "code":
            nb.cells.append(nbf.v4.new_code_cell('\n'.join(cell["content"])))

    # Write the notebook to a file
    try:
        nbf.write(nb, output_file)
        print(f"Jupyter notebook '{output_file}' has been created successfully.")
    except IOError:
        print(f"Error: There was an issue writing to the file '{output_file}'.")
        sys.exit(1)

def get_default_output_filename(input_file):
    # Get the base name of the input file (without directory)
    base_name = os.path.basename(input_file)
    # Split the base name into name and extension
    name, _ = os.path.splitext(base_name)
    # Return the name with .ipynb extension
    return f"{name}.ipynb"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JINC: Create a Jupyter notebook from a Python script.")
    parser.add_argument("input_file", help="The input Python script file")
    parser.add_argument("-o", "--output", 
                        help="The output Jupyter notebook file (default: input_filename.ipynb)")
    
    args = parser.parse_args()

    # If output file is not specified, use the input filename with .ipynb extension
    if not args.output:
        args.output = get_default_output_filename(args.input_file)

    create_notebook(args.input_file, args.output)