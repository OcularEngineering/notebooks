#!/usr/bin/env python3
"""
Automatically generate the notebooks table in README.md from data in notebooks-table-data.csv.
Run this script whenever you add a new notebook to update the README.md file.
"""

import csv
import os
import re

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
CSV_FILE = os.path.join(SCRIPT_DIR, 'notebooks-table-data.csv')
README_FILE = os.path.join(ROOT_DIR, 'README.md')

# Table generation marker comments
START_MARKER = "<!-- NOTEBOOKS_TABLE_START -->"
END_MARKER = "<!-- NOTEBOOKS_TABLE_END -->"

def read_notebook_data():
    """Read the notebook data from the CSV file."""
    notebooks = []
    with open(CSV_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            notebooks.append(row)
    return notebooks

def convert_markdown_to_html(markdown_text):
    """Convert Markdown links to HTML links."""
    # Match Markdown links: [text](url)
    pattern = r'\[(.*?)\]\((.*?)\)'
    
    def replace_link(match):
        text = match.group(1)
        url = match.group(2)
        return f'<a href="{url}" target="_blank">{text}</a>'
    
    return re.sub(pattern, replace_link, markdown_text)

def generate_table(notebooks):
    """Generate the HTML table from the notebook data with proper borders."""
    table = []
    table.append('<table style="border-collapse: collapse; width: 100%; border: 1px solid #ddd;">')
    
    # Table header
    table.append('<thead>')
    table.append('<tr>')
    table.append('<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Notebook Title</th>')
    table.append('<th style="border: 1px solid #ddd; padding: 8px; text-align: center;">Colab Link</th>')
    table.append('<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Resources</th>')
    table.append('<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Publisher\'s Paper & Repo</th>')
    table.append('</tr>')
    table.append('</thead>')
    
    # Table body
    table.append('<tbody>')
    for notebook in notebooks:
        title = notebook['title']
        colab_link = notebook['colab_link']
        resources = convert_markdown_to_html(notebook['resources'])
        paper_link = notebook['paper_link']
        paper_title = notebook['paper_title']
        repo_link = notebook['repo_link']
        repo_name = notebook['repo_name']
        
        colab_badge = f'<a href="{colab_link}" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>'
        paper_ref = f'<a href="{paper_link}" target="_blank">{paper_title}</a>'
        repo_ref = f'<a href="{repo_link}" target="_blank">{repo_name}</a>'
        
        table.append('<tr>')
        table.append(f'<td style="border: 1px solid #ddd; padding: 8px;">{title}</td>')
        table.append(f'<td style="border: 1px solid #ddd; padding: 8px; text-align: center;">{colab_badge}</td>')
        table.append(f'<td style="border: 1px solid #ddd; padding: 8px;">{resources}</td>')
        table.append(f'<td style="border: 1px solid #ddd; padding: 8px;">{paper_ref}, {repo_ref}</td>')
        table.append('</tr>')
    
    table.append('</tbody>')
    table.append('</table>')
    
    return "\n".join(table)

def update_readme():
    """Update the README.md file with the generated table."""
    # Read the current README content
    with open(README_FILE, 'r') as file:
        content = file.read()
    
    # Check if the markers exist
    if START_MARKER not in content or END_MARKER not in content:
        # If markers don't exist, add them around the ## Notebooks section
        notebooks_heading_pattern = r"(## Notebooks\s*\n)"
        if re.search(notebooks_heading_pattern, content):
            content = re.sub(
                notebooks_heading_pattern,
                f"\\1\n{START_MARKER}\n{END_MARKER}\n",
                content
            )
        else:
            print("Error: Could not find '## Notebooks' heading in README.md")
            return False
    
    # Generate the new table
    notebooks = read_notebook_data()
    table = generate_table(notebooks)
    
    # Replace the content between the markers
    pattern = f"{START_MARKER}(.*?){END_MARKER}"
    replacement = f"{START_MARKER}\n{table}\n{END_MARKER}"
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Write the updated content back to the README
    with open(README_FILE, 'w') as file:
        file.write(updated_content)
    
    print(f"Successfully updated the notebooks table in {README_FILE}")
    return True

if __name__ == "__main__":
    update_readme() 