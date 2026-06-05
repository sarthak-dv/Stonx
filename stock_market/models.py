from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Stock(models.Model):
	ticker = models.CharField(max_length=10)
	user = models.ForeignKey(User, on_delete = models.CASCADE)

	def __str__(self):
		return self.ticker

class StockFolio(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	earned = models.FloatField(default=0, max_length=12)
	spent = models.FloatField(default=0, max_length=12)
	net = models.FloatField(default=0, max_length=12)

class StockPortfolio(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	stock = models.CharField(max_length=10)
	company = models.CharField(max_length=100, default='')
	shares = models.PositiveIntegerField(default=0)
	action = models.CharField(max_length=10, default='')
	cur_price = models.DecimalField(default=0, max_digits=12, decimal_places=2)
	total_price = models.DecimalField(default=0, max_digits=12, decimal_places=2)
	date = models.DateTimeField(default=timezone.now)

	@staticmethod
	def buy(user, num_shares, cost_per_share):
		'''Create stock row or add num of shares'''
		stock_user = StockFolio.objects.get_or_create(user=user)[0]
		stock_user.spent += float(cost_per_share) * int(num_shares)
		stock_user.net = stock_user.earned - stock_user.spent
		stock_user.save()

	@staticmethod
	def sell(user, num_shares, cost_per_share):
		'''Create stock row or negate num of shares'''
		stock_user = StockFolio.objects.get_or_create(user=user)[0]
		stock_user.earned += float(cost_per_share) * int(num_shares)
		stock_user.net = stock_user.earned - stock_user.spent
		stock_user.save()