# Imports
import argparse
import csv
from datetime import date, timedelta, datetime
import uuid
import sys
import os
from types import SimpleNamespace as Namespace

#from process_stats_function import process_stats
#from make_report_function import make_report_profit, make_report_inventory, make_report_revenue
#from sell_function import process_sell_instruction
#from print_helplist import print_helplist

# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'


# Your code below this line.
"""We need a class to set the date, so we can use it for buy functions"""
class setDates:
    def __init__(self, day):
        self.today = day
        self.yesterday = self.today+timedelta(days=-1)
        self.tomorrow = self.today+timedelta(days=1)
        self.fortnight_day = self.today+timedelta(days=2)
        self.today_str = self.today.strftime('%d%m%Y')
        self.yesterday_str = self.yesterday.strftime('%d%m%Y')
        self.tomorrow_str = self.tomorrow.strftime('%d%m%Y')
        self.fortnight_day_str = self.fortnight_day.strftime('%d%m%Y')

"""First we want to set the date. This can be the date for today,
    because we want to test the superpy we will set the date back.
    Thats why I make a function to reset the date."""
def get_referred_date(shift_number_of_days=0, reset='N'):
    #the first parameter is for to set the day backwords(or to the next day)
    #the second parameter is to reset the referred_day to system date
    f_get_date = None
    date_validated = 'N'
    try:
        f = open('./referred-date.txt', 'r')
        date_line = f.readline().lstrip()[0:10]
        f_get_date = datetime.strptime(date_line, '%d%m%Y')
        f.close()
    except:
        this_moment = datetime.now()
        this_moment_str = this_moment.strftime('%d%m%Y')
        f_get_date = datetime.strptime(this_moment_str, '%d%m%Y')
    if shift_number_of_days != 0:
        f_get_date = f_get_date+timedelta(shift_number_of_days)
    elif reset == 'Y':
        f_get_date = datetime.strptime(datetime.now().strftime('%d%m%Y'), '%d%m%Y')
    f = open('./referred-date.txt', 'w')
    f.write(f_get_date.strftime('%d%m%Y'))
    f.close()
    date_validated = 'Y'
    return f_get_date, date_validated

#print(get_referred_date(-1, 'N'))

"""Next step is to make a function to put things in the store. So what did you buy for in the supermarket.
   I called this function process_buy_instruction. It need the args and the dates parameter. 
   To test this i first will do it without args and dates en put my own parameters in it. 
   We use success to see if the function did successfully run."""

def process_buy_instruction(productname, dates, price, expirationdate):
    success= False
    max_id = uuid.uuid4() #makes a random ID
    product_name = productname.lower()
    field_names = ['ID', 'product_name', 'buy_date', 'buy_price', 'expiration_date', 'sold']
    dates = datetime.strptime(dates, '%Y-%m-%d')
    expiration_date = datetime.strptime(expirationdate, '%Y-%m-%d')
    dict={
        'ID': str(max_id), 
        'product_name': product_name, 
        'buy_date': dates.strftime('%d%m%Y'), 
        'buy_price': str(price).replace('.', ','), 
        'expiration_date': expiration_date.strftime('%d%m%Y'), 
        'sold': 'N'}
    
    file_exists = os.path.isfile('bought.csv')

    with open('bought.csv', 'a', newline="") as csvfile:
        bought_object = csv.DictWriter(csvfile, fieldnames=field_names)
        if max_id != 0:
            if not file_exists:
                bought_object.writeheader()
            bought_object.writerow(dict)
            success = True
             
    csvfile.close()
    return success


print(process_buy_instruction('milk', '2021-05-28', 0.40, '2021-05-30'))

def main():
    pass


if __name__ == '__main__':
    main()
