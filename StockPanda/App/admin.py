from django.contrib import admin
from .models import Stock,CryptoCurrency

# Register your models here.
admin.site.register(Stock)
admin.site.register(CryptoCurrency)
