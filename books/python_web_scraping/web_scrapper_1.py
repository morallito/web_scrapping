from cmath import e
import logging
from urllib.error import ContentTooShortError, HTTPError, URLError
import urllib.request
from lago_logs import logs_lake
import re

# Initialize logs 
logs_lake()

def download_url (url:str, num_retries=2, user_agent='wswp',charset='utf-8') -> str:
    """ 
    Download an URL that is given, retry to download it until retries limit is reached
    """
    logging.getLogger().debug(f'Downloading: {url}')
    request = urllib.request.Request(url)
    request.add_header('User-agent', user_agent) 
    try:
        logging.getLogger().debug(f'Starting to download the URL: {url}')
        resp = urllib.request.urlopen(url)
        cs = resp.headers.get_content_charset()
        if not cs:
            cs = charset
        html  = resp.read().decode(cs)
    except (URLError, HTTPError, ContentTooShortError) as e:
        logging.getLogger().error(f'Download error: {e.reason}')
        html = None
        if num_retries > 0:
            # If error is server side 5xx, retry
            logging.getLogger().error(f'Error on the request: {e}')
            if hasattr(e, 'code') and 500 <= e.code < 600:
                logging.getLogger().debug(f'Num retries: {num_retries}')
                return download_url(url, num_retries -1)
    return html


def crawl_sitemap(url):
    try: 
        sitemap = download_url(url)
        links = re.findall(r'<a href=[\'"]?([^\'" >]+)', sitemap)
        print(links)
        logging.getLogger().debug(f'Number of founded URLs {len(links)}')
    except Exception as error:
        logging.getLogger().error(str(e))
    for link in links:
        html = download_url(link)

crawl_sitemap('https://www.iagomoreira.com.br/')









