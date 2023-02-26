#!venv/bin/python
import os
from glob import glob

dir_root = './sample-content'

# Define the file extensions to search for
extensions = (".md", ".yaml", ".csv")
skip_files = ('corpus.csv')

# Generate the list of file paths
file_paths = []
for root, dirs, files in os.walk(dir_root):
    for ext in extensions:
        for file in glob(os.path.join(root, "*" + ext)):
          if os.path.basename(file) in skip_files:
              continue
          file_paths.append(file)

# Write the list of file paths to a file
with open("corpus_source_files.txt", "w") as f:
    for file_path in file_paths:
        f.write(file_path + "\n")