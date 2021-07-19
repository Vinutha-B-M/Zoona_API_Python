from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
import requests


# class device_list(APIView):
#
#     def get(self, request):
#         response = requests.get('https://connect.squareupsandbox.com/v2/locations/L8BKETKRHE1PP/transactions/',
#                                 headers={"Authorization": "Bearer EAAAENz618Mx91J_aZ2jq-VAlBEr05uLz6yTMngy84AfbuBCvKAvQ38pyhNKLYT3"})
#         json_response = response.json()
#         return JsonResponse(json_response)
#
#     def post(self, request):
#
#       return
