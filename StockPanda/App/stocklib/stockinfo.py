import urllib.request
import urllib.parse
from App.sThread import sThread
import json
import threading
import queue

from decimal import *

'''
This multi-threaded module gets current stock information from IEX Developer platform
Returns information in dictionaries/ list of dictionaries form to caller function
For getting earnings, the function is multi-threaded to allow for multiple API calls simultaneously
'''

class UnknownStock(Exception):
    pass

def realtime_price(symbol):
    '''
    Returns the real time price for stock with symbol x
    realtime_price, amount_change, percent_change
    '''
    try:
        api_call = "https://api.iextrading.com/1.0/stock/"+str(symbol)+"/quote"
        res = urllib.request.urlopen(api_call).read().decode('utf-8')
        json_res = json.loads(res)
        if "Unknown symbol" in str(res):
            raise UnknownStock()
        return {'realtime_price':round(Decimal(json_res['latestPrice']),2), 'amount_change':round(Decimal(json_res['change']),2), 'percent_change':round(Decimal(json_res['changePercent']),2)}
    except Exception as e:
        print("Failed to retreive stock realtime price with symbol " + symbol + " "+str(e))

def current_price(symbol):
    ''' Returns the delayed current price for stock with symbol x
        T[0] := current_price
        DEPRECATED, USE REALTIME_PRICE FUNCTION
        '''
    try:
        api_call = "https://api.iextrading.com/1.0/stock/"+str(symbol)+"/delayed-quote"
        res = urllib.request.urlopen(api_call).read().decode('utf-8')
        json_res = json.loads(res)
        if "Unknown symbol" in str(res):
            raise UnknownStock()
        return {'current_price':round(Decimal(json_res['delayedPrice']),2)}
    except Exception as e:
        print("Failed to retreive stock delayed quote with symbol "+symbol+" "+str(e))

def company_info(symbol):
    '''Returns information about company with symbol x -only run when new stock added to db
    T[0] := company_name, T[1] := exchange, T[2] = industry, T[3] = website, T[4] = description, T[5] = ceo, T[6] = issueType, T[7] = sector
    '''
    try:
        api_call = "https://api.iextrading.com/1.0/stock/" + str(symbol) + "/company"
        res = urllib.request.urlopen(api_call).read().decode('utf-8')
        json_res = json.loads(res)
        if "Unknown symbol" in str(res):
            raise UnknownStock()
        return {
            'company_name': json_res['companyName'],
            'exchange': json_res['exchange'],
            'industry': json_res['industry'],
            'website': json_res['website'],
            'description': json_res['description'],
            'ceo': json_res['CEO'],
            'issue_type': json_res['issueType'],
            'sector': json_res['sector']
        }
    except Exception as e:
        print("Failed to retreive stock company information with symbol " + symbol + " " + str(e))

def dividends(symbol):
    ''' Returns information about dividends of stock with symbol x
        T[0] = amount, T[1] = type
    '''
    try:
        api_call = "https://api.iextrading.com/1.0/stock/" + str(symbol) + "/dividends/ytd"
        res = urllib.request.urlopen(api_call).read().decode('utf-8')
        json_res = json.loads(res)
        if "Unknown symbol" in str(res):
            raise UnknownStock()
        if "[]" == str(res):
            return {
                'amount' : 0,
                'type' : "No dividend"
            }
        return{
            'amount': round(Decimal(json_res[0]['amount']),2),
            'type': json_res[0]['type']
        }
    except Exception as e:
        print("Failed to retreive stock dividend information with symbol " + symbol + " " + str(e))

def earnings(symbol):
    ''' Returns information about earnings of company of stock with symbol x (last four quarters)
        (T[0][0] = actual_eps,
        T[0][1] = estimated_eps,
        T[0][2] = eps_year_ago,
        T[0][3] = eps_year_ago_change_percent
        T[0][4] = eps_year_ago_estimated_change_percent,
        T[0][5] = fiscal_period)...
        dictionary list
    '''
    try:
        api_call = "https://api.iextrading.com/1.0/stock/" + str(symbol) + "/earnings"
        res = urllib.request.urlopen(api_call).read().decode('utf-8')
        json_res = json.loads(res)
        if "Unknown symbol" in str(res):
            raise UnknownStock()
        earnings_list = []

        for index in range(0,4):
            nested_earnings_dict = {'actualEPS': json_res['earnings'][index]['actualEPS'],
                'estimated_eps': json_res['earnings'][index]['estimatedEPS'],
                'year_ago': json_res['earnings'][index]['yearAgo'],
                'eps_year_ago_change_percent': round(Decimal(json_res['earnings'][index]['yearAgoChangePercent']),2),
                'estimated_change_percent': round(Decimal(json_res['earnings'][index]['estimatedChangePercent']),2),
                'fiscal_period': json_res['earnings'][index]['fiscalPeriod']}
            earnings_list.append(nested_earnings_dict)
        return earnings_list

    except Exception as e:
        print("Failed to retreive stock earnings information with symbol " + symbol + " " + str(e))

def oneDayChart(symbol):
    try:
        api_call = "https://api.iextrading.com/1.0/stock/" + str(symbol) + "/chart/1d"
        res = urllib.request.urlopen(api_call).read().decode('utf-8')
        json_res = json.loads(res)
        if "Unknown symbol" in str(res):
            raise UnknownStock()
        averagePrices = []
        highPrices = []
        lowPrices = []
        time = []
        for data in json_res:
            averagePrices.append(round(data['marketAverage'],2))
            highPrices.append(round(data['marketHigh'],2))
            lowPrices.append(round(data['marketLow'],2))
            time.append(data['label'])
        return {'averagePrices': averagePrices, 'highPrices': highPrices, 'lowPrices': lowPrices, 'time': time}
    except Exception as e:
        print("error this really shouldn't error like really the api is hella broken :(" + symbol +" "+ str(e))

def getAll(symbol):
    '''
    Aggregate threaded function, used in addnewstock, updatestock
    returns dict with keys current_price, company_info, dividends, earnings
    which are nested dictionaries
    '''
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
    return {
        'current_price': current_price_res,
        'company_info': company_info_res,
        'dividends': dividends_res,
        'earnings': earnings_res
    }
