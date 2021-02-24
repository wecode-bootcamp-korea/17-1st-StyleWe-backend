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
        
        result                  = {}
        product_basic           = {}
        product_review          = {}    
        product_detail          = {}
        product_inquiry         = {}
        product_exchange_return = {}
        product_category_hot    = {}
        product_brand_hot       = {}

        product_basic['brand_name']         = product.brand.name
        product_basic['product_name']       = product.name
        product_basic['thumbnail_image']    = product.productimageurl_set.all().filter(is_main=1)[0].image_url
        product_basic['discount_rate']      = product.discount_rate
        product_basic['original_price']     = product.price
        product_basic['first_option_name']  = 'Color'
        product_basic['first_options']      = list(set(product_option['color'] for product_option in product.productoption_set.values()))
        product_basic['second_option_name'] = 'Size'
        product_basic['second_options']     = list(set(product_option['size'] for product_option in product.productoption_set.values()))

        product_review['feed_total_number'] = len(product.feed_set.all())
        product_review['feed_basic']        = [{
                                                'main_image': feed.imageurl_set.all()[0].image_url,
                                                'user_name': feed.user.user_name,
                                                'description': feed.description,
                                                'like_number': feed.like_number,
                                                'comment_number': len(feed.comment_set.all())
                                            } for feed in product.feed_set.filter(product_id=product_id)]
        #10개만 보내기 가능?

        product_detail['detail_images']  = [product_image_url['image_url'] for product_image_url in product.productimageurl_set.values()]
        
        product_inquiry['inquiry_total_number'] = len(product.productquestion_set.values())
        product_inquiry['Q&A']                  = [
                                                        {
                                                        'question':     [
                                                                            question.user.user_name,
                                                                            question.created_at,
                                                                            question.content
                                                                    ],
                                                        'answer':   [
                                                                    answer.content
                                                                ]
                                                    } 
                                                    for question in product.productquestion_set.all()
                                                    for answer in question.productanswer_set.all()
                                                ]

        #product_exchange_return = [고정되어있는 상황은 백엔드가 보내주는게 좋은지? 프론트가 고정시키는지? 후자 선호할듯]

        product_category_hot['subcategory_name']    = product.subcategory.name
        product_category_hot['items']               = [
                                                            {
                                                                'brand_name':category_hot_product.brand.name,
                                                                'name': category_hot_product.name,
                                                                'price': category_hot_product.price,
                                                                'discount_rate': category_hot_product.discount_rate,
                                                                'total_like_number': sum([category_hot_feed.like_number for category_hot_feed in category_hot_product.feed_set.all()]),
                                                                'total_feed_number': len(category_hot_product.feed_set.all())
                                                        }
                                                        for category_hot_product in Product.objects.filter(subcategory=product.subcategory_id)
                                                    ]

        product_brand_hot['brand_name'] = product.brand.name
        product_brand_hot['items']      = [
                                                {
                                                    'brand_name':brand_hot_product.brand.name,
                                                    'name': brand_hot_product.name,
                                                    'price': brand_hot_product.price,
                                                    'discount_rate': brand_hot_product.discount_rate,
                                                    'total_like_number': sum([brand_hot_feed.like_number for brand_hot_feed in brand_hot_product.feed_set.all()]),
                                                    'total_feed_number': len(brand_hot_product.feed_set.all())
                                            }
                                            for brand_hot_product in Product.objects.filter(brand=product.brand_id)
                                        ]

        result['product_basic']         = product_basic
        result['product_review']        = product_review
        result['product_detail']        = product_detail
        result['product_inquiry']       = product_inquiry
        result['product_category_hot']  = product_category_hot
        result['product_brand_hot']     = product_brand_hot

        return JsonResponse({'result':result}, status=200)
