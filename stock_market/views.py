from django.shortcuts import render, redirect, get_object_or_404
from .models import Stock, StockPortfolio, StockFolio
from .forms import StockForm, BuyStockForm, SellStockForm
from django.contrib import messages
from dotenv import load_dotenv
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView,
)
import os
load_dotenv()

IEX_API_KEY = os.getenv("IEX_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def home(request):
    import requests
    import json

    if request.method == 'POST':
        ticker = request.POST['ticker']
        api_request = requests.get(f"https://cloud.iexapis.com/stable/stock/{ticker}/quote?token={IEX_API_KEY}")

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."

        return render(request, 'home.html', {'api': api, 'error': 'Could not access the api'})

    else:
        return render(request, 'home.html', {'ticker': "Enter a Ticker Symbol Above..."})


def add_stock(request):
    import requests
    import json

    if request.method == 'POST':
	    form = StockForm(user=request.user, data=request.POST)
	
	    if form.is_valid():
		    form.save()
		    messages.success(request, ("Stock has been added to your favorites!"))


    user = request.user
    ticker = Stock.objects.filter(user=user)
    output = []
    for ticker_item in ticker:
        api_request = requests.get(f"https://cloud.iexapis.com/stable/stock/{str(ticker_item)}/quote?token={IEX_API_KEY}")
        try:
            api = json.loads(api_request.content)
            api['id'] = ticker_item.id
            output.append(api)
        except Exception as e:
            api = "Error..."	

    return render(request, 'favorites.html', {'ticker': ticker, 'output':  output})


def about(request):
    return render(request, 'about.html')


def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock Has Been Deleted From Favorites!"))
	return redirect(add_stock)


def news(request):
    import requests
    import json

    api_request = requests.get(f"http://newsapi.org/v2/everything?q=stocks&apiKey={NEWS_API_KEY}")
    api = json.loads(api_request.content)
    return render(request, 'news.html', {'api': api})


def portfolio(request):
    import requests
    import json

    user = request.user
    stocks = StockPortfolio.objects.filter(user=user)
    userfolio = StockFolio.objects.filter(user=user).first()
    return render(request, 'portfolio.html', {'stocks': stocks, 'folio': userfolio})


@login_required
def buy(request):
    import requests
    import json

    if request.method == 'POST':
        form = BuyStockForm(user=request.user, data=request.POST)
        
        if form.is_valid():
            form.save()
            user = request.user
            stocks = StockPortfolio.objects.last()
            api_request = requests.get(f"https://cloud.iexapis.com/stable/stock/{str(stocks.stock)}/quote?token={IEX_API_KEY}")
            try:
                api = json.loads(api_request.content)
                stocks.cur_price = api['latestPrice']
                stocks.action = 'BOUGHT'
                stocks.company = api['companyName']
                stocks.total_price = stocks.cur_price * stocks.shares
                stocks.save()
                stocks.buy(user, stocks.shares, api['latestPrice'])
            except Exception as e:
                api = "Error..."	

            messages.success(request, f'Stock bought!')
            return redirect('portfolio')
    else:
        form = BuyStockForm(instance=request.user)

    context = {'form': form}

    return render(request, 'buy.html', context)


@login_required
def sell(request):
    import requests
    import json

    if request.method == 'POST':
        form = SellStockForm(user=request.user, data=request.POST)
        
        if form.is_valid():
            form.save()
            user = request.user
            stocks = StockPortfolio.objects.last()
            api_request = requests.get(f"https://cloud.iexapis.com/stable/stock/{str(stocks.stock)}/quote?token={IEX_API_KEY}")
            try:
                api = json.loads(api_request.content)
                stocks.cur_price = api['latestPrice']
                stocks.action = 'SOLD'
                stocks.company = api['companyName']
                stocks.total_price = stocks.cur_price * stocks.shares
                stocks.save()
                stocks.sell(user, stocks.shares, api['latestPrice'])
            except Exception as e:
                api = "Error..."
            messages.success(request, f'Stock sold!')
            return redirect('portfolio')
    else:
        form = SellStockForm(instance=request.user)

    context = {'form': form}

    return render(request, 'sell.html', context)