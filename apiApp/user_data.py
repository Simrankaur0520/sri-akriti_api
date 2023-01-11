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
from apiApp.models import user_data,user_address
from apiApp.models import user_whishlist
from apiApp.models import product_data

#----------------------------extra---------------------------------------------------
import simplejson as json
from apiApp.functions import profile_view


@api_view(['POST'])
def profileView(request,format=None):
    token = request.data['token']
    wishlist_product_array=[]
    try:
        user = user_data.objects.get(token = token)
        wishlist_view=user_whishlist.objects.filter(user_id=user.id).values_list('product_id',flat=True)
        wishlist_product_array=product_data.objects.filter(id__in=wishlist_view).values('name','category','image')
  
        user_res = {
                'name': user.name,
                'gender':user.gender,
                'dob':user.dob,
                'email':user.email,
                'phone_no':user.phone_no,
                'phone_code':user.phone_code,

               }

        add_res = user_address.objects.filter(user_id = user.id)\
                                      .values('id','add_line_1','add_line_2',
                                              'landmark','city','state',
                                              'country','pincode')                          
        res = {
                'status':True,
                'message':'Response created successfully',
                'user':user_res,
                'address':{
                            'content':add_res
                          },
                'wishlist':wishlist_product_array
              }
    except:
        res = {
                'status':False,
                'message': 'Something went wrong'        
              }
    return Response(res)


@api_view(['PUT'])
def profileEdit(request,formt=None):
    name = request.data['name']
    gender = request.data['gender']
    dob = request.data['dob']
    email = request.data['email']
    phone_code = request.data['phone_code']
    phone_no = request.data['phone_no']
    token = request.data['token']

    try:
        user_data.objects.get(token = token)
        user_data.objects.filter(token = token).update(
                                                        name = name,
                                                        email = email,
                                                        gender = gender,
                                                        dob = dob,
                                                        phone_code = phone_code,
                                                        phone_no = phone_no,
                                                      )
        res = {
               'status':True,
               'message': 'Profile updated successfully'
              }
    except:
        res = {
                'status':False,
                'message':'Something went wrong'
              }
    return Response(res)


@api_view(['POST'])
def addressAdd(request,format=None):
    token = request.data['token']
    add_line_1 = request.data['add_line_1']
    add_line_2 = request.data['add_line_2']
    landmark = request.data['landmark']
    city = request.data['city']
    state = request.data['state']
    country = request.data['country']
    pincode = request.data['pincode']
    try:
        user = user_data.objects.get(token = token)
    except:
        res = {
                'status':False,
                'message':'Something went wrong'
              }
        return Response(res)

    data = user_address(
                        user_id = user.id,
                        add_line_1 = add_line_1,
                        add_line_2 = add_line_2,
                        landmark = landmark,
                        city = city,
                        state = state,
                        country = country,
                        pincode = pincode,
                       )
    data.save()
    res = {
            'status': True,
            'message':'Address added successfully'
          }
    return Response(res)

@api_view(['PUT','POST','DELETE'])
def addressEdit(request,format=None):
    if request.method == 'DELETE':
        address_id = request.data['address_id']
        try:
            token = request.data['token']
            user = user_data.objects.get(token = token)
        except:
            res = {
                    'status':False,
                    'message':'Something went wrong'
                }
            return Response(res)

        try:
            user_address.objects.get(id = address_id)
        except:
            res = {
                    'status':False,
                    'message':'Something went wrong'
                }
            return Response(res)
        user_address.objects.filter(id = address_id).delete()
        res = profile_view(token)
        if res['status'] == True:
            res['message'] = 'Address deleted successfully'

        return Response(res)

    if request.method == 'POST':
        address_id = request.data['address_id']
        add_res = user_address.objects.filter(id = address_id)\
                                      .values('id','add_line_1','add_line_2',
                                              'landmark','city','state',
                                              'country','pincode','phone_no')  .last()   
        res = {
                'status':True,
                'message':'Response created successfully',
                'address':{
                            'content':add_res
                          }              
               }
        return Response(res)
        

    if request.method == 'PUT':
        address_id = request.data['address_id']
        add_line_1 = request.data['add_line_1']
        add_line_2 = request.data['add_line_2']
        landmark = request.data['landmark']
        city = request.data['city']
        state = request.data['state']
        country = request.data['country']
        pincode = request.data['pincode']

        try: 
            user_address.objects.get(id = address_id)
        except:
            res = {
                    'status':False,
                    'message':'Something went wrong'
                }
            return Response(res)
        obj = user_address.objects.filter(id = address_id)\
                                .update(
                                            add_line_1 = add_line_1,
                                            add_line_2 = add_line_2,
                                            landmark = landmark,
                                            city = city,
                                            state = state,
                                            country = country,
                                            pincode = pincode,   
                                        ) 
        res = {
                'status': True,
                'message':'Address updated successfully'
            }
        return Response(res)


@api_view(['POST'])
def userWishlist(request,format=None):
    if request.method == "POST":
        token = request.data['token']
        product_id = request.data['product_id']
        try:
            user = user_data.objects.get(token = token)
        except:
            res = {
                    'status':False,
                    'message':'Something went wrong'
                }
            return Response(res)
        wishlist_products = user_whishlist.objects.filter(user_id = user.id).values_list('product_id',flat=True).distinct()
        if product_id not in wishlist_products:   
            data = user_whishlist(
                                    product_id = product_id,
                                    user_id = user.id,
                                )
            data.save()
        else:
            user_whishlist.objects.filter(user_id = user.id,product_id=product_id).delete()
        
        wishlist_array = user_whishlist.objects.filter(user_id = user.id).values_list('product_id',flat=True)
        
        res = {
                'status':True,
                'message':'Product added to whishlist',
                'wishlist_array':wishlist_array,
              }
        return Response(res)

@api_view(['POST',"DELETE"])
def getUserWishlist(request,format=None):
    if request.method == "POST":
        token = request.data['token']
        try:
            user = user_data.objects.get(token = token)
        except:
            res = {
                    'status':False,
                    'message':'Something went wrong'
                }
            return Response(res)
        wishlist_array = user_whishlist.objects.filter(user_id = user.id).values_list('product_id',flat=True)
        wishlist_data = product_data.objects.filter(id__in = wishlist_array).values('id','name','image','diamond_quality')
        # ----------------------- userdefined functions --------------------------------------------
        def func_eval_first_index(value):
            return eval(value)[0][0]
        def func_image_first(value):
            return value.split(',')[0]
        #-------------------------------------------------------------------------------------------
        if(len(wishlist_data)>0):
            df = pd.DataFrame(wishlist_data)
            df['image'] = df['image'].apply(func_image_first)
            
            wishlist_data_res = df.to_dict(orient='records')
            res = {
                    'status':True,
                    'message':'User wishlist response',
                    'wishlist_data':wishlist_data_res,
                }
        else:
             res = {
                    'status':True,
                    'message':'User wishlist response',
                    'wishlist_data':[],
                }
        return Response(res)

    if request.method == "DELETE":
        token = request.data['token']
        product_id = request.data['product_id']
        try:
            user = user_data.objects.get(token = token)
        except:
            res = {
                    'status':False,
                    'message':'Something went wrong'
                }
            return Response(res)
        user_whishlist.objects.filter(product_id = product_id,user_id = user.id).delete()

        wishlist_array = user_whishlist.objects.filter(user_id = user.id).values_list('product_id',flat=True)
        wishlist_data = product_data.objects.filter(id__in = wishlist_array).values('id','name','image','diamond_quality')
        # ----------------------- userdefined functions --------------------------------------------
        def func_eval_first_index(value):
            return eval(value)[0][0]
        def func_image_first(value):
            return value.split(',')[0]
        #-------------------------------------------------------------------------------------------
        if(len(wishlist_data)>0):
            df = pd.DataFrame(wishlist_data)
            df['image'] = df['image'].apply(func_image_first)
            
            wishlist_data_res = df.to_dict(orient='records')
            res = {
                    'status':True,
                    'message':'product deleted from wishlist successfully',
                    'wishlist_array':wishlist_array,
                    'wishlist_data':wishlist_data_res,
                }
        else:
             res = {
                    'status':True,
                    'message':'product deleted from wishlist successfully',
                    'wishlist_array':wishlist_array,
                    'wishlist_data':[],
                }
        return Response(res)