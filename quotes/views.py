from django.shortcuts import render,redirect
from .models import stock
from .forms import StockForm
from django.contrib import messages
from django.http import HttpResponseRedirect

def home(request):
    import requests
    import json 
    if request.method == "POST":
        ticker = request.POST['ticker']
        api_request=requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" +ticker+ "&interval=5min&apikey=DP0GVTOWY9FKY73D")
       
        try:
            api = json.loads(api_request.content)
            MetaData = api.get("Meta Data")
            metaData= {x.replace(' ', '').split('.')[1]: v for x, v in MetaData.items()}
        except Exception as e:
            api = "Error ..."
            metaData = "error ... "
        
        return render(request, 'home.html', {'api': api, 'metaData':metaData })
    else:
        return render(request, 'home.html', {'ticker_symbol': "enter a ticker symbol above"})



def about(request):
    return render(request, 'about.html',{})



def add_stock(request):
    import requests
    import json

    if request.method == "POST":
        form = StockForm(request.POST or None )
        if form.is_valid():
            form.save()
            messages.success(request, ('stock has been added'))
            return redirect('add_stock')
    else:
        symbol = stock.objects.all()
        output = []
        for symbol_item in symbol:
            api_request=requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" +str(symbol_item)+ "&interval=5min&apikey=DP0GVTOWY9FKY73D")
            try:
                api = json.loads(api_request.content)
                MetaData = api.get("Meta Data")
                metaData= {x.replace(' ', '').split('.')[1]: v for x, v in MetaData.items()}
                output.append(metaData)
            except Exception as e:
                api = "Error ..."
        return render(request, 'add_stock.html', {'symbol': symbol, 'output':output})


def delete(request, stock_id):
    item = stock.objects.get(pk= stock_id)
    item.delete()
    messages.success(request, ('stock has been deleted'))
    return redirect('delete_stock')


def delete_stock(request):
    symbol = stock.objects.all()
    return render(request, 'delete_stock.html', {'symbol': symbol})
     

