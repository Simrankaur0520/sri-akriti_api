import numpy as np
import pandas as pd
import time
from datetime import datetime as dt
import datetime
import re
from operator import itemgetter 
import os
import random


#-------------------------Django Modules---------------------------------------------
from django.http import Http404, HttpResponse, JsonResponse,FileResponse
from django.shortcuts import render
from django.db.models import Avg,Count,Case, When, IntegerField,Sum,FloatField,CharField
from django.db.models import F,Func,Q
from django.db.models import Value as V
from django.db.models.functions import Concat,Cast,Substr
from django.contrib.auth.hashers import make_password,check_password
from django.db.models import Min, Max
from django.db.models import Subquery
#----------------------------restAPI--------------------------------------------------
from rest_framework.decorators import parser_classes,api_view
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.response import Response

#----------------------------models---------------------------------------------------
from apiApp.models import product_data
from apiApp.models import user_whishlist,user_data


#----------------------------extra---------------------------------------------------
import simplejson as json

# Create your views here.

@api_view(['POST'])
def adminViewAllProducts(request,format=None):
    data = product_data.objects.values('id','name','category')
    res = {
            'status':True,
            'message':'response for all products',
            'data':data
          }
    return Response(res)

@api_view(['GET'])
def adminSingleProduct(request,format=None):
    id =  request.GET.get('product_id')
    obj = product_data.objects.filter(id=id).values().last()
    res = {}
    res['product_id'] = obj['id']
    res['name'] = obj['name']
    res['gender'] = 'Male' if obj['gender'] == 'M' else ('Female' if obj['gender'] == 'F' else 'Unisex')
    res['category'] = obj['category']
    res['image'] = obj['image'].split(',')
    res['discount'] = obj['discount']

    diamond_quality = obj['diamond_quality'].split(',')
    weight = obj['weight'].split(',')
    size = obj['size'].split(',')
    actual_price = eval(obj['actual_price'])
    selling_price = eval(obj['selling_price'])

    variants = []
    mock_id = 1
    for i in range(len(diamond_quality)):
      sub_variants = {}
      sub_variants['diamond_quality'] = diamond_quality[i]
      sub_variant_data = []
      for j in range(len(size)):
        sub_variant_data.append([{
                                'id': mock_id,
                                'title':'size',
                                'value':size[j]
                                },
                                {
                                'id': mock_id+1,
                                'title':'weight',
                                'value':weight[j]
                                },
                                {
                                'id': mock_id+2,
                                'title':'actual_price',
                                'value':actual_price[i][j]
                                },
                                {
                                'id': mock_id+3,
                                'title':'selling_price',
                                'value':selling_price[i][j]
                                }])
        mock_id = mock_id + 4
        sub_variants['sub_variants_data'] = sum(sub_variant_data,[])
      variants.append(sub_variants)
      # variants.append({
      #                   'diamond_quality':diamond_quality[i],
      #                   'size':size,
      #                   'weight':weight,
      #                   'actual_price':actual_price[i],
      #                   'selling_price':selling_price[i],
      #                 })
    res['variants'] = variants
    return Response(res)