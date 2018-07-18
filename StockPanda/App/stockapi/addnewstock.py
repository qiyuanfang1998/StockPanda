from App.models import *
from .stockinfo import *
import threading
import queue
#for testing only
import time

'''
This module adds a new stock to the database using the stockinfo querying module
'''

class sThread(threading.Thread):
    '''
    generic thread implementation to run stockinfo functions inside python thread
    '''
    def __init__(self,func,symbol,out_queue,threadID):
        threading.Thread.__init__(self)
        self.func = func
        self.symbol = symbol
        self.out_queue = out_queue
        self.threadID = threadID

    def run(self):
         res_enum = (self.threadID, self.func(self.symbol))
         self.out_queue.put(res_enum)

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
    current_price_thread = sThread(current_price,symbol,out_queue,1)
    company_info_thread = sThread(company_info,symbol,out_queue,2)
    dividends_thread = sThread(dividends,symbol,out_queue,3)
    earnings_thread = sThread(earnings,symbol,out_queue,4)

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

    print(current_price_res)
    print(company_info_res)
    print(dividends_res)
    print(earnings_res)

    print(time.time() - start_time)

    # stock =  Stock(symbol = 'AAA')
    # stock.save()
