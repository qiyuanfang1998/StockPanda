from django.db import models
from django.contrib.auth.models import User

'''
Django ORM models for database
Description:
Users have A SuperPortfolio
SuperPortfolios have ZERO OR MORE Portfolios
Portfolios MANY TO MANY ZERO OR MORE Stocks through StockOwnership intermediate
Portfolios MANY TO MANY ZERO OR MORE CryptoCurrency through CryptoCurrencyOwnership intermediate
'''

class Stock(models.Model):
    #stock attributes
    ticker = models.CharField(max_length = 20)
    current_value = models.DecimalField(max_digits = 19, decimal_places = 2)
    last_updated_time = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.ticker

class CryptoCurrency(models.Model):
    #crypto attributes
    currency_name = models.CharField(max_length = 50)
    current_value = models.DecimalField(max_digits = 19, decimal_places = 2)
    last_updated_time = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.ticker

class SuperPortfolio(models.Model):
    #super portfolio attributes
    total_value = models.DecimalField(max_digits = 19, decimal_places = 2)
    #super portfolio - User foreign key
    owned_by = models.ForeignKey(User,on_delete = models.CASCADE, related_name = 'superportfolio')

class Portfolio(models.Model):
    #portfolio attributes
    name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 100)
    total_value = models.DecimalField(max_digits = 19, decimal_places = 2)
    cash = models.DecimalField(max_digits = 19, decimal_places = 2)
    #portfolio - super portfolio foreign key
    owned_by = models.ForeignKey(SuperPortfolio,on_delete = models.CASCADE, related_name = 'portfolios')
    #stock, crypto ownership M2M relationships
    stocks_owned = models.ManyToManyField(Stock, through = 'StockOwnership', related_name = 'stocks')
    cryptocurrencies_owned = models.ManyToManyField(CryptoCurrency, through = 'CryptoCurrencyOwnership', related_name = 'cryptocurrencies')
    def __str__(self):
        return self.name

#Intermediate ownership relationship between Portfolio - stock M2M relationship
class StockOwnership(models.Model):
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete = models.CASCADE)
    shares = models.DecimalField(max_digits = 19, decimal_places = 2)
    average_price_per_share = models.DecimalField(max_digits = 19, decimal_places = 2)

#Intermediate ownership relationship between Portfolio - CryptoCurrency M2M relationship
class CryptoCurrencyOwnership(models.Model):
    cryptocurrency = models.ForeignKey(CryptoCurrency, on_delete = models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete = models.CASCADE)
    units = models.DecimalField(max_digits = 19, decimal_places = 2)
    average_price_per_unit = models.DecimalField(max_digits = 19, decimal_places = 2)
