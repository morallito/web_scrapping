from cgitb import html
import logging
import requests
from lago_logs import logs_lake

logs_lake()

def download_url (url, user_agent='wswp', num_retries=2, proxies=None):
    headers = {'User-Agent' : user_agent}
    try:
        resp = requests.get(url, headers=headers, proxies=proxies)
        html = resp.text      
        html = None
        if resp.status_code >=400:
            logging.getLogger().error(f'Error getting the page: {resp.text}')
            html = None
        if num_retries and 500 <= resp.status_code < 600:
            return download_url
    except requests.exceptions.RequestException as e:
        logging.getLogger().error(f'Error getting the URL {e.reason}')
        html = None 

    return html