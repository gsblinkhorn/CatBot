from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import reddit_bot #image download module
import config #email info
import email_html #html body info
import datetime
import smtplib
import os
import pickle

def generate_email():
    if(config.DOWNLOAD): #Boolean to bypass download step
        reddit_bot.get_data()

    # Instance of Date
    now = datetime.datetime.now()

    # Create the root message and fill in headers
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = "The Feline Fanatic " + str(now.strftime("%m-%d-%Y"))
    msgRoot['From'] = config.FROM
    msgRoot['To'] = ", ".join(config.TO)
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText('This is the alternative plain text message.')
    msgAlternative.attach(msgText)

    # Load tuples
    tuples = []
    with open(config.BINARY_FILE, 'rb') as file:
        while True:
            try:
                tuples.append(pickle.load(file))
            except (EOFError):
                break

    url_list = []
    title_list = []
    author_list = []
    jpg_path_list = []
    top_com_list = []

    for tup in tuples:
        (url, tit, auth, jpg, top) = tup
        url_list.append(url)
        title_list.append(tit)
        author_list.append(auth)
        jpg_path_list.append(jpg)
        top_com_list.append(top)

    # Generate HTML code for background images and add images to email message
    with open("email_images/logo_gif.gif", 'rb') as pic:
        msgImage = MIMEImage(pic.read())
        msgImage.add_header('Content-ID', '<logo>')
        msgRoot.attach(msgImage)

    with open("email_images/black_background.png", 'rb') as pic:
        msgImage = MIMEImage(pic.read())
        msgImage.add_header('Content-ID', '<bback>')
        msgRoot.attach(msgImage)

    img_html_list = []
    for i, path in enumerate(jpg_path_list):
        # Create/store an html img tag with unqiue id
        img_html_list.append('<img src="cid:image' + str(i) + '">')

        # Retrieve image from path and create image instance
        with open(path, 'rb') as pic:
            msgImage = MIMEImage(pic.read())

        # Attach unique id to image instance and embed image within the message
        msgImage.add_header('Content-ID', '<image' + str(i) + '>')
        msgRoot.attach(msgImage)

    # Generate body of email in HTML format
    msgText = MIMEText(email_html.generate_html(img_html_list, title_list, author_list, top_com_list),'html')
    print("Sending email...")
    msgAlternative.attach(msgText)

    return msgRoot.as_string()
