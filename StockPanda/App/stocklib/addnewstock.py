from App.models import *
from .stockinfo import *
from App.sThread import sThread
import threading
import queue
import datetime

'''
This module adds a new stock to the database using the stockinfo querying module
Uses sThread module for multithreading API calls
'''

def stock(symbol):
    '''
    This function takes symbol s and creates a new Stock in the database
    calls getAll from stockinfo module and parses the information to create the new Stock.
    '''

    getAll_res = getAll(symbol)

    current_price_res = getAll_res['current_price']
    company_info_res = getAll_res['company_info']
    dividends_res = getAll_res['dividends']
    earnings_res = getAll_res['earnings']

    #create the stock model from models.py with the information obtained
    stock = Stock(
        #general stock information
        symbol = str(symbol),
        company_name = company_info_res['company_name'],
        exchange = company_info_res['exchange'],
        industry = company_info_res['industry'],
        website = company_info_res['website'],
        description = company_info_res['description'],
        ceo = company_info_res['ceo'],
        issueType = company_info_res['issue_type'],
        sector = company_info_res['sector'],
        #dividends information
        amount = dividends_res['amount'],
        div_type = dividends_res['type'],
        #earnings information todo

        #current_price information (added anyways on first addnewstock just for placeholding)
        current_value = current_price_res['current_price'],
        last_updated_time =  datetime.datetime.now()
    )
    stock.save()

def stock_Batch(stocks):
    '''
    ??? might make a multi-threaded function to create a batch of stocks prob not needed, Django probably takes care of
    '''
    pass
