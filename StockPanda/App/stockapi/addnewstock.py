from .. import models
from stockinfo import *

'''
This module adds a new stock to the database using the stockinfo querying module
'''

def stock(symbol):
    
    stock = Stock()
