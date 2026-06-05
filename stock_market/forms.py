from django import forms
from .models import Stock, StockPortfolio


class StockForm(forms.ModelForm):
	def __init__(self, **kwargs):
		self.user = kwargs.pop('user', None)
		super(StockForm, self).__init__(**kwargs)

	def save(self, commit=True):
		obj = super(StockForm, self).save(commit=False)
		obj.user = self.user
		if commit:
			obj.save()
		return obj

	class Meta:
		model = Stock
		fields = ["ticker"]


class BuyStockForm(forms.ModelForm):
	stock = forms.CharField(max_length=10)
	shares = forms.IntegerField()

	def __init__(self, **kwargs):
		self.user = kwargs.pop('user', None)
		super(BuyStockForm, self).__init__(**kwargs)

	def save(self, commit=True):
		obj = super(BuyStockForm, self).save(commit=False)
		obj.user = self.user
		if commit:
			obj.save()
		return obj

	class Meta:
		model = StockPortfolio
		fields = ['stock', 'shares']


class SellStockForm(forms.ModelForm):
	stock = forms.CharField(max_length=10)
	shares = forms.IntegerField()

	def __init__(self, **kwargs):
		self.user = kwargs.pop('user', None)
		super(SellStockForm, self).__init__(**kwargs)

	def save(self, commit=True):
		obj = super(SellStockForm, self).save(commit=False)
		obj.user = self.user
		if commit:
			obj.save()
		return obj

	class Meta:
		model = StockPortfolio
		fields = ['stock', 'shares']