from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_dict_list(target_text):
    dict_list = list()
    for text in target_text:
        save_dict = {"comment":""}
        save_dict["comment"] = text.get_text()
        dict_list.append(save_dict)
    return dict_list
    

def grab_content(url):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    target_style = "line-height:1.4em;margin-left:155px;border-left: 1px dotted #dbd5c5;padding:5px 10px;"
    target_text = soup.find_all('div', {'style':target_style})
    #print(type(target_text))
    print(target_text[0].get_text())
    dict_list = get_dict_list(target_text)
    df = pd.DataFrame(dict_list)
    export_csv = df.to_csv('output.csv', index = None, header=True)

if __name__ == "__main__":
    url = "http://www.progarchives.com/album-reviews.asp?id=1440"
    grab_content(url)
