import praw #Reddit API
import urllib
import config
import csv
import shutil #remove files
from PIL import Image
from resizeimage import resizeimage
import os

# Retrieves images and metadata from Reddit
def get_images():
   clean_storage() # deletes previously downloaded pictures
   cats = run_reddit() # cats is a Subreddit object which contains desired recent posts
   get_metadata(cats) # retrieves post metadata


##### Helper Functions #####
   
# Remove old pictures from storage file
def clean_storage():
   print("Cleaning picture storage...")
   assure_path_exists(config.STORAGE_PATH)
   fileList = os.listdir(config.STORAGE_PATH)
   for fileName in fileList:
      os.remove(config.STORAGE_PATH+"/"+fileName)
   with open(config.CSV, "w") as empty: # Removes old CSV data
      pass
   print("Storage cleaned.")
   
   
# Creates a directory for storing pictures if it does not already exist
def assure_path_exists(path):
   direc =(path)
   if not os.path.isdir(direc):
      os.makedirs(direc)
      print("Directory %s created." %direc)
      

# Initializes Reddit instance using bot's params
def run_reddit():
   print("Retrieving posts")
   reddit = praw.Reddit(client_id = config.BOT_ID,
                        client_secret = config.CLIENT_SECRET,
                        username = config.USERNAME,
                        password = config.PASSWORD,
                        user_agent = config.USER_AGENT)

   # Initializes Subreddit instance from multiple subreddits
   subreddits = ["cats","MEOW_IRL","Kittens","TuckedInKitties","Floof",
                 "CatsInBusinessAttire","CatCircles","CatPictures"]
   cats = reddit.subreddit('+'.join(subreddits)).top('day', limit=30)
   return cats


# Retrieves and stores all relevant metadata
def get_metadata(cats): #Takes a Subreddit object as an argument
   successCounter = 0
   for post in cats:
      if successCounter == 10:
         break
      if(post.url.endswith('.jpg')):
         url = str(post.url)
         title = str(post.title)
         author = str(post.author)
         pic_path = get_pic_path(url)
         comments = get_html_coms(post.comments)
         metadata = (url, title, author, pic_path, comments)
         
         try:
            store_to_csv(metadata)
            print("Post stored to CSV")
            successCounter += 1
         except:
            print("Storage error occured")
            continue

# Formats comments into single line of HTML code to be directly inserted        
def get_html_coms(comments):
   all_comments = """<font size="3">"""
   for i,com in enumerate(comments):
      if len(com.body)<300: #Restricts comments to desired length
         all_comments += "\"" + com.body + "\"<br> - /u/" 
         all_comments += "" + com.author.name + "<br><br><br>"
      if i == 4: #this value denotes number of desired comments to capture
         break
   all_comments += "</font>"

   return all_comments
   
# Downloads image from url and returns file_path to image
def get_pic_path(url):
   store_file_path = ".\\daily_pics\\"
   filename = url.split('/')[-1] # uses last part of address as file name
   file_path = store_file_path + filename
   
   try:
      urllib.request.urlretrieve(url, file_path)
      with open(file_path,'rb') as f:
         with Image.open(f) as image:
            cover = resizeimage.resize_cover(image, [350,350], validate=False)
            cover.save(file_path, image.format)
      return file_path
   except:
      print("Image download error occured")
      return -1 # Flag that error occured

# Stores metadata into csv file
def store_to_csv(post_tuple):
   csv_file = config.CSV
   with open(csv_file, 'a', newline='') as o:
      writer = csv.writer(o)
      writer.writerow(post_tuple)
