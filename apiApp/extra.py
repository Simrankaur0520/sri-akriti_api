# @api_view(['GET'])
# def navbar(request,format=None):
#     df = pd.read_csv('sri_akriti.csv')
#     titles = list(set(list(df['Category'])))
#     nav = []
#     for i in range(len(titles)):
#         res = {}
#         res['title'] = titles[i]
#         res['id'] = i
#         res['routes'] = '/single-category/'+titles[i]
#         res['sub'] = ['SHOP BY STYLE','SHOP FOR WHOM','GIFTING']
#         sub_sub = []
#         for k in res['sub']:
#             if k == 'SHOP BY STYLE':
#                 l = []
#                 for j in list(set(list(df.loc[df['Category'] == titles[i]]['Sub Category']))):
#                     l.append({'link_name':j,'link_path':"/"+j})
#                 sub_sub.append(l)
#             elif k == 'SHOP FOR WHOM':
#                 l = []
#                 for j in list(set(list(df.loc[df['Category'] == titles[i]]['Gender']))):
#                     l.append({'link_name':j,'link_path':"/"+j})
#                 sub_sub.append(l)
#             else:
#                 l = [
#                         {
#                         "link_name": "Birthday Gift",
#                         "link_path": "/birthday-gift"
#                         },
#                         {
#                         "link_name": "Aniversary Gift",
#                         "link_path": "/aniversary-gift"
#                         },
#                         {
#                         "link_name": "Valentines Day Gift",
#                         "link_path": "/valentines-gift"
#                         },
#                         {
#                         "link_name": "Personal Gift",
#                         "link_path": "/personal-gift"
#                         }
#                     ]
#                 sub_sub.append(l)
#         res['sub_sub'] = sub_sub
#         nav.append(res)
#     res = {}
#     res['title'] = 'COLLECTION'
#     res['id'] = 11
#     res['routes'] = '/single-category/COLLECTION'
#     res['sub'] = ['SHOP BY STYLE','SHOP FOR WHOM','GIFTING']
#     sub_sub = []
#     for k in res['sub']:
#         if k == 'SHOP BY STYLE':
#             l = []
#             for j in list(set(list(df['Sub Category']))):
#                 l.append({'link_name':j,'link_path':"/"+j})
#             sub_sub.append(l[:6])
#         elif k == 'SHOP FOR WHOM':
#             l = []
#             for j in list(set(list(df['Gender']))):
#                 l.append({'link_name':j,'link_path':"/"+j})
#             sub_sub.append(l)
#         else:
#             l = [
#                     {
#                     "link_name": "Birthday Gift",
#                     "link_path": "/birthday-gift"
#                     },
#                     {
#                     "link_name": "Aniversary Gift",
#                     "link_path": "/aniversary-gift"
#                     },
#                     {
#                     "link_name": "Valentines Day Gift",
#                     "link_path": "/valentines-gift"
#                     },
#                     {
#                     "link_name": "Personal Gift",
#                     "link_path": "/personal-gift"
#                     }
#                 ]
#             sub_sub.append(l)
#     res['sub_sub'] = sub_sub
#     nav.append(res)
#     nav1 = [{
#       "title": "ABOUT US",
#       "id": 6,
#       "routes": "/about-us"
#     },
#     {
#       "title": "ACCOUNT",
#       "id": 7,
#       "routes": "/account"
#     },
#     {
#       "title": "WISHLIST",
#       "id": 8,
#       "routes": "/wishlist"
#     },
#     {
#       "title": "STORE",
#       "id": 9,
#       "routes": "/store"
#     }]
#     nav = nav + nav1
#     return Response(nav)



# @api_view(['GET'])
# def landingPage(request,format=None):
#     landing_page_data = {

#     'first_section': {
#         'section_image': "media/hero-img.png",
#                     },
#     'third_section': [
#                         {
#                             'title': 'NECKLESS COLLECTIONS',
#                             'image': 'media/bracelet.png',
#                             'route': '/single-category/neckless',
#                         },
#                         {
#                             'title': 'BRACELET COLLECTIONS',
#                             'image': 'media/chain.png',
#                             'route': '/single-category/bracelet'
#                         },
#                     ],
#     'fourth_section': {
#                         'section_title': 'Made to last longer than life',
#                         'carousal_images': [
#                                                 { 'route': '/product-details' , 'image': 'media/ring_1.png'}, 
#                                                 { 'route': '/product-details' , 'image': 'media/ring_2.png'}, 
#                                                 { 'route': '/product-details' , 'image': 'media/chain_1.png'}, 
#                                                 { 'route': '/product-details' , 'image': 'media/chain_2.png'}, 
#                                                 { 'route': '/product-details' , 'image': 'media/ring_1.png'}, 
#                                                 { 'route': '/product-details' , 'image': 'media/ring_2.png'}, 
#                                                 { 'route': '/product-details' , 'image': 'media/chain_1.png'}, 
#                                                 { 'route': '/product-details' , 'image': 'media/chain_2.png'},
#                                             ],
#                      },

#                         }     

#     return Response(landing_page_data)  




# @api_view(['POST'])
# def categoryPage(request,format=None):
#     title = request.data['title']
#     desc = "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Atque, laborum odio? Sunt, modi tempora sint reprehenderit corrupti laboriosam molestias consequatur."
#     df = pd.read_csv('sri_akriti.csv')
#     if title == 'COLLECTION':
#         ndf = df
#     else:
#         ndf = df.loc[df['Category'] == title]

#     product = []
#     for i in range(ndf.shape[0]):
#         d = {
#             'product_id':i+1,
#             'product_name':list(ndf['Product Name'])[i],
#             'price':list(ndf['Offer Price'])[i],
#             'image':'media/products/'+list(ndf['Product Name'])[i]+'.png'
#         }
#         product.append(d)
#     res = {
#         'category':title,
#         'category_details':desc,
#         'category_image': 'media/products/'+list(ndf['Product Name'])[i]+'.png',
#         'products':product
#     }
#     return Response(res)


# def index(request):
#     df = pd.read_csv('new_rings.csv')
#     # print(df.columns)
#     for i in range(df.shape[0]):
#         name = list(df['Product Name'])[i].strip()   
#         gender =  list(df['M or F'])[i].strip()
#         dq =  list(df['Diamond Quality'])[i].strip()
#         size =  list(df['Size'])[i]
#         weight =  list(df['Weight'])[i]
#         ap =  list(df['Actual Price'])[i]
#         sp =  list(df['Selling Price'])[i]
#         discount =  list(df['Discount'])[i]
#         if name not in product_data.objects.values_list('name',flat=True):
#             data = product_data(
#                                 name = name,
#                                 image =  'media/products/mock_product.png',
#                                 gender = gender,
#                                 diamond_quality = dq,
#                                 size =  size,
#                                 weight =  weight,
#                                 actual_price =  ap,
#                                 selling_price =  sp,
#                                 discount =  discount,
#                                 status = 'Active',
#                             )
#             data.save()
#             print(i)
#     return HttpResponse('Hello World')



