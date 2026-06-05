from django.contrib import admin
from .models import Stock, StockPortfolio, StockFolio

admin.site.register(Stock)
admin.site.register(StockPortfolio)
admin.site.register(StockFolio)
