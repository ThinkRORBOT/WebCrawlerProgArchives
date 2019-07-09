from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys
from datetime import datetime
from dateutil import parser
import nlp

def get_stars(text_content):
    # finding the number of stars using attribute
    img_tag = text_content.find('img')['alt']
    star = img_tag.split(" ")[0]
    return star

def get_dict_list(target_text, epoch_time_list):
    dict_list = list()
    count = 1
    len_data = len(target_text)
    for text, time in zip(target_text, epoch_time_list):
        save_dict = {"comment":"", "stars":"", "epoch_time":time, "sentiment":""}
        save_dict["comment"] = text.get_text()
        print("Analysing %d comments out of %d comments" % (count, len_data))
        count = count + 1
        sentiment = nlp.get_sentiment(text.get_text())
        save_dict["sentiment"] = sentiment
        save_dict["stars"] = get_stars(text)
        dict_list.append(save_dict)
    return dict_list
    
def grab_user_date(soup):
    target_style = "margin-top:20px;"
    target_text = soup.find_all('div',  {'style':target_style})
    epoch_time_list = list()
    for text in target_text:
        output_text = text.get_text()
        # the date is in between the first comma and the pipe
        first_index = output_text.find(",")
        last_index = output_text.find("|")
        date_text = output_text[first_index+2:last_index].replace(",", "")
        
        try:
            dt = parser.parse(date_text)
            epoch = datetime(1970, 1, 1)
            epoch_time = (dt-epoch).total_seconds()
            epoch_time_list.append(epoch_time)
        except ValueError as v:
            print("cannot parse datetime object")
            print(v)
            sys.exit(0)
    return epoch_time_list


def grab_content(url, id):
    try:
        page = requests.get(url).text
    except Exception as e:
        print(e)
        sys.exit(0)
    soup = BeautifulSoup(page, 'html.parser')
    # get the comment div
    target_style = "line-height:1.4em;margin-left:155px;border-left: 1px dotted #dbd5c5;padding:5px 10px;"
    target_text = soup.find_all('div', {'style':target_style})
    epoch_time_list = grab_user_date(soup)
    # export to csv
    dict_list = get_dict_list(target_text, epoch_time_list)
    df = pd.DataFrame(dict_list)
    export_csv = df.to_csv('%d.csv'%(id), index = None, header=True)

if __name__ == "__main__":
    url = "http://www.progarchives.com/album-reviews.asp?id=1440"
    grab_content(url, id=1440)
