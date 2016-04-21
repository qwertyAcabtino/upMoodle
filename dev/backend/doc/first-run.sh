#!/usr/bin/env bash
cd ..
#install python dependencies
sudo pip install -r requirements.txt
#init django stuff
bash updatedb
#provision database
sqlite3 db.sqlite3 ".read provision-database.sql"