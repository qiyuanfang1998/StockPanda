from App.models import Stock

'''
This module provides queries for stocks that exist in the database
functions:
    exists(symbol): returns Boolean for if stock with symbol = symbol exists in db, used for determining if add new stock with symbol to db

'''

def exists(symbol):
    '''
    Returns Boolean of stock with symbol = symbol exists in db
    '''
    return Stock.objects.filter(symbol = symbol).exists()

def get(symbol):
    '''
    Returns Stock with symbol = symbol
    Do not call without prior exists unless from a link of a known existing stock
    '''
    return Stock.objects.get(symbol = symbol)

def similar_exchange(stock):
    '''
    Returns list of Stock objects with exchanges = stock.exchange
    '''
    return Stock.objects.filter(exchange = stock.exchange)
    

def similar_industry(stock):
    '''
    Returns list of Stock objects with industry = stock.industry
    '''
    return Stock.objects.filter(industry = stock.industry)

def similar_sector(stock):
    '''
    Returns list of Stock objects with sector = stock.sector
    '''
    return Stock.objects.filter(sector = stock.sector)



