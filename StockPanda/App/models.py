from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

'''
Django ORM models for database for main Application.
Information is obtained through the IEX Developer API
Description:
Users have A SuperPortfolio
Users have A WatchList that has MANY TO MANY ZERO OR MORE STOCK/CryptoCurrency
SuperPortfolios have ZERO OR MORE Portfolios
Portfolios MANY TO MANY ZERO OR MORE Stocks through StockOwnership intermediate
Portfolios MANY TO MANY ZERO OR MORE CryptoCurrency through CryptoCurrencyOwnership intermediate
'''

class Stock(models.Model):
    '''
    The information stored in the Stock model is for db querying so we don't have to pull all
    of the information for the stock from web API every single time.
    What is pulled from the web APIs is stock value information as it is impractical
    for us to store that information in the db every single time we query.
    '''
    #general stock information
    symbol = models.CharField(max_length = 20, default = "",unique = True)
    company_name = models.CharField(max_length = 50, default = "")
    exchange = models.CharField(max_length = 100, default = "")
    industry = models.CharField(max_length = 100, default = "")
    website = models.CharField(max_length = 250, default = "")
    description = models.CharField(max_length = 1000, default = "")
    ceo = models.CharField(max_length = 100, default = "")
    issueType = models.CharField(max_length = 50, default = "")
    sector = models.CharField(max_length = 50, default = "")
    #dividends information
    amount = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    div_type = models.CharField(max_length = 50, default = "")
    #earnings information
        #latest quarter
    latest_actual_eps = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    latest_estimated_eps = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    latest_eps_year_ago = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    latest_eps_year_ago_change_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    latest_eps_year_ago_estimated_change_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    latest_fiscal_period =  models.CharField(max_length = 100, default = "")
        #T-1 quarter
    tminusone_actual_eps = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    tminusone_estimated_eps = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    tminusone_eps_year_ago = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    tminusone_eps_year_ago_change_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    tminusone_eps_year_ago_estimated_change_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    tminusone_fiscal_period =  models.CharField(max_length = 100, default = "")
        #T-2 quarter
    tminustwo_actual_eps = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    tminustwo_estimated_eps = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    tminustwo_eps_year_ago = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    tminustwo_eps_year_ago_change_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    tminustwo_eps_year_ago_estimated_change_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    tminustwo_fiscal_period =  models.CharField(max_length = 100, default = "")
        #T-3 quarter
    tminusthree_actual_eps = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    tminusthree_estimated_eps = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    tminusthree_eps_year_ago = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    tminusthree_eps_year_ago_change_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    tminusthree_eps_year_ago_estimated_change_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    tminusthree_fiscal_period =  models.CharField(max_length = 100, default = "")

    #stock value & last updated time        /stored EOD and queried if markets have closed
    current_value = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    last_updated_time = models.DateTimeField(auto_now_add = True)



    def __str__(self):
        return self.symbol

class CryptoCurrency(models.Model):
    #crypto attributes
    currency_name = models.CharField(max_length = 50,default = "", unique=True)

    def __str__(self):
        return self.ticker

class WatchList(models.Model):
    owned_by = models.OneToOneField(User,on_delete = models.CASCADE, related_name = 'watchlist')
    stocks_watched = models.ManyToManyField(Stock, related_name = 'stocks_watched')
    cryptocurrencies_watched = models.ManyToManyField(CryptoCurrency, related_name = 'cryptocurrencies_watched')


class SuperPortfolio(models.Model):
    #super portfolio attributes
    total_value = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    #super portfolio - User foreign key
    owned_by = models.OneToOneField(User,on_delete = models.CASCADE, related_name = 'superportfolio')


class Portfolio(models.Model):
    #portfolio attributes
    name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 250)
    total_value = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    cash = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
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

#auto create watchlist and SuperPortfolio everytime a new user is added to the db. Each user has a single super portfolio and watchlist.
@receiver(post_save,sender = User)
def create_user_watchlist_and_superportfolio(sender,instance,created,**kwargs):
    if created:
        WatchList.objects.create(owned_by = instance)
        SuperPortfolio.objects.create(owned_by = instance)

@receiver(post_save, sender = User)
def save_user_watchlist_and_superportfolio(sender, instance, **kwargs):
    instance.watchlist.save()
    instance.superportfolio.save()
