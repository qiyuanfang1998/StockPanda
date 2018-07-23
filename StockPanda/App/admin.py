from django.contrib import admin
from .models import Stock, CryptoCurrency

# Default stock, crypto models
admin.site.register(Stock)
admin.site.register(CryptoCurrency)


