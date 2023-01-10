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

#----------------------------extra---------------------------------------------------
import simplejson as json



def profile_view(token):
    try:
        user = user_data.objects.get(token = token)
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
                          }
              }
    except:
        res = {
                'status':False,
                'message': 'Something went wrong'        
              }
    return(res)