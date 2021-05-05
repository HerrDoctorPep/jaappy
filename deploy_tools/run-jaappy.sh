#! /bin/bash
export SQL_USER=""
export SQL_WW=""
cd /home/pubuntu/scheduled-tasks/jaappy

# Run the scraping script
/home/pubuntu/venv/base/bin/python /home/pubuntu/scheduled-tasks/jaappy/MainJaap.py

# Run the script that writes to the database
/home/pubuntu/venv/base/bin/python /home/pubuntu/scheduled-tasks/jaappy/db/clean_df_write_db.py

# Mail the log file
date_string=$(date "+%Y%m%d")
mail -s "Jaappy log of the day" xxxxxxxxxx@xxxxxxx.xxx < /home/pubuntu/scheduled-tasks/jaappy/data/logs/log_${date_string}.txt