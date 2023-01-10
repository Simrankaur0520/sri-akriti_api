from django.contrib import admin

from apiApp.models import product_data,diamond_pricing,metal_price
from apiApp.models import user_data,user_address,user_whishlist,user_cart

# Register your models here.

admin.site.register(product_data)
admin.site.register(user_data)
admin.site.register(user_address)
admin.site.register(user_whishlist)
admin.site.register(diamond_pricing)
admin.site.register(metal_price)
admin.site.register(user_cart)
