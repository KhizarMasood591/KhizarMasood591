from word import Word
from datetime import datetime, timedelta
from scraper import get_html
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')
from sqlalchemy import text


def get_rates(df: pd.DataFrame, rate_name: str, resort: str, los: int) -> list:
    df_filter_rate = df[df['rate_name'] == rate_name]
    if resort =='Shebara' or resort == 'DesertRock':
        df_filter_rate['rate']  = df_filter_rate['rate'] / los
        df_filter_rate['rate'] = df_filter_rate['rate'].astype('int')
    df_filter_rate['Total inc Tax'] = ((df_filter_rate['rate'] * los) * 1.05) * 1.15
    data = []
    row_order = {
        '1':['One Bedroom Beach Villa', 'Onebedroom Wadi Villa','Deluxe King Room'],
        '2':['Two Bedroom Beach Villa', 'Onebedroom Cliff Hanging Villa','Deluxe King Room with Garden View'],
        '3':['One Bedroom Overwater Villa', 'Onebedroom Mountain Cave Suite', 'Deluxe King Room with Sea View'],
        '4':['Two Bedroom Overwater Villa', 'Onebedroom Mountain Crevice Villa'],
        '5':['Twobedroom Wadi Villa'],
        '6':['Twobedroom Cliff Hanging Villa']
        }
    for i, row in df_filter_rate.iterrows():
        room_type = row['room_type'].replace('-','').strip()
        for key in row_order:
            if room_type in row_order[key]:
                row_no = int(key)
                room_rate = {
                    'roomType':room_type,
                    'roomPerNight':f'{int(row["rate"]):,}',
                    'roomRate': f'{int(row["Total inc Tax"]):,}',
                    'rowNo':row_no
                }
        data.append(room_rate)
    return data



def generate(resort:str,
         check_in: datetime,
         check_out: datetime,
         offer_type: str,
         rate_name: str,
         discount: float,
         guest_name: str,
         path: str,
         adult: int
         ):
    if rate_name != 'Discounted':
        discount = 0
    df = get_html(
        resort,
        check_in,
        check_out,
        discount,
        adult
        )
    los = (check_out - check_in).days
    if offer_type == 'Wholesale':
        rate_name = df[df['rate_type']=='Wholesale']['rate_name'].iloc[0]
        df = df[df['rate_type']=='Wholesale']
    else:
        df = df[df['rate_type'] != "Wholesale"]
    temp_docx = Word(path, resort)
    temp_docx.update_guest_name(guest_name)
    temp_docx.update_stay_dates(
        check_in.strftime('%d %b %Y'),
        check_out.strftime('%d %b %Y'),
        str(los)
        )
    temp_docx.update_offer_name(f"{int(discount)}% Discount Applied")
    rates = get_rates(
        df,
        rate_name,
        resort,
        los
    )
    temp_docx.update_rates_table(rates)
    name = temp_docx.save_files(
        f"{guest_name}-{check_in.strftime('%d %b %Y')}",
        offer_type
        )
    return name

