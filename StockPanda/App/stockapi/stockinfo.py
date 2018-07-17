import urllib.request
import urllib.parse
import json

from decimal import *

'''
This library gets current stock information from IEX Developer platform
Returns information in tuple form to caller function
'''

class UnknownStock(Exception):
    pass

def current_price(symbol):
    ''' Returns the delayed current price for stock with symbol x
        T[0] := current_price'''
    try:
        api_call = "https://api.iextrading.com/1.0/stock/"+str(symbol)+"/delayed-quote"
        res = urllib.request.urlopen(api_call).read().decode('utf-8')
        json_res = json.loads(res)
        if "Unknown symbol" in str(res):
            raise UnknownStock()
        return (round(Decimal(json_res['delayedPrice']),2))
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
        return (
            json_res['companyName'],
            json_res['exchange'],
            json_res['industry'],
            json_res['website'],
            json_res['description'],
            json_res['CEO'],
            json_res['issueType'],
            json_res['sector']
        )
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
        return(
            round(Decimal(json_res[0]['amount']),2),
            json_res[0]['type']
        )
    except Exception as e:
        print("Failed to retreive stock dividend information with symbol" + symbol + " " + str(e))

def earnings(symbol):
    ''' Returns information about earnings of company of stock with symbol x (last four quarters)
        (T[0][0] = actual_eps, T[0][1] = estimated_eps, T[0][2] = eps_year_ago, T[0][3] = eps_year_ago_change_percent T[0][4] = eps_year_ago_estimated_change_percent, T[0][5] = fiscal_period)...
        Nested tuple
    '''
    try:
        api_call = "https://api.iextrading.com/1.0/stock/" + str(symbol) + "/earnings"
        res = urllib.request.urlopen(api_call).read().decode('utf-8')
        json_res = json.loads(res)
        if "Unknown symbol" in str(res):
            raise UnknownStock()
        return (
            (json_res['earnings'][0]['actualEPS'],json_res['earnings'][0]['estimatedEPS'],json_res['earnings'][0]['yearAgo'],json_res['earnings'][0]['yearAgoChangePercent'],json_res['earnings'][0]['estimatedChangePercent'],json_res['earnings'][0]['fiscalPeriod']),
            (json_res['earnings'][1]['actualEPS'],json_res['earnings'][1]['estimatedEPS'],json_res['earnings'][1]['yearAgo'],json_res['earnings'][1]['yearAgoChangePercent'],json_res['earnings'][1]['estimatedChangePercent'],json_res['earnings'][1]['fiscalPeriod']),
            (json_res['earnings'][2]['actualEPS'],json_res['earnings'][2]['estimatedEPS'],json_res['earnings'][2]['yearAgo'],json_res['earnings'][2]['yearAgoChangePercent'],json_res['earnings'][2]['estimatedChangePercent'],json_res['earnings'][2]['fiscalPeriod']),
            (json_res['earnings'][3]['actualEPS'],json_res['earnings'][3]['estimatedEPS'],json_res['earnings'][3]['yearAgo'],json_res['earnings'][3]['yearAgoChangePercent'],json_res['earnings'][3]['estimatedChangePercent'],json_res['earnings'][3]['fiscalPeriod'])
        )

    except Exception as e:
        print("Failed to retreive stock earnings information with symbol" + symbol + " " + str(e))

# def getStock_historical(symbol):
#     ''' Returns historical information about company of stock with symbol x '''
#     try:
#         api_call_1d = "https://api.iextrading.com/1.0/stock/" + str(symbol) + "/stats" + "/"
#         api_call_
