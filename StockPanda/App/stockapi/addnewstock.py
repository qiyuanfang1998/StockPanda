from App.models import *
from .stockinfo import *
from App.sThread import sThread
import threading
import queue
#for testing only
import time

'''
This module adds a new stock to the database using the stockinfo querying module
Uses sThread module for multithreading API calls
'''

# class sThread(threading.Thread):
#     '''
#     generic thread implementation to run stockinfo functions inside python thread
#     '''
#     def __init__(self,func,symbol,out_queue,threadID):
#         threading.Thread.__init__(self)
#         self.func = func
#         self.symbol = symbol
#         self.out_queue = out_queue
#         self.threadID = threadID
#
#     def run(self):
#          res_enum = (self.threadID, self.func(self.symbol))
#          self.out_queue.put(res_enum)

#TEST FUNCTION FOR UNTHREADED, NOT USED IN PRODUCTION
#ABOUT 3.5X SLOWER WITH TIME MODULE TEST THAN THREADED VERSION
def stock_unthreaded(symbol):
    start_time = time.time()

    current_price_res = current_price(symbol)
    company_info_res = company_info(symbol)
    dividends_res = company_info(symbol)
    earnings_res = earnings(symbol)
    print(current_price_res)
    print(company_info_res)
    print(dividends_res)
    print(earnings_res)
    print(time.time() - start_time)





def stock(symbol):
    '''
    This function takes symbol s and creates a new Stock in the database
    calls from stockinfo module
        current_price(symbol)
        company_info(symbol)
        dividends(symbol)
        earnings(symbol)
    and parses the information to create the new Stock.
    '''

    start_time = time.time()

    #out Queue
    out_queue = queue.Queue()

    #threads to run
    current_price_thread = sThread.sThread(current_price,symbol,out_queue,1)
    company_info_thread = sThread.sThread(company_info,symbol,out_queue,2)
    dividends_thread = sThread.sThread(dividends,symbol,out_queue,3)
    earnings_thread = sThread.sThread(earnings,symbol,out_queue,4)

    current_price_thread.start()
    company_info_thread.start()
    dividends_thread.start()
    earnings_thread.start()

    current_price_thread.join()
    company_info_thread.join()
    dividends_thread.join()
    earnings_thread.join()

    current_price_res = None
    company_info_res = None
    dividends_res = None
    earnings_res = None

    for x in range(0,4):
        res = out_queue.get()
        if 1 == res[0]:
            current_price_res = res[1]
        elif 2 == res[0]:
            company_info_res = res[1]
        elif 3 == res[0]:
            dividends_res = res[1]
        elif 4 == res[0]:
            earnings_res = res[1]

    # print(current_price_res)
    # print(company_info_res)
    # print(dividends_res)
    # print(earnings_res)

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
        #earnings information

        #current_price information (added anyways on first addnewstock just for placeholding)
        current_value = current_price_res['current_price']
    )
    stock.save()
    print(time.time() - start_time)
