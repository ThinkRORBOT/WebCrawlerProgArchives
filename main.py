from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_stars(text_content):
    img_tag = text_content.find('img')['alt']
    star = img_tag.split(" ")[0]
    return star

def get_dict_list(target_text):
    dict_list = list()
    for text in target_text:
        save_dict = {"comment":"", "stars":""}
        save_dict["comment"] = text.get_text()
        save_dict["stars"] = get_stars(text)
        dict_list.append(save_dict)
    return dict_list
    

def grab_content(url):
    try:
        page = requests.get(url).text
    except Exception as e:
        print(e)
    soup = BeautifulSoup(page, 'html.parser')
    target_style = "line-height:1.4em;margin-left:155px;border-left: 1px dotted #dbd5c5;padding:5px 10px;"
    target_text = soup.find_all('div', {'style':target_style})
    #print(type(target_text))
    dict_list = get_dict_list(target_text)
    df = pd.DataFrame(dict_list)
    export_csv = df.to_csv('output.csv', index = None, header=True)

if __name__ == "__main__":
    url = "http://www.progarchives.com/album-reviews.asp?id=1440"
    grab_content(url)
