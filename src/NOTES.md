# Notes about the files in this directory

## ./searchJournal.py

- Performs an automated search of journals
- Journals are classes within the ./journals directory
- Raw output from searches is returned
- Currently only PLOS is supported
  - Must support at least Science and Nature
- Search queries and relevant years stored in ./search/__init__.py
  - See how many files depend upon this path and migrate these to file specific
    global variables
  - Only used in this file. These will be migrated to the top of the file
