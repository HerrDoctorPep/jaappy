#! /bin/bash
export SQL_USER=""
export SQL_WW=""
cd /home/pubuntu/scheduled-tasks/jaappy
/home/pubuntu/venv/base/bin/python /home/pubuntu/scheduled-tasks/jaappy/MainJaap.py
/home/pubuntu/venv/base/bin/python /home/pubuntu/scheduled-tasks/jaappy/db/clean_df_write_db.py