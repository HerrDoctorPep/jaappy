# Setting up house scraping on server

## Required packages

* Python 3.8
* virtualenv + pip
* Git

## Required Python packages
See requirements.txt

## Running the script
Copy run-jaappy.sh to the directory /home/pubuntu/scheduled-tasks
Run the bash script run-jaappy.sh

## Add to crontab
Run 

    crontab -e

Add shell and schedule to the crontab:

    SHELL = /bin/bash
    0 13 * * * * /home/pubuntu/scheduled-tasks/run-jaappy.sh

## Folder structure
Not fully used... only 'data' 

/home/pubuntu/scheduled-tasks/jaappy
├── data
│   ├── logs
│   └── processed
├── docs
├── models
├── notebooks
├── __pycache__
├── references
├── reports
│   └── figures
└── src
    ├── data
    ├── features
    ├── models
    └── visualization
