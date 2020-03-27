import bs4
import requests
from bs4 import BeautifulSoup
import os
import lxml
from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView

class QuoteView(APIView):
    def get(self, request, *args, **kwargs):
        symbol = request.query_params.get('symbol')
        # price = request.query_params.get('price')

        url = f'https://finance.yahoo.com/quote/{symbol}?p={symbol}'
        r = requests.get(url)
        soup = bs4.BeautifulSoup(r.text, features="lxml")
        try:
            last_sale_price = soup.find_all('div',{'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
            prev_close = soup.find_all('table', {'class': 'W(100%)'})[0].text
            prev_close = prev_close[14:prev_close.find('Open')]
            price_and_percent_change = str(soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find_all('span')[1].text)
            percent_change = price_and_percent_change[price_and_percent_change.find('(') + 1:-2]
            percent_change = float(percent_change.replace('+', ''))
            #day_range = soup.find_all('div', {'class': 'D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($c-fuji-grey-c)'})[0].find_all('td')[9].text
            day_range = soup.find_all('div', {'class': 'D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)'})[0].find_all('td')[9].text
            day_low = str(day_range)[0:day_range.find('-') - 1]
            day_high = str(day_range)[day_range.find('-') + 2:]
        except Exception as error:
            db_conn = db.connect()
            db.insert_run_log(db_conn, str(datetime.now()), f'Encountered an exception when trying to retrieve price for {symbol} from Yahoo.', error, soup)

        data = {
            'symbol': symbol,
            'last_sale_price': last_sale_price, 
            'percent_change': percent_change, 
            'day_low': day_low, 
            'day_high': day_high, 
        }
        return Response(data)

# http://127.0.0.1:8000/?format=json&symbol=BAC&price=18.98


# def test_view(request):
#     #age = self.request.query_params.get('age')
#     data = {
#         'name': 'john',
#         'age': 98,
#     }
#     return JsonResponse(data, safe=False)
