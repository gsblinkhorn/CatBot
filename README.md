# Cat-Bot
'Cat-Bot' is a Python-powered (Python 3.6), Reddit-scraping application for automatically generating and emailing a cat-themed newsletter, 'The Feline Fanatic'. In order to run the program, clone this repository. With some simple tweaks to the config_sample.py file, the driver file will be ready to execute. If Python 3 is not installed, you will need to download and install that as well. [Download Python 3 here](https://www.python.org/downloads/). This program was designed on a Linux machine. You will need a Reddit bot account to login with and a gmail address to send the message from.

## Third-Party Libraries
- requests
- BeautifulSoup
- PRAW
- PIL

## config
Once you have downloaded config_sample.py, rename it to config.py. This will allow the rest of the scripts to access your configuration variables. .gitignore will ignore your config.py if you create a local repository, as well as the local directory and binary files which the program will create

### 'Trigger Image Download'
Boolean used to enable/disable the download step. Images are downloaded from Reddit into local directory 'config.STORAGE_PATH', and their metadata is stored in a binary file 'config.BINARY_FILE'. With DOWNLOAD = False, the program will simply embed the data currently stored in the binary file and local directory. Each download will overwrite the previous contents of these two files.

### 'Bot Parameters'
After creating your own Reddit bot ([Instructions Here](http://pythonforengineers.com/build-a-reddit-bot-part-1/)), store the necessary values here

### 'Known Emails & Mailing Lists'
Email addresses should be stored as strings. These addresses can then be stored in a list of addresses. This list will be what is passed to the program.

### 'All Necessary Email Info'
USER & PASS are the username and password to the email account you wish to send from, stored as strings. Currently, the program is hard-coded to work with gmail accounts only. By default, gmail will prevent this bot from logging in. In order to bypass this security measure, you will need to allow less secure apps on your account ([Instructions here](https://support.google.com/accounts/answer/6010255?hl=en)). For this reason, I created a new gmail account solely to be used as the sender rather than use a personal one.

## Running the Program
1 - Download all files into local directory

2 - Initialize your config file (Bot params, email params, mailing list)

3 - Run the driver.py file.

Print-outs should appear in the terminal as the program executes. Upon successful completion, the email should be received by all addresses in your TO list. The program will terminate after successfully sending the email.

## Set Script to Run Automatically
This script can be setup to run automatically on any computer with a reliable internet connection.  Rather than execute the driver file directly (python /path/to/file/driver.py), I created a bash script called job.sh that the crontab command executes instead (crontab command : * * * * * ~/job.sh).

### job.sh - Automatically trigger this script with a cron job
#!/usr/bin/env bash
cd ~/CatBot
python3 driver.py

