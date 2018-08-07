import requests
from bs4 import BeautifulSoup

quote_url = 'https://www.brainyquote.com/quote_of_the_day'

# Generates body of Email Message
def generate_html(image_html_list, title_list, author_list, top_com_list):
    print('Generating HTML')

    quote = get_quote()
    quote_url_html = "<a href=" +"\"" + quote_url + "\"" + ">BrainyQuote - Quote of the Day</a>"

    # Creates blocks of html code for every image
    blocks = []
    for i,(img_code, title, author, comments) in enumerate(zip(image_html_list, title_list, author_list, top_com_list)):
        blocks.append(make_image_block(i, img_code, title, author, comments))

    with open("templates/email_template.html", "r") as file:
        template = file.read()
        html = template.format(quote, quote_url_html, *blocks)
        return html


########## HELPER FUNCTIONS #############

# Creates a block of html code containing the arguments
def make_image_block(counter, img_code, title, author, comments):
	with open("templates/email_image_table_template.html", "r") as file:
		image_snippet = image_html(counter, img_code, comments)
		temp = file.read()
		html = temp.format(title, author, image_snippet)
		return html

# Formats image and comments into HTML snppet to return
def image_html(counter, img_code, comments):
    if counter % 2 == 0: # Alternates images on either side of table
        table = """
                <td width="50%" align="center">""" + str(img_code) + """</td>
                <td width="50%" align="center">""" + comments + """</td>
                """
    else:
        table = """
                <td width="50%" align="center">""" + comments + """</td>
                <td width="50%" align="center">""" + str(img_code) + """</td>
                """
    return table

# Retrieves Daily Quote
def get_quote():
    cont = requests.get(quote_url).content
    soup = BeautifulSoup(cont, 'html.parser')
    class_var = "p-qotd bqPhotoDefault bqPhotoDefaultFw img-responsive delayedPhotoLoad"
    image = soup.find('img', {'class': class_var})
    # print(soup)
    return(str(image.get('alt', '')))
