import json
from operator import itemgetter

from django.shortcuts   import render
from django.http        import HttpResponse, JsonResponse
from django.views       import View

from product.models     import Product

class ProductView(View):
    def get(self, request, product_id):
        if not Product.objects.filter(id=product_id).exists():
            return JsonResponse({'message': 'PRODUCT_NOT_EXIST'}, status=404)

        product = Product.objects.get(id=product_id)

        product_basic = {
            'brand_name'            : product.brand.name,
            'product_name'          : product.name,
            'thumbnail_image'       : product.productimageurl_set.filter(is_main=1).first().image_url,
            'discount_rate'         : product.discount_rate,
            'original_price'        : product.price,
            'first_option_name'     : 'Color',
            'first_options'         : list(set(product_option['color'] for product_option in product.productoption_set.values())),
            'second_option_name'    : 'Size',
            'second_options'        : list(set(product_option['size'] for product_option in product.productoption_set.values()))
        }

        product_review = {
            'feed_total_number' : product.feed_set.count(),
            'feed_basic'        : [{
                'feed_id'           : feed.id,
                'main_image'        : feed.imageurl_set.filter().first().image_url,
                'user_name'         : feed.user.user_name,
                'description'       : feed.description,
                'like_number'       : feed.like_number,
                'comment_number'    : feed.comment_set.count()
            } for feed in product.feed_set.filter(product_id=product_id)]
        }

        product_detail = {
            'detail_images': [product_image_url['image_url'] for product_image_url in product.productimageurl_set.values()]
        }

        product_inquiry = {
            'inquiry_total_number'  : product.productquestion_set.count(),
            'Q&A'                   : [{
                'question'      : {
                    'user_name'     : question.user.user_name,
                    'created_at'    : question.created_at,
                    'content'       : question.content
                },
                'answer': {
                    'content': answer.content
                }
            } for question in product.productquestion_set.all() for answer in question.productanswer_set.all()]
        }

        product_category_hot = {
            'subcategory_name': product.subcategory.name,
            'items': sorted([{
                'product_id'        : category_hot_product.id,
                'brand_name'        : category_hot_product.brand.name,
                'name'              : category_hot_product.name,
                'price'             : category_hot_product.price,
                'discount_rate'     : category_hot_product.discount_rate,
                'total_like_number' : sum([category_hot_feed.like_number for category_hot_feed in category_hot_product.feed_set.all()]),
                'total_feed_number' : category_hot_product.feed_set.count()
            } for category_hot_product in Product.objects.filter(subcategory=product.subcategory_id)], key=itemgetter('total_like_number'), reverse=True)
        }

        product_brand_hot = {
            'brand_name': product.brand.name,
            'items': sorted([{
                'product_id'        : brand_hot_product.id,
                'brand_name'        : brand_hot_product.brand.name,
                'name'              : brand_hot_product.name,
                'price'             : brand_hot_product.price,
                'discount_rate'     : brand_hot_product.discount_rate,
                'total_like_number' : sum([brand_hot_feed.like_number for brand_hot_feed in brand_hot_product.feed_set.all()]),
                'total_feed_number' : brand_hot_product.feed_set.count()
            } for brand_hot_product in Product.objects.filter(brand=product.brand_id)], key=itemgetter('total_like_number'), reverse=True)
        }

        result = {
            'product_id'            : product_id,
            'product_basic'         : product_basic,
            'product_review'        : product_review,
            'product_detail'        : product_detail,
            'product_inquiry'       : product_inquiry,
            'product_category_hot'  : product_category_hot,
            'product_brand_hot'     : product_brand_hot
        }

        return JsonResponse({'result': result}, status=200)
