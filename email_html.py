import requests
from bs4 import BeautifulSoup

quote_url = 'https://www.brainyquote.com/quote_of_the_day'

# Generates body of Email Message
def generate_html(image_html_list, title_list, author_list, top_com_list):
    print('Generating HTML')
    
    quote = get_quote()
    quote_url_html = "<a href=" +"\"" + quote_url + "\"" + ">BrainyQuote - Quote of the Day</a>"

    # Creates blocks of code for every image
    blocks = []
    for i,(img_code, title, author, comments) in enumerate(zip(image_html_list, title_list, author_list, top_com_list)):
        blocks.append(make_block(i, img_code, title, author, comments))     
        
    with open("html_template.html", "r") as file:
        template = file.read()
        html = template.format(quote, quote_url_html, *blocks)
        return html   


########## HELPER FUNCTIONS #############
    
# Creates a block of html code containing the arguments 
def make_block(counter, img_code, title, author, comments):
    block = """
        <table class="image" align="center" bgcolor="#FFFFFF" width="80%">
            <caption align="top"><b><font size="5">""" + str(title) + """
                - /u/""" + str(author) + """
            </font></b></caption><br>
    """
        
    block = insert_image(block, counter, img_code, comments) + "</table><br><br>"
    return block


# This function causes images to display on alternating sides of the email message
def insert_image(block, counter, img_code, comments):
    if counter % 2 == 0:
        block += """<tr><td style="padding:0 50px 0 50px;">""" + str(img_code) + """</td>
                    <td align="center">""" + comments + """</td>
                </tr>"""
    else:
        block += """<tr><td align="center">""" + comments + """</td>
                        <td style="padding:0 50px 0 50px;">""" + str(img_code) + """</td>
                </tr>"""
    return block

# Retrieves Daily Quote
def get_quote():
    cont = requests.get(quote_url).content
    soup = BeautifulSoup(cont, 'html.parser')
    image = soup.find('img', {'class': "p-qotd bqPhotoDefault bqPhotoDefaultFw img-responsive"})

    return(str(image.get('alt', '')))
