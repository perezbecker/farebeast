# FareBeast #

------------------------------------

## Overview ##

This GitHub repository contains the source files of FareBeast.com 

FareBeast is an automated airfare monitor that finds optimal travel dates and ticket purchasing times for trips with flexible schedules.

It is developed in Python and uses the headless Qt browser to scrape AJAX-based flight aggregators hourly for dozens of travel-date combinations for each trip. An optimal stopping algorithm determines best purchasing times for the cheapest travel dates of each trip and alerts users via email/SMS. 

The alert system outperforms that of KAYAK, sending a fraction of the emails and recommending fares that are up to 30% lower (never higher, as FareBeast searches include KAYAK).

Source files for the interactive front-end using Flask and Twitter Bootstrap are also included.



## File Description ##

- `airalert.py`: Optimal stopping algorithm that determines if users should be alerted based on fare histories.
- `airmail.py`: Sends alert emails to users. 
- `airmail_test.py`: Test version of airmail.py to verify that gmail is not blocking remote server.
- `airplot.py`: Generates plots of fare histories for website/emails.
- `create_database.sql`: Creates MySQL database used by Farebeast.
- `farebeast_functions.py`: Contains functions common to many components.
- `farebeast_scrape.py`: Scrapes flight aggregators for fares. Calls `get_expedia.py` and `jw_bing.py`.
- `fb-backup`: Creates backups of FareBeast MySQL database, which are transferred to a safe location.
- `frontend.py`: Flask web framework.
- `get_expedia.py`: Auxiliary file for scraping Expedia.
- `gmailbeast.py`: Auxiliary file for sending alerts via gmail.com.
- `jw_bing.py`: Auxiliary file for scraping Bing/KAYAK.
- `kayak_exact_daily.txt`: Daily KAYAK alerts for tracked flights (to compare with FareBeast alerts).
- `load_flightqueue.py`: Loads flight queue generated by users on farebeast.com to the MySQL database.
- `reload_users.py`: (Re)loads users into MySQL database.
- `simple.conf`: Configuration file for Supervisor (handles the website).
- `smsbeast.py`: Auxiliary file for sending alerts via SMS using an SMS email gateway.
- `t_every1h`: CRON script to hourly scrape for all flights, crate database backup, run the optimal stopping algorithm, create plots, and send alerts.  
- `webfunctions.py`: Contains functions used in the webapp.
- `/static/`: Twitter Bootstrap CSS, javascript, images, fonts, plots, airport data, etc.
- `/templates/`: html templates for webapp. 


------------------------------------

## General Remarks ##

FareBeast was developed as an Insight Data Science project during January of 2014. If you have any questions about
this software or how to implement it, please don't hesitate in contacting me. Feel free track flights on FareBeast.com -- it will save you money on your next flight!
