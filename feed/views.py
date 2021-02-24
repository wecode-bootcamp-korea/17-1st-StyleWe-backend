import json

from django.http.response   import JsonResponse
from django.views           import View

from .models                import Feed, Comment, ImageUrl
from user.models            import User
from product.models         import Product

class FeedView(View):    
    def get(self, request):
        MAXIMUM_COMMENT = 2
        feed_list   = []
        # offset      = int(request.GET.get('offset'))
        # limit       = int(request.GET.get('limit'))
    
        for feed in Feed.objects.all().order_by('-id'):

            # 피드 정보
            feed_basic_data = {
                'feed_id'         : feed.id, 
                'feed_user'       : feed.user.nickname,
                'created_at'      : feed.created_at,
                'description'     : feed.description,
                'like_number'     : feed.like_number,
                'tag_item_number' : feed.tag_item_number,
                'feed_main_image' : feed.imageurl_set.values('image_url').first()
                }

            # 피드의 상품 정보
            if feed.product_id:
                product_feed_id = feed.product
                product_id      = feed.product.id 
                product_name    = feed.product.name
                discount_rate   = feed.product.discount_rate
                price           = feed.product.price
                product_image   = feed.product.productimageurl_set.get(is_main=1).image_url

                product_data = {
                    'product_name'      : product_name,
                    'discount_rate'     : discount_rate,
                    'price'             : price,
                    'product_image'     : product_image
                    }
            else:
                product_data = {
                    'product_name'      : '',
                    'discount_rate'     : '',
                    'price'             : '',
                    'product_image'     : ''
                }
            
            # 피드의 댓글
            if feed.comment_set.exists():
                feed_comment_count      = feed.comment_set.all().count()                   
                feed_comment_new        = list(feed.comment_set.values('content').order_by('-created_at'))
                feed_comment_user_id    = list(feed.comment_set.values('user_id').order_by('-created_at'))

                # comment_list = []
                # for i in range(MAXIMUM_COMMENT):
                #     comment_user_id         = feed_comment_user_id[i]
                #     comment_user_nickname   = User.objects.get(id = comment_user_id['user_id']).nickname
                #     comment_new             = feed_comment_new[i]['content']
                        
                #     comment = {'user' : comment_user_nickname, 'content' : comment_new}
                #     comment_list.append(comment)
                if feed_comment_count >= MAXIMUM_COMMENT:        
                    comment_list = []
                    for i in range(MAXIMUM_COMMENT):
                        comment_user_id         = feed_comment_user_id[i]
                        comment_user_nickname   = User.objects.get(id = comment_user_id['user_id']).nickname
                        comment_new             = feed_comment_new[i]['content']
                        
                        comment = {'user' : comment_user_nickname, 'content' : comment_new}
                        comment_list.append(comment)
                else:
                    comment_list = []
                    for i in range(MAXIMUM_COMMENT-1):
                        comment_user_id         = feed_comment_user_id[i]
                        comment_user_nickname   = User.objects.get(id = comment_user_id['user_id']).nickname
                        comment_new             = feed_comment_new[i]['content']
                        
                        comment = {'user' : comment_user_nickname, 'content' : comment_new}
                        comment_list.append(comment)
                                
                feed_comment_data = {
                    'feed_comment_count'    : feed_comment_count,
                    'comment_list'          : comment_list                    
                    }
            else:
                feed_comment_data = {
                    'feed_comment_count'    : '',
                    'comment_list'          : [{
                        'user':'',
                        'content':''
                    }]    
                }

            feed_data = {
                'feed_basic_data'       : feed_basic_data,
                'product_data'          : product_data,
                'feed_comment_data'     : feed_comment_data
            }

            feed_list.append(feed_data)
        # feed_list = feed_list[offset:offset+limit]

        return JsonResponse({'feed_list': feed_list}, status=200)