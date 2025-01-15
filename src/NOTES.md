# Notes about the files in this directory

## ./searchJournal.py

- Performs an automated search of journals
- Journals are classes within the ./journals directory
- Raw output from searches is returned
- Currently only PLOS is supported
  - Must support at least Science and Nature - Currently working on Science -
    TOS of Science prevent automatic scraping. A message regarding this and
    explaining why no tool is provided will be made when the user selects the
    Science option. Links to the appropriate pages will be made availible at the
    bottom of the notice.
  - Done
- Search queries and relevant years stored in ./search/__init__.
  - See how many files depend upon this path and migrate these to file specific
    global variables
  - Only used in this file. These will be migrated to the top of the file
  - Done
