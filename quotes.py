import requests
from bs4 import BeautifulSoup

daily_quote = ''
url = 'https://www.brainyquote.com/quote_of_the_day'

def get_quote():
    cont = requests.get(url).content
    soup = BeautifulSoup(cont, 'html.parser')
    image = soup.find('img', {'class': "p-qotd bqPhotoDefault bqPhotoDefaultFw img-responsive"})

    return(str(image.get('alt', '')))



