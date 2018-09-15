import praw #Reddit API
import urllib
import config
import pickle
import shutil #remove files
from PIL import Image
import os

# Retrieves images and metadata from Reddit
def get_data():
   clean_storage() # deletes previously downloaded pictures
   cats = run_reddit() # cats is a Subreddit object which contains desired recent posts
   get_metadata(cats) # retrieves post metadata

##### Helper Functions #####

# Remove old pictures from storage file
def clean_storage():
   print("Cleaning picture storage...")
   assure_path_exists(config.STORAGE_PATH)
   fileList = os.listdir(config.STORAGE_PATH)
   try:
       os.remove(config.BINARY_FILE)
   except FileNotFoundError:
       pass

   for fileName in fileList:
      os.remove(config.STORAGE_PATH+"/"+fileName)
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
                 "CatsInBusinessAttire","CatCircles","CatPictures","SupermodelCats"]
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
            write_tuple(metadata)
            print("Post stored successfully")
            successCounter += 1
         except:
            print("Storage error occured")
            continue

# Formats comments into single line of HTML code to be directly inserted
def get_html_coms(comments):
   all_comments = """<font size="3">"""
   for i,com in enumerate(comments):
      if i == 4: #this value denotes number of desired comments to capture
         break
      if len(com.body)<300: #Restricts comments to desired length
         all_comments += "\"" + com.body + "\"<br> - /u/"
         all_comments += "" + com.author.name + "<br><br><br>"
   all_comments += "</font>"

   return all_comments

# Downloads image from url and returns file_path to image
def get_pic_path(url):
   store_file_path = config.STORAGE_PATH + "/"
   filename = url.split('/')[-1] # uses last part of address as file name
   file_path = store_file_path + filename

   try:
      urllib.request.urlretrieve(url, file_path)
      basewidth = 300
      with Image.open(file_path) as img:
         wpercent = (basewidth/float(img.size[0]))
         hsize = int((float(img.size[1])*float(wpercent)))
         img = img.resize((basewidth,hsize), Image.ANTIALIAS)
         img.save(file_path)
      return file_path
   except:
      print("Image download error occured")

def write_tuple(tuple):
    with open(config.BINARY_FILE, 'ab+') as file:
        pickle.dump(tuple, file)
