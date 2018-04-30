import requests
from bs4 import BeautifulSoup

quote_url = 'https://www.brainyquote.com/quote_of_the_day'

# Retrieves Daily Quote
def get_quote():
    cont = requests.get(quote_url).content
    soup = BeautifulSoup(cont, 'html.parser')
    image = soup.find('img', {'class': "p-qotd bqPhotoDefault bqPhotoDefaultFw img-responsive"})

    return(str(image.get('alt', '')))


# Generates body of Email Message
def generate_html(image_html_list, title_list, author_list, top_com_list):
    print('Generating HTML')
    
    quote = get_quote()
    quote_url_html = "<a href=" +"\"" + quote_url + "\"" + ">BrainyQuote - Quote of the Day</a>"

    # Image HTML Generator 
    blocks = []
    for i,(img_code, title, author, comments) in enumerate(zip(image_html_list, title_list, author_list, top_com_list)):
        block = """
        <table class="image" align="center" bgcolor="#FFFFFF">
            <caption align="top"><b><font size="5">""" + str(title) + """
                - /u/""" + str(author) + """
            </font></b></caption><br>
        """
        
        block = make_img_html(block, i, img_code, comments) + "</table><br><hr>"
        blocks.append(block)
        

    with open("html_template.html", "r") as file:
        code = file.read()
        code = code.format(quote, quote_url_html, *blocks)
        return code   
    

# This function causes images to display on alternating sides of the email message
def make_img_html(block, counter, img_code, comments):
    if counter % 2 == 0:
        block += """<tr><td style="padding:0 50px 0 50px;">""" + str(img_code) + """</td>
                    <td align="center">""" + comments + """</td>
                </tr>"""
    else:
        block += """<tr><td align="center">""" + comments + """</td>
                        <td style="padding:0 50px 0 50px;">""" + str(img_code) + """</td>
                </tr>"""
    return block
