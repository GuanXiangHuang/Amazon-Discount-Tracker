from django.shortcuts import render
from django.http import HttpResponse
from . import AmazonScraper
import cgi

# Create your views here.
def index(request):
    return render(request, 'PriceApp/Price.html')

def submit(request):
    print("PRINTING FORM INFO")
    info = request.GET
    email = info['form-email']
    url = info['form-url']
    price = info['form-price']
    print(info)
    print(email)
    print(url)
    print(price)
    AmazonScraper.check_price(url, price, email)
    print("after calling check_price")
    return HttpResponse("Submitted!")
