import simplejson as json
import json

import razorpay
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import OrderSerializer

from .models import Order,user_data,user_cart,order_status

from django.views.decorators.csrf import csrf_exempt


@api_view(['POST'])
def start_payment(request):
    amount = request.data['amount']
    name = request.data['name']
    token=request.data['token']

    client = razorpay.Client(auth=('rzp_test_gHJS0k5aSWUMQc', '8hPVwKRnj4DZ7SB1wyW1miaf'))
    user=user_data.objects.filter(token=token).values()
    #cart_to_order_shift(token)

    payment = client.order.create({"amount": eval(amount) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})

    order = Order.objects.create(order_product=name, 
                                 order_amount=amount, 
                                 order_payment_id=payment['id'])

    serializer = OrderSerializer(order)

    """order response will be 
    {'id': 17, 
    'order_date': '23 January 2021 03:28 PM', 
    'order_product': '**product name from frontend**', 
    'order_amount': '**product amount from frontend**', 
    'order_payment_id': 'order_G3NhfSWWh5UfjQ', # it will be unique everytime
    'isPaid': False}"""

    data = {
        "payment": payment,
        "order": serializer.data,
        "user details" :user
    }
    return Response(data)



@csrf_exempt
@api_view(['POST'])
def handle_payment_success(request):
    # request.data is coming from frontend
    # print(type(request.data["response"]))
    res = eval(request.data["response"])

    """res will be:
    {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
    'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
    'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
    this will come from frontend which we will use to validate and confirm the payment
    """

    ord_id = ""
    raz_pay_id = ""
    raz_signature = ""

    # res.keys() will give us list of keys in res
    for key in res.keys():
        if key == 'razorpay_order_id':
            ord_id = res[key]
        elif key == 'razorpay_payment_id':
            raz_pay_id = res[key]
        elif key == 'razorpay_signature':
            raz_signature = res[key]

    # get order by payment_id which we've created earlier with isPaid=False
    order = Order.objects.get(order_payment_id=ord_id)

    # we will pass this whole data in razorpay client to verify the payment
    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
    }

    client = razorpay.Client(auth=('rzp_test_gHJS0k5aSWUMQc', '8hPVwKRnj4DZ7SB1wyW1miaf'))

    # checking if the transaction is valid or not by passing above data dictionary in 
    # razorpay client if it is "valid" then check will return None
    check = client.utility.verify_payment_signature(data)

    if not check:
        print("Redirect to error url or error page")
        return Response({'error': 'Something went wrong'})

    # if payment is successful that means check is None then we will turn isPaid=True
    order.isPaid = True
    order.save()

    res_data = {
        'message': 'payment successfully received!'
    }

    return Response(res_data)

'''@api_view(['GET'])
def cart_to_order_shift(request,format=None):
    #token=token
    #user = user_data.objects.get(token = token)
    items=user_cart.objects.values()
    #for i in items:
     #   print(i)
    
    delivery_status=models.TextField(blank=True)
    date=models.TextField(blank=True)
    product_img=models.TextField(blank=True)
    product_name=models.TextField(blank=True)
    product_code=models.TextField(blank=True)
    product_price=models.TextField(blank=True)
    user_id=models.TextField(blank=True)
    payment_status=models.BooleanField(default=False)

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
    cart_product_id": 21,
            "id": 893,
            "image": "media/products/mock_product.png",
            "title": "SA-BAND-057",
            "quantity": "2",
            "price": 276639.957      

    order_res={
        "Delivery_Status":"Placed",
        #'date':"",
        'product_img':items.image,
        'product_name':items.name,
        'product_code':items.id,
        'product_price':items.price/items.quantity,
        #'order_id':Order_id,
        'user_id':user.id,
        'payment_status':"True"
        }
    #res=items.product_id
    return Response(items)'''
        






   


    

