from App.models import *

'''
This module determines if stock queried is a stock not yet in database -> addnewstock module
or if the stock queried is already in the database -> updatestock module
'''

def exists(symbol):
    '''
    Returns Boolean of stock with symbol = symbol exists in db
    '''
    return Stock.objects.filter(symbol = symbol).exists()

