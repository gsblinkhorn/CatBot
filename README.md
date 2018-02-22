# Cat-Bot
'Cat-Bot' is a Python-powered (Python 3.6.4), Reddit-scraping application for automatically generating and emailing a cat-themed newsletter, 'The Feline Fanatic'. In order to run the program, download all files into a local directory. With some simple tweaks to the config.py file, the driver file will be ready to execute. If Python 3 is not installed, you will need to download and install that as well. [Download Python 3 here](https://www.python.org/downloads/). This program was designed on a Windows machine - Mac and Linux functionality not guaranteed. 

# config
### 'Trigger Image Download'
Boolean used to enable/disable the download step. Images are downloaded from Reddit into local directory 'config.STORAGE_PATH', and their metadata is stored in a csv file 'config.CSV'. All info is then embedded in the email body from the csv and local directory. With DOWNLOAD = False, the program will simply embed the data currently stored in the csv and local directory. Each download will overwrite the previous contents of these two files.

### 'Storage Paths'
Change the paths for each of the necessary storage structures - local directory and csv

### 'Known Emails & Mailing Lists'
Email addresses should be stored as strings. These addresses can then be stored in a list of addresses. This list will be what is passed to the program. 

### 'All Necessary Email Info'
USER & PASS are the username and password to the email account you wish to send from, stored as strings. Currently, the program is hard-coded to work with gmail accounts only. By default, gmail will prevent this bot from logging in. In order to bypass this security measure, you will need to allow less secure apps on your account ([Instructions here](https://support.google.com/accounts/answer/6010255?hl=en)). For this reason, I created a new gmail account solely to be used as the sender rather than use a personal one. 

# Running the Program
After downloading all files and setting up your config file, execute the driver.py file. Print-outs should appear in the terminal as the program executes. Upon successful completion, the email should be received by all addresses in your TO list. The program will terminate after successfully sending the email.
