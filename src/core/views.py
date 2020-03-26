from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView

class QuoteView(APIView):
    def get(self, request, *args, **kwargs):
        symbol = request.query_params.get('symbol')
        price = request.query_params.get('price')
        data = {
            'symbol': symbol,
            'price': price,
        }
        return Response(data)

# http://127.0.0.1:8000/?format=json&name=john&age=98


# def test_view(request):
#     #age = self.request.query_params.get('age')
#     data = {
#         'name': 'john',
#         'age': 98,
#     }
#     return JsonResponse(data, safe=False)
