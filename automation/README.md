# Notebooks Table Automation

This directory contains the necessary files to automatically generate the notebooks table in the main README.md file.

## How It Works

1. The `notebooks-table-data.csv` file contains the data for all notebooks.
2. The `autogenerate_notebooks_table.py` script reads this CSV file and updates the main README.md file with a generated table.
3. The README.md file contains special marker comments to designate where the table should be inserted.

## How to Add a New Notebook

Follow these steps to add a new notebook:

1. Add your new `.ipynb` notebook file to the `notebooks` directory.
2. Add a new entry to the `notebooks-table-data.csv` file with the following information:
   - `title`: The display title for your notebook
   - `notebook_filename`: The filename of your notebook
   - `colab_link`: The link to your notebook in Colab
   - `resources`: Markdown-formatted links to datasets, models, etc.
   - `paper_link`: Link to the relevant research paper
   - `paper_title`: Title of the research paper
   - `repo_link`: Link to the relevant GitHub repository
   - `repo_name`: Name of the repository

3. Run the automation script:
   ```bash
   python3 automation/autogenerate_notebooks_table.py
   ```

4. The main README.md file will be updated automatically with your new notebook entry.

5. Commit and push your changes:
   ```bash
   git add notebooks/your_new_notebook.ipynb
   git add automation/notebooks-table-data.csv
   git add README.md
   git commit -m "Add new notebook: Your Notebook Title"
   git push
   ```

## Notes

- The script looks for markers `<!-- NOTEBOOKS_TABLE_START -->` and `<!-- NOTEBOOKS_TABLE_END -->` in the README.md file to know where to insert the table.
- If the markers don't exist, the script will try to add them after the "## Notebooks" heading.
- Make sure to follow the CSV format exactly to ensure the table is generated correctly.

<!-- NOTEBOOKS_TABLE_START -->
...table content...
<!-- NOTEBOOKS_TABLE_END --> 