from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import datetime
import get_image
import smtplib
import csv
import config #email info 
import email_html #html body info


def generate_email():
    if(config.DOWNLOAD): #Boolean to bypass download step 
        get_image.get_images()
    
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

    # Extract contents of csv
    title_list = []
    author_list = []
    url_list = []
    jpg_path_list = []
    top_com_list = []
    with open(config.CSV, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            url_list.append(row[0])
            title_list.append(row[1])
            author_list.append(row[2])
            jpg_path_list.append(row[3])
            top_com_list.append(row[4])

    # Generate HTML code for images and add images to email message
    with open("logo_gif.gif", 'rb') as pic:
        msgImage = MIMEImage(pic.read())
        msgImage.add_header('Content-ID', '<logo>')
        msgRoot.attach(msgImage)

    with open("black_background.png", 'rb') as pic:
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

