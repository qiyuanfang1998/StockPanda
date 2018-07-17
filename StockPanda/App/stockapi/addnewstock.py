from App.models import *
from .stockinfo import *
import threading
import queue

'''
This module adds a new stock to the database using the stockinfo querying module
'''

class sThread(threading.Thread):
    '''
    generic thread implementation to run stockinfo function inside python thread
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

    #out Queue
    out_queue = queue.Queue()

    #threads to run
    current_price_thread = sThread(current_price,symbol,out_queue,"current_price_thread")
    company_info_thread = sThread(company_info,symbol,out_queue,"company_info_thread")
    dividends_thread = sThread(dividends,symbol,out_queue,"dividends_thread")
    earnings_thread = sThread(earnings,symbol,out_queue,"earnings_thread")

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
        if "current_price_thread" in res[0]:
            current_price_res = res[1]
        elif "company_info_thread" in res[0]:
            company_info_res = res[1]
        elif "dividends_thread" in res[0]:
            dividends_res = res[1]
        elif "earnings_thread" in res[0]:
            earnings_res = res[1]

    print(current_price_res)
    print(company_info_res)
    print(dividends_res)
    print(earnings_res)
