import requests
from bs4 import BeautifulSoup
import re
import sys
import os
import individual_album

def get_id_list(url):
    try:
        page = requests.get(url).text
    except Exception as e:
        print(e)
        sys.exit(0)
    soup = BeautifulSoup(page, 'html.parser')
    target_style = "border:1px solid #a0a0a0; background:#ffffff;"
    target_text = soup.find_all('table', {'style':target_style})
    target_text_str = str(target_text[0])
    target_text_str = target_text_str.replace("\n", " ")
    try:
        result = re.findall(r'album\.asp\?id=(.*?)"', target_text_str)
    except AttributeError as a:
        print(a)
        
    for item in result:
        if "#buymusic" in item:
            result.remove(item)

    for item in result:
        individual_album.grab_content(item)

if __name__ == "__main__":
    url = "http://www.progarchives.com/top-prog-albums.asp?ssubgenres=&salbumtypes=1&syears=&scountries=&sminratings=0&smaxratings=0&sminavgratings=0&smaxresults=250&x=0&y=0#list"
    if not os.path.isdir("csv_output"):
        os.mkdir("csv_output")
    get_id_list(url)
    
