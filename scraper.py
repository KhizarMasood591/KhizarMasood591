import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json
from json import JSONDecodeError
import re


head = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"
}




def get_html(prpty: str, arrival_date: datetime, departure_date: datetime, discount: float=0.0, adults: int= 2):
    fmt_arrvl = arrival_date.strftime('%Y-%m-%d')
    fmt_dep = departure_date.strftime('%Y-%m-%d')
    los = (departure_date - arrival_date).days
    if prpty == 'DesertRock':
        url = f"https://reservations.desertrock.sa/rates-room1?hotel=62782&arrival={fmt_arrvl}\
            &rooms=1&nights={los}&adults%5B1%5D=2&children%5B1%5D=0&infants%5B1%5D=0&code="
    if prpty == 'TBH':
        url = f"https://reservations.turtlebayhotel.sa/rates-room1?hotel=62781&arrival={fmt_arrvl}&\
            departure={fmt_dep}&rooms=1&adults%5B1%5D={adults}&children%5B1%5D=0&adults%5B2%5D={adults}&\
                children%5B2%5D=0&adults%5B3%5D={adults}&children%5B3%5D=0&adults%5B4%5D={adults}&\
                    children%5B4%5D=0&adults%5B5%5D={adults}&children%5B5%5D=0&code="
    if prpty == 'Shebara':
        url = url = f"https://reservations.shebara.sa/en/rates-room1?hotel=62780&arrival={fmt_arrvl}&\
            departure={fmt_dep}&rooms=1&adults%5B1%5D=2&children%5B1%5D=0&adults%5B2%5D=2&\
                children%5B2%5D=0&adults%5B3%5D=2&children%5B3%5D=0&adults%5B4%5D=2&\
                    children%5B4%5D=0&adults%5B5%5D=2&children%5B5%5D=0&codeType=default&code="
    response = requests.get(url, headers=head)
    html = response.text
    return parse_html(
        html,
        prpty,
        arrival_date,
        departure_date,
        discount
    )



def parse_html(html: str, prpty: str, check_in: datetime, check_out: datetime, discnt: float) -> pd.DataFrame:
    schema = {
        'check_in':[],
        'check_out':[],
        'room_type':[],
        'rate_name':[],
        'rate':[],
        'property':[],
    }
    soup = BeautifulSoup(html, 'html.parser')
    if prpty == 'TBH':
        locate_data = soup.select('script')[2].text
        data = '{' + locate_data[locate_data.find("'event'"):].split(");")[0].replace("\'", "\"")
        try:
            json_data = json.loads(data)
            rates = json_data['ecommerce']['items']
            for rate in rates:
                schema['check_in'].append(check_in.strftime("%m/%d/%Y"))
                schema['check_out'].append(check_out.strftime("%m/%d/%Y"))
                schema['room_type'].append(rate['item_category2'])
                schema['rate_name'].append(rate['item_name'])
                schema['rate'].append(float(rate['price']))
                schema['property'].append(rate['affiliation'])
        except JSONDecodeError:
            pass
    if prpty == 'DesertRock' or prpty == "Shebara":
        rooms = soup.select("section.room-with-rates-wrapper")
        for room in rooms:
            rates = room.select('div.rate-container')
            for rate in rates:
                rate_name = rate.select_one("div.rate-name h2").text.strip()
                price = rate.select_one("a.select-rate-btn").attrs['p3qa-room-price']
                price = re.sub('[\ue900,]','',price)
                room_name = room.select_one("h2.roomName__color").text.strip()
                schema['check_in'].append(check_in.strftime("%m/%d/%Y"))
                schema['check_out'].append(check_out.strftime("%m/%d/%Y"))
                schema['room_type'].append(room_name)
                schema['rate_name'].append(rate_name)
                schema['rate'].append(float(price))
                schema['property'].append(prpty)
    df = pd.DataFrame(schema)
    df_wholesale = df.copy()
    df['rate_type'] = 'Published'
    df_wholesale['rate'] = df_wholesale['rate'] * (1-0.1735)
    df_wholesale['rate_type'] = 'Wholesale'
    df = pd.concat([df,df_wholesale], axis=0)
    add_rate_names = {
        'Multiproperty 5 Nights':0.2,
        'Multiproperty 6 Nights':0.3,
        'Discounted':discnt/100,
    }
    for rate, discount in add_rate_names.items():
        df_bar = df[(df['rate_name'] == 'Villa Rate Including Breakfast') | (df['rate_name'] == 'Room Rate with Breakfast')]
        df_bar['rate_name'] = rate
        df_bar['rate'] = df_bar['rate'] * (1-discount)
        df_bar['rate_type'] = 'Discounted'
        df = pd.concat([df, df_bar])
    return df
