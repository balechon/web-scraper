import requests
import lxml.html as html
import os 
import datetime
from requests.api import request

from requests.models import Response

HOME_URL="https://www.elcomercio.com/"
XPATH_LINK_TO_ARTICLE ='//div[@class="article-highlighted__body"]/h3/a/@href'
XPATH_TITLE='//h1[@class="entry__title"]/text()'
XPATH_BODY='//div[@class="entry__content"]/p[not(@class)]//text()'
XPATH_SUMMARY='//p[@class="article-highlighted__description"]/text()'

def parsed_notice(link, today):
    try:
        response=requests.get(link)
        if response.status_code==200:
            notice= response.content.decode('utf-8')
            parsed=html.fromstring(notice)

            try:
                title=parsed.xpath(XPATH_TITLE)[0]
                title=title.replace('\"','')
                body= parsed.xpath(XPATH_BODY)
            except IndexError:
                return
            
            with open(f'{today}/{title}.txt','w',encoding='UTF-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write('\n\n')
                for p in body:
                    f.write(p)



        else:
            raise ValueError(f'Error :{response.status_code}')
    except ValueError as ve:
        print(ve)

def parse_home():
    try:
        response=requests.get(HOME_URL)
        if response.status_code==200:
            home= response.content.decode('utf-8')
            parsed=html.fromstring(home)
            links_to_notices=parsed.xpath(XPATH_LINK_TO_ARTICLE)
            summary=parsed.xpath(XPATH_SUMMARY)
        
            today =datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            for  idx,link in enumerate(links_to_notices): 
                parsed_notice(link,today)
        else:
            raise ValueError(f'Error :{response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()

if __name__=="__main__":
    run()