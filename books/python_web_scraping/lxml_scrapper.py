from cmath import log
import logging
from webbrowser import get
from lxml.html import fromstring, tostring
from lxml.etree import ParseError
import requests
from lago_logs import logs_lake
import cssselect


# Start logging structure - Append the current logger to the logger var
logs_lake()
logger = logging.getLogger()


def parse_html (html:str) -> str:
    """
    Receives a string and returns a valid HTML file
    @param 
    html -> Html text to be parsed 
    @return 
    valid_html -> Valid HTML file.  
    """
    valid_html = None
    try: 
        logger.debug('Parsing HTML in parse_html.')
        tree = fromstring(html=html)
        valid_html = tostring(tree, pretty_print=True)
    except ParseError as err:
        logger.error(f'Error parsing HTML: {err}')
        raise err('Error while validating the HTML in parse_html') 
    logger.debug('Html parsed successfully.')
    return valid_html


def extract_urls(html:str) -> list:
    logger.debug(html)
    tree = fromstring(html=html)
    links_list= tree.xpath('//a[contains(@href,"http")]/@href')
    founded_links = []
    logger.debug(f'Founded {len(links_list)} <a> tags')
    for link in links_list:
        logger.debug(f'Started processing: {link}')
        founded_links.append(link)
    return founded_links

def download_url (url:str, user_agent='wswp', num_retries=2, proxies=None) -> str:
    """
    Download a given URL and return the HTML
    @params 
    url -> Teh url to be downloaded 
    user_agent -> The user agent to be used, default is wswp
    num_reties -> How many retries to do when a 5XX error happens
    proxies -> Proxies to be used
    @return 
    html -> the URL page in HTML 
    """
    headers = {'User-Agent' : user_agent}
    try:
        resp = requests.get(url, headers=headers, proxies=proxies)
        html = resp.text      
        if resp.status_code >=400:
            logger.error(f'Error getting the page: {resp.text}')
            html = None
        if num_retries and 500 <= resp.status_code < 600:
            return download_url(url, num_retries=(num_retries-1))
    except requests.exceptions.RequestException as e:
        logger.error(f'Error getting the URL {e.reason}')
        html = None 
    return html



# perform some tests (manually)
if __name__ == '__main__':
    URL='https://www.google.com'
    html = download_url(URL,num_retries=4)
    proper_html = parse_html(html=html)
    url_list = extract_urls(proper_html)
    print(url_list)
