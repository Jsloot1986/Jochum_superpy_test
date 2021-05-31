"""Because the process to sell thinks have to use diffrent function and actions,
    I deside to make a separte file from it and import it in the main.py"""

import csv
from datetime import date, datetime, timedelta
import sys
import os
import uuid

# first we want to check if there are items in the inventory

def get_items_to_be_sold():
    items_to_be_sold = []
    try:
        with open('bought.csv', newline='') as csvfile:
            bought_item = csv.DictReader(csvfile)
            for row in bought_item:
                price = float(row['buy_price'].replace(',', '.'))
                buy_date = datetime.strptime(row['buy_date'], '%d%m%Y')
                expiration_date = datetime.strptime(row['expiration_date'], ('%d%m%Y'))
                items_to_be_sold.append({
                    'ID': row['ID'],
                    'product_name': row['product_name'],
                    'buy_date': buy_date.strftime('%d%m%Y'),
                    'buy_price': price,
                    'expiration_date': expiration_date.strftime('%d%m%Y'),
                    'sold': row['sold']
                })
        csvfile.close()
    except:
        None
    return items_to_be_sold

#print(get_items_to_be_sold())

"""Now we will check the oldest sellable item, with the follow function call.
    Why? because you always want to sell the oldest item first. Normally in the supermarket you will do this with FIFO method"""

def get_oldest_sellable_item(items_to_be_sold, productname, dates):
    item_found = 'N'
    bought_id = 0
    index = -1
    index_found = -1
    bought_price = 0
    # is searching between the sell item and the inventory for the oldest item in stock
    for item in items_to_be_sold:
        index = index+1
        dates = datetime.strptime(dates, '%Y-%m-%d')
        if (item['product_name'] == productname and item['expiration_date'] == dates.strftime('%d%m%Y') and item['sold'] == 'N' and item_found == 'N'):
            index_found = index
            item_found = 'Y'
            bought_id = item['ID']
            bought_price = item['buy_price']
    return bought_id, bought_price, index_found

#print(get_oldest_sellable_item(get_items_to_be_sold(), 'milk', '2021-05-28'))

"""After we found the item we want to rewrite the bought.csv file and change the sold row in the sold_Date.
    We will do this because we need this data for the reports"""


#def rewrite_bought_file(items_to_be_sold):    
#    for key, value in items_to_be_sold.items():
#        print(key, value)
#        with open('bought.csv', 'r') as csvfile:
#            reader = csv.DictReader(csvfile)
#            print(reader)
#            update_item = []
#            for row in reader:
#                print(row)
#                row = {
#                    'ID': row['ID'],
#                    'product_name': row['product_name'],
#                    'buy_date': row['buy_date'],
#                    'buy_price': row['buy_price'],
#                    'expiration_date': row['expiration_date'],
#                    'sold': 'Y'
#                }
#                if (key[0] == row['ID'] and key[5] == 'N'):
#                    update_item.append(row)
#                else:
#                    pass
#                print(update_item)
#        csvfile.close()
#        with open('bought.csv', 'w+', newline="") as csvfile:
#            field_names = ['ID', 'product_name', 'buy_date', 'buy_price', 'expiration_date', 'sold']
#            updated_item = csv.DictWriter(csvfile, delimiter=',', fieldnames=field_names)
#            updated_item.writerow(dict((heads, heads) for heads in field_names))
#            updated_item.writerows(update_item)
#    
#        csvfile.close()
from tempfile import NamedTemporaryFile

def rewrite_bought_file(items_to_be_sold):
    field_names = ['ID', 'product_name', 'buy_date', 'buy_price', 'expiration_date', 'sold']
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    with open('./bought.csv', 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=field_names)
        writer = csv.DictWriter(tempfile, fieldnames=field_names)
        for row in reader:
            if row['ID'] == str(items_to_be_sold['ID']):
                print('updating row', row['ID'])
                row['ID'], row['product_name'], row['buy_date'], row['buy_price'], row['expiration_date'], row['sold'] = items_to_be_sold['ID'], items_to_be_sold['product_name'], items_to_be_sold['buy_date'], items_to_be_sold['buy_price'], items_to_be_sold['expiration_date'], items_to_be_sold['sold']
            row = {'ID': row['ID'], 'product_name': row['product_name'], 'buy_date': row['buy_date'], 'buy_price': row['buy_price'], 'expiration_date': row['expiration_date'], 'sold': 'Y'}
            writer.writerow(row)
    csvfile.close()

print(rewrite_bought_file({
    'ID': '1ba5e92f-f45b-4d0a-bb8d-cb553bd8ee40',
    'product_name': 'milk',
    'buy_date': '28052021',
    'buy_price': 0.4,
    'expiration_date':'30052021',
    'sold': 'N'
}))    

