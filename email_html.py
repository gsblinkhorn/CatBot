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

    block = start_table(title, author)    
    block = insert_image(block, counter, img_code, comments)
    block = add_border(block) 
    
    return block

# Creates table, adds title and author
def start_table(title, author):
    block = """
            <table class="image" align="center" bgcolor="#FFFFFF" width="100%">
                <tr>
                    <th colspan="2"><b><font size="5">""" + str(title) + """
                        - /u/""" + str(author) + """
                    </font></b></th>
                </tr>
            """
    return block
    

# Add black border to block
def add_border(block):
    block = """ 
            <table border="3px" cellpadding="0" cellspacing="0" width="80%">
            """ + block + """
            </table><br><br>"""
    return block
    
# Adds an image and comments to a given table and closes the table
def insert_image(table, counter, img_code, comments):
    if counter % 2 == 0: # Alternates images on either side of table
        table += """
                <tr>
                    <td align="center" style="padding:0 50px 0 50px;">""" + str(img_code) + """</td>
                    <td align="center">""" + comments + """</td>
                </tr>
                </table>
                """
    else:
        table += """
                <tr>
                    <td align="center">""" + comments + """</td>
                    <td style="padding:0 50px 0 50px;">""" + str(img_code) + """</td>
                </tr>
                </table>
                """
    return table

# Retrieves Daily Quote
def get_quote():
    cont = requests.get(quote_url).content
    soup = BeautifulSoup(cont, 'html.parser')
    image = soup.find('img', {'class': "p-qotd bqPhotoDefault bqPhotoDefaultFw img-responsive"})

    return(str(image.get('alt', '')))
