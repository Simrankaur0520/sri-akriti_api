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
from apiApp.models import metal_price,diamond_pricing


#----------------------------extra---------------------------------------------------
import simplejson as json

# Create your views here.

@api_view(['POST'])
def categoryPageNew(request,format=None):
    cat_name = request.data['category_name']


    obj = product_data.objects.filter(category = cat_name).values('id','name','image','diamond_quality','actual_price','selling_price','discount','weight','diamond_quality','diamond_size')
    price_obj = metal_price.objects.values().last()
    diamond_obj = diamond_pricing.objects.values()
    # ----------------------- userdefined functions --------------------------------------------
    def func_eval_first_index(value):
        return eval(value)[0][0]
    def func_image_first(value):
        return value.split(',')[0]
    #-------------------------------------------------------------------------------------------
    df = pd.DataFrame(obj)
    # df['actual_price'] = df['actual_price'].apply(func_eval_first_index)
    # df['selling_price'] = df['selling_price'].apply(func_eval_first_index)
    df['actual_price'] = df['actual_price']
    df['selling_price'] = df['selling_price']
    df['image'] = df['image'].apply(func_image_first)
    
    resp = df.to_dict(orient='records')

    res = {
            'category':cat_name,
            'data':resp,
          }
    try:
        token = request.data['token']
        try:
            user = user_data.objects.get(token = token)
            wishlist_array = user_whishlist.objects.filter(user_id = user.id).values_list('product_id',flat=True)
            res['wishlist_array'] = wishlist_array

        except:
            res = {
                    'status':False,
                    'message':'Something went wrong'
                }
    except:
        pass

    
    return Response(res)


@api_view(['POST'])
def productDetails(request,format=None):
    id = request.data['product_id']
    obj = product_data.objects.filter(id=id).values().last()
    res = {}
    res['product_id'] = obj['id']
    res['name'] = obj['name']
    res['category'] = obj['category']
    res['gender'] = 'Male' if obj['gender'] == 'M' else ('Female' if obj['gender'] == 'F' else 'Unisex')
    res['size'] = obj['size'].split(',')
    res['weight'] = obj['weight'].split(',')
    res['diamond_quality'] = obj['diamond_quality'].split(',')
    res['diamond_size'] = obj['diamond_size'].split(',')
    res['image'] = obj['image'].split(',')
    res['discount'] = '10'
    # ---------------------------Pricing---------------------------------------------------------------------
    metal_obj = metal_price.objects.values().last()
    diamond_obj = diamond_pricing.objects.values()
    weight_0 = res['weight'][0].split('/')
    
    sum = 0
    metal_sum = 0
    if len(weight_0)>1:
        metal_sum = metal_sum + ( eval(metal_obj['platinum']) * eval(weight_0[0]) )
        metal_sum = metal_sum + ( eval(metal_obj['gold']) * eval(weight_0[1]) )
    else:
        metal_sum = metal_sum + ( eval(metal_obj['platinum']) * eval(weight_0[0]) )
    sum = sum+ metal_sum

    if res['diamond_quality'][0] != 'P':
        diamond_sum = diamond_obj.filter(diamond_quality = res['diamond_quality'][0].strip(),diamond_size = res['diamond_size'][0].strip()).last()
        sum = sum+ eval(diamond_sum['diamond_pricing'])
    
    if len(weight_0)>1:
        making_price = ( eval(weight_0[0]) + eval(weight_0[1]) ) * eval(metal_obj['making_charges'])
        sum = sum + making_price
    else:
        making_price = eval(weight_0[0]) * eval(metal_obj['making_charges'])
        sum = sum + making_price


    res['actual_price'] = round(sum,2)
    res['selling_price'] = round(sum,2)
    return Response(res)


@api_view(['POST'])
def priceCalculation(request,format=None):
    try:
        data = request.data
        diamond_quality = data['diamond_quality']
        diamond_size = data['diamond_size']
        size = data['size']
        weight = data['weight'].split('/')
        metal_obj = metal_price.objects.values().last()
        diamond_obj = diamond_pricing.objects
        
        sum = 0
        metal_sum = 0
        
        if diamond_quality != 'P':
            print('###############',size,weight)
            diamond_sum = eval(diamond_obj.filter(diamond_quality = diamond_quality,diamond_size = diamond_size.strip()).values_list('diamond_pricing',flat=True)[0])
            sum = sum + diamond_sum
        

        if len(weight)>1:
            metal_sum = metal_sum + ( eval(metal_obj['platinum']) * eval(weight[0]) )
            metal_sum = metal_sum + ( eval(metal_obj['gold']) * eval(weight[1]) )
        else:
            metal_sum = metal_sum + ( eval(metal_obj['platinum']) * eval(weight[0]) )
        sum = sum+ metal_sum
        

        
        if len(weight)>1:
            making_price = ( eval(weight[0]) + eval(weight[1]) ) * eval(metal_obj['making_charges'])
        else:
            making_price = eval(weight[0]) * eval(metal_obj['making_charges'])
        sum = sum + making_price

        res = {
                'status':True,
                'selling_price':str(round(sum,2)),
                'actual_price':str(round(sum,2))
                }
        return Response(res)
    except:
        res = {
                'status':False,
                'message':'something went wrong refresh again'
                }
        return Response(res)



def new(request):
    pass