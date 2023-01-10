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
from apiApp.models import user_cart
from apiApp.models import diamond_pricing,metal_price

#----------------------------extra---------------------------------------------------
import simplejson as json
from apiApp.functions import profile_view


'''@api_view(['POST'])
def addToCart(request,format=None):
    if request.method == 'POST':
        token = request.data['token']
        product_id = request.data['product_id']
        size = request.data['size']
        diamond_quality = request.data['diamond_quality']
        weight=request.data['weight']
        quantity=request.data['quantity']
        try:
            user = user_data.objects.get(token = token)
        except:
            res = {
                    'status':False,
                    'message':'Something went wrong'
                }
            return Response(res)
        obj = user_cart.objects.filter(user_id = user.id,
                                       product_id = product_id,
                                       size = size,
                                       diamond_quality = diamond_quality).values()
        if len(obj) == 0:
            data = user_cart(
                                user_id = user.id,
                                product_id = product_id,
                                size = size,
                                diamond_quality = diamond_quality,
                                quantity = '1'

                            )
            data.save()
            res = {
                    'status' : True,
                    'message': 'Product added to cart successfully'
                }
        else:
            obj = user_cart.objects.filter(user_id = user.id,
                                       product_id = product_id,
                                       size = size,
                                       diamond_quality = diamond_quality).values().last()
            quantity = int(obj['quantity'])+1
            user_cart.objects.filter(user_id = user.id,
                                       product_id = product_id,
                                       size = size,
                                       diamond_quality = diamond_quality).update(quantity = quantity)
            res = {
                    'status' : True,
                    'message': 'Product already exist, quantity increased'
                  }
        return Response(res)'''

@api_view(['POST'])
def getUserCart(request,format=None):
    token = request.data['token']
    try:
        user = user_data.objects.get(token = token)
    except:
        res = {
                'status':False,
                'message':'Something went wrong'
            }
        return Response(res)
    products = product_data.objects.values()
    items = user_cart.objects.filter(user_id = user.id).values()
    
    product_list = []
    final_sub_total = 0
    final_making_charges = 0
    shipping = 100
    tax = 1.8
    for i in items:
        prod_data = products.filter(id = i['product_id']).last()
    
        prod_dict = {
                     'cart_product_id':i['id'],
                     'id':prod_data['id'],
                     'image':prod_data['image'].split(',')[0],
                     'title':prod_data['name'],
                     'quantity':i['quantity']
                    }
        
        # -------------------------- Diamond Price ---------------------------------
        diamond_quality = i['diamond_quality'].strip()
        diamond_size = i['diamond_size'].strip()
        quantity = eval(i['quantity'].strip())

        diamond_obj = diamond_pricing.objects.filter(diamond_quality = diamond_quality,
                                                     diamond_size = diamond_size).values().last()
        diamond_sum = eval(diamond_obj['diamond_pricing'].strip())

        #--------------------------- Metal Price -----------------------------------
        weight = i['weight'].strip().split('/')
        metal_obj = metal_price.objects.values().first()
        if len(weight) > 1:
            metal_sum = (eval(weight[0]) * eval(metal_obj['platinum'])) \
                        +\
                        (eval(weight[1]) * eval(metal_obj['gold']))
        else:
            metal_sum = eval(weight[0]) * eval(metal_obj['platinum'])


        # --------------------------- Making Charges -------------------------------
        if len(weight) > 1:
            making_charges_sum = (eval(weight[0]) * eval(metal_obj['making_charges'])) \
                        +\
                        (eval(weight[1]) * eval(metal_obj['making_charges']))
        else:
            making_charges_sum = eval(weight[0]) * eval(metal_obj['making_charges'])


        product_total = diamond_sum + metal_sum + making_charges_sum
        prod_dict['price'] = product_total*quantity
        product_list.append(prod_dict)
        final_sub_total = final_sub_total + diamond_sum + metal_sum
        final_making_charges = final_making_charges + making_charges_sum

    checkout = {
                'sub_total':{
                                'title':'Sub Total', 
                                'amount': str(round(final_sub_total,2)*quantity),
                            },
                'shipping': {
                                'title': 'Shipping',
                                'charges': shipping,
                            },
                'tax': {
                                'title': 'Estimated Tax',
                                'amount': str(tax)+'%',
                        },
                'making_charges': {
                                'title':'Making Charges',
                                'amount': str(round(final_making_charges,2)*quantity)
                            },
                'total': {
                                'title':'Estimated Total',
                                'amount': round((final_making_charges+final_sub_total)*quantity+shipping,2)
                            },
                }
    res = {
            'status':True,
            'message':'Cart generated',
            'products':product_list,
            'checkout_data': checkout
          }

    return Response(res)


@api_view(['POST'])
def cartQuantityUpdate(request,format=None):
    if request.method == 'POST':
        token = request.data['token']
        cart_product_id = request.data['cart_product_id']
        update_type = request.data['update_type']
        try:
            user = user_data.objects.get(token = token)
        except:
            res = {
                    'status':False,
                    'message':'Something went wrong'
                }
            return Response(res)
        
        if update_type == '+':
            obj = user_cart.objects.filter(user_id = user.id,
                                           id = cart_product_id).values().last()
            quantity = int(obj['quantity'])+1
            user_cart.objects.filter(user_id = user.id,
                                           id = cart_product_id).update(quantity = quantity)
        else:
            obj = user_cart.objects.filter(user_id = user.id,
                                           id = cart_product_id).values().last()
            if int(obj['quantity']) <=1:
                user_cart.objects.filter(user_id = user.id,
                                           id = cart_product_id).delete()
            else:
                quantity = int(obj['quantity'])-1
                user_cart.objects.filter(user_id = user.id,
                                           id = cart_product_id).update(quantity = quantity)
                    

        
        res = {
                'status':True,
                'message':'Quantity updated',
                # 'products':product_list,
                # 'checkout_data': checkout
            }

        return Response(res)



# ---------------------------------------------------------------------------------------------------------

@api_view(['POST'])
def addToCart(request,format=None):
    if request.method == 'POST':
        token = request.data['token']
        product_id = request.data['product_id']
        size = request.data['size']
        diamond_size=request.data['diamond_size']
        diamond_quality = request.data['diamond_quality']
        weight=request.data['weight']
        #----------------Checking for Product id in produt data

        try:
            product_data.objects.get(id=product_id)
            try:
                user = user_data.objects.get(token = token)
            except:
                res = {
                        'status':False,
                        'message':'Something went wrong'
                    }
                return Response(res)
            obj = user_cart.objects.filter(user_id = user.id,
                                        product_id = product_id,
                                        size = size,
                                        diamond_quality = diamond_quality,
                                        diamond_size=diamond_size,
                                        weight=weight).values()
            if len(obj) == 0:
                data = user_cart(
                                    user_id = user.id,
                                    product_id = product_id,
                                    size = size,
                                    diamond_quality = diamond_quality,
                                    quantity = '1',
                                    diamond_size=diamond_size,
                                    weight=weight

                                )
                data.save()
               
                res = {
                        
                        'status' : True,
                        'message': 'Product added to cart successfully'
                    }
                return Response(res)
            else:
                obj = user_cart.objects.filter(user_id = user.id,
                                        product_id = product_id,
                                        size = size,
                                        diamond_quality = diamond_quality,
                                        diamond_size=diamond_size,
                                            weight=weight).values().last()
                quantity = int(obj['quantity'])+1
                user_cart.objects.filter(user_id = user.id,
                                        product_id = product_id,
                                        size = size,
                                        diamond_quality = diamond_quality,
                                        diamond_size=diamond_size,
                                            weight=weight).update(quantity = quantity)
                res = {
                        'status' : True,
                        'message': 'Product already exist, quantity increased'
                    }
                return Response(res)
                    

        #---------------Except block for product id
        except:
            res = {
                    'status':False,
                    'message':'Something went wrong'
                }
            return Response(res)
@api_view(['POST'])
def checkout(request,format=None):
    if request.method == 'POST':
        token = request.data['token']
        try:
                user = user_data.objects.get(token = token)

        except:
            res = {
                    'status':False,
                    'message':'Something went wrong'
                    }
        delivery_details = {
            
            
                "heading":"Delivery Details",
                "label": "First Name",       
                'value' : user.name,
                'Email ID' :user.email,
                'Phone Number':user.phone_no
     
                
                } 
        user_add=user_address.objects.filter(user_id=user.id).values().last()
        add_line1=user_add['add_line_1']
        add_line2=user_add['add_line_2'] 
        landmark=user_add['landmark']
        state=user_add['state']
        locality=add_line1+add_line2+landmark
        address_details={
            "heading":"Address",
            "locality":locality,
            "City":user_add['city']+state,
            "Pincode":user_add["pincode"]

        }
    products = product_data.objects.values()
    items = user_cart.objects.filter(user_id = user.id).values()
    
    product_list = []
    final_sub_total = 0
    final_making_charges = 0
    shipping = 100
    tax = 1.8
    for i in items:
        prod_data = products.filter(id = i['product_id']).last()
        prod_array=[]
        prod_dict = {
                     'cart_product_id':i['id'],
                     'id':prod_data['id'],
                     'image':prod_data['image'].split(',')[0],
                     'title':prod_data['name'],
                     'quantity':i['quantity']
                    }
        prod_array=[prod_dict['cart_product_id'],prod_dict['id'],prod_dict['image'],prod_dict['title'],prod_dict['quantity']]
        
        # -------------------------- Diamond Price ---------------------------------
        diamond_quality = i['diamond_quality'].strip()
        diamond_size = i['diamond_size'].strip()
        quantity = eval(i['quantity'].strip())

        diamond_obj = diamond_pricing.objects.filter(diamond_quality = diamond_quality,
                                                     diamond_size = diamond_size).values().last()
        diamond_sum = eval(diamond_obj['diamond_pricing'].strip())

        #--------------------------- Metal Price -----------------------------------
        weight = i['weight'].strip().split('/')
        metal_obj = metal_price.objects.values().first()
        if len(weight) > 1:
            metal_sum = (eval(weight[0]) * eval(metal_obj['platinum'])) \
                        +\
                        (eval(weight[1]) * eval(metal_obj['gold']))
        else:
            metal_sum = eval(weight[0]) * eval(metal_obj['platinum'])


        # --------------------------- Making Charges -------------------------------
        if len(weight) > 1:
            making_charges_sum = (eval(weight[0]) * eval(metal_obj['making_charges'])) \
                        +\
                        (eval(weight[1]) * eval(metal_obj['making_charges']))
        else:
            making_charges_sum = eval(weight[0]) * eval(metal_obj['making_charges'])


        product_total = diamond_sum + metal_sum + making_charges_sum
        prod_dict['price'] = product_total*quantity
        product_list.append(prod_dict)
        final_sub_total = final_sub_total + diamond_sum + metal_sum
        final_making_charges = final_making_charges + making_charges_sum

    checkoutt = {
                'sub_total':{
                                'title':'Sub Total', 
                                'amount': str(round(final_sub_total,2)*quantity),
                            },
                'shipping': {
                                'title': 'Shipping',
                                'charges': shipping,
                            },
                'tax': {
                                'title': 'Estimated Tax',
                                'amount': str(tax)+'%',
                        },
                'making_charges': {
                                'title':'Making Charges',
                                'amount': str(round(final_making_charges,2)*quantity)
                            },
                'total': {
                                'title':'Estimated Total',
                                'amount': round((final_making_charges+final_sub_total)*quantity+shipping,2)
                            },
                }
   
   
    res={
        "form": {
            "header": {
            "heading": "Delivery Details",
            "sub_heading": "Edit"
            },
            "content": [
            {
                "label": "Full Name",
                'value' : user.name,
            },
            {
                "label": "Email ID",
                'value' : user.email,
            },
            {
                "label": "Phone Number",
                'value' : user.phone_no,
            }
            ]
        },
        "address": {
            "header": {
            "heading": "Address",
            "sub_heading": "Edit"
            },
            "content": [
            {
                "locality": locality,
                "city": user_add['city']+state,
                "pincode": user_add["pincode"]
            }
            ]
        },
        "card": {
            "header": {
            "heading": "Card",
            "sub_heading": "Edit"
        },
            "content": [
        {
            "number": "4454-0213-4594-4523",
            "cvv": "623",
            "name": "Vicky Waelchi",
            "expiry": "12/2023"
        }
        ]
        },
        "item": {
            "header": {
            "heading": "Item Details",
            "sub_heading": "Edit"
            },
            "content":  prod_dict
            },
        "checkout_data": {
            "coupon": {
            "title": "Coupon Code",
            "button": "Add"
            },
            "packaging": {
            "title": "Gift Packaging",
            "button": "Add"
            },
            "sub_total": {
            "title": "Sub Total",
            "amount": str(round(final_sub_total,2)*quantity)
            },
            "shipping": {
            "title": "Shipping",
            "charges": shipping,
            },
            "tax": {
            "title": "Estimated Tax",
            "amount": str(tax)+'%',
            },
            "total": {
            "title": "Estimated Total",
            "amount": round((final_making_charges+final_sub_total)*quantity+shipping,2)
            },
        "checkout_button": "CONTINUE"
    }}
    
                

      

                            
    return Response(res)

        
            
                


        