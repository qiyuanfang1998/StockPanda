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
    #general stock information
    symbol = models.CharField(max_length = 20, default = "")
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
    actual_eps = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    estimated_eps = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    eps_year_ago = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    eps_year_ago_change_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    eps_year_ago_estimated_change_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)

    #stock value & last updated time
    current_value = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    last_updated_time = models.DateTimeField(auto_now_add = True)

    #stock performance
        #stock amount changes information
    one_day_performance_amount = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    one_week_performance_amount = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    one_month_performance_amount = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    three_month_performance_amount = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    one_year_performance_amount = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    five_year_performance_amount = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
        #stock percent change information
    one_day_performance_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    one_week_performance_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    one_month_performance_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    three_month_performance_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    one_year_performance_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    five_year_performance_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)


    def __str__(self):
        return self.ticker

class CryptoCurrency(models.Model):
    #crypto attributes
    currency_name = models.CharField(max_length = 50)
    current_value = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    last_updated_time = models.DateTimeField(auto_now_add = True)
    #crypto performance
        #crpyto amount changes information
    one_day_performance_amount = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    one_week_performance_amount = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    one_month_performance_amount = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    three_month_performance_amount = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    one_year_performance_amount = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    five_year_performance_amount = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
        #crypto percent change information
    one_day_performance_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    one_week_performance_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    one_month_performance_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    three_month_performance_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    one_year_performance_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    five_year_performance_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)

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
    #aggregate portfolio perfomance
        #portfolio amount changes information
    one_day_performance_amount = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    one_week_performance_amount = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    one_month_performance_amount = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    three_month_performance_amount = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    one_year_performance_amount = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    all_time_performance_amount = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
        #portfolio percent change information
    one_day_performance_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    one_week_performance_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    one_month_performance_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    three_month_performance_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    one_year_performance_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    all_time_performance_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)


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
    #portfolio performance
        #portfolio amount changes information
    one_day_performance_amount = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    one_week_performance_amount = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    one_month_performance_amount = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    three_month_performance_amount = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    one_year_performance_amount = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    all_time_performance_amount = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
        #portfolio percent change information
    one_day_performance_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    one_week_performance_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    one_month_performance_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    three_month_performance_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    one_year_performance_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)
    all_time_performance_percent = models.DecimalField(max_digits = 19, decimal_places = 2,default = 0)

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

#auto create watchlist and SuperPortfolio for new User
@receiver(post_save,sender = User)
def create_user_watchlist_and_superportfolio(sender,instance,created,**kwargs):
    if created:
        WatchList.objects.create(owned_by = instance)
        SuperPortfolio.objects.create(owned_by = instance)

@receiver(post_save, sender = User)
def save_user_watchlist_and_superportfolio(sender, instance, **kwargs):
    instance.watchlist.save()
    instance.superportfolio.save()
