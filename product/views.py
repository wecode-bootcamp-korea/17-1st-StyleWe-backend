import json

from django.shortcuts   import render
from django.http        import HttpResponse, JsonResponse
from django.views       import View

from product.models     import Product

class ProductView(View):
    def get(self, request, product_id):
        if product_id is None:
            return JsonResponse({'message':'PRODUCT_NOT_EXIST'}, status=404)
        product = Product.objects.get(id=product_id)
        
        result          = {}
        product_basic   = {}
        product_review  = {}

        product_basic['brand_id']           = product.brand_id
        product_basic['brand_name']         = product.brand.name
        product_basic['product_name']       = product.name
        product_basic['thumbnail_image']    = product.productimageurl_set.all().filter(is_main=1)[0].image_url
        product_basic['discount_rate']      = product.discount_rate
        product_basic['original_price']     = product.price
        product_basic['first_option_name']  = 'Color'
        product_basic['first_options']      = [i['name'] for i in product.color.values().distinct()]
        product_basic['second_option_name'] = 'Size'
        product_basic['second_options']     = [i['name'] for i in product.color.values().distinct()]
        result['product_basic'] = product_basic

        product_review['feed_total_number'] = len(product.feed_set.all())
        product_review['feed_basic']        = [{
                    'main_image': ,
                    'user_name':,
                    'description':,
                    'like_number': product.feed_set.like_number,
                    'comment_number': product.feed_set.
                    } for i in product.feed_set.filter(product_id=product_id)
        
        return JsonResponse({'result':result}, status=200)
