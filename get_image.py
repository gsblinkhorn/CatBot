import praw #Reddit API
import numpy as np
import pandas as pd
import urllib
import config
import csv
import shutil #remove files
from PIL import Image
from resizeimage import resizeimage
import os

# Creates a directory for storing pictures if it does not already exist
def assure_path_exists(path):
   direc =(path)
   if not os.path.isdir(direc):
      os.makedirs(direc)
      print("Directory %s created." %direc)

# Remove old pictures from storage file
def clean_storage():
   print("Cleaning picture storage...")
   assure_path_exists(config.STORAGE_PATH)
   fileList = os.listdir(config.STORAGE_PATH)
   for fileName in fileList:
      os.remove(config.STORAGE_PATH+"/"+fileName)
   print("Storage cleaned.")

def run_reddit():
   # Initializes Reddit instance using bot's params
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

# Retrieves images and metadata from Reddit
def get_images():
   
   cats = run_reddit(); # cats is a Subreddit object
   
   clean_storage();
   
 
   '''
   Information to Gather:
   #Individual Post Variables
   url - string, target image url
   title - string, title of post
   top_com - string, top comment on post
   tc_author - string, author of top comment

   #Lists for storing information
   url_list - list of urls
   title_list - list of titles
   author_list - list of authors
   top_com_list - list of top comments
   '''

   url_list = []
   title_list = []
   author_list = []
   top_com_list = []

   print("Retrieving pictures")
   for post in cats:
      if(post.url.endswith('.jpg')):
         try:
            url = str(post.url)
            title = str(post.title)
            author = str(post.author)
            comments = post.comments
         except: #If error occurs while gathering data, skip that post
            print("Post retrival error occured")
            continue

         #If no error occurs while retrieving information, store information
         url_list.append(url)
         title_list.append(title)
         author_list.append(author)
         all_comments = """<font size="3">"""

         #Formats comments into single line of HTML code to be directly inserted
         i=0
         for com in comments:
            if len(com.body)<300: #Restricts comments to desired length
               try:
                  com.body
                  com.author.name
               except:
                  print("Error retrieving comment")
                  continue
               all_comments += "\"" + com.body + "\"<br> - /u/" + com.author.name + "<br><br><br>"
               i += 1
            if i == 4: #this value denotes number of comments captured
               break
         all_comments += "</font>"

         #Appends finished comment HTML code into list
         top_com_list.append(all_comments)
         print("Post retrieved successfully")
               
   # Download/store images from url
   file_path_list = []
   store_file_path = ".\\daily_pics\\"

   for url in url_list:
      filename = url.split('/')[-1]#uses last part of address as file name
      file_path = store_file_path + filename
      try:
         urllib.request.urlretrieve(url, file_path)
         file_path_list.append(file_path)
         with open(file_path,'rb') as f:
            with Image.open(f) as image:
               cover = resizeimage.resize_cover(image, [350,350], validate=False)
               cover.save(file_path, image.format)
         print("Image downloaded successfully")
      except:
         print("Image download error occured")
         

   #Store all information into csv
   rows = zip(title_list, author_list, url_list, file_path_list, top_com_list)
   csv_file = config.CSV

   csv_counter = 0
   with open(csv_file, "w", newline='') as o:
      writer = csv.writer(o)
      for row in rows:
         try:
            writer.writerow(row)
            print("Image added to CSV")
            csv_counter += 1
         except:
            print("Image could not be saved to CSV")
         if csv_counter == 10: #this value denotes the desired number of pictures in message
            break
      print("Image Data saved to CSV")

