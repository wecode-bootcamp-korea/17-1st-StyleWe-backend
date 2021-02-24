import json, jwt

from django.shortcuts   import render
from django.views       import View
from django.http        import JsonResponse

from my_settings        import SECRET_KEY, ALGORITHM
from user.models        import User
from feed.models        import Feed, ImageUrl, Comment
from product.models     import Product, ProductImageUrl
#from user.utils         import login_decorator

class FeedDetailView(View):
    def get(self, request, feed_id):
        try:
            current_user_id = 0 # 미가입자
            if request.headers.get('AUTHORIZATION'):
                current_user_id = jwt.decode(request.headers['AUTHORIZATION'], SECRET_KEY, algorithms=ALGORITHM)['user_id']

            feed_data       = Feed.objects.get(id=feed_id)
            feed_writer     = User.objects.get(id=feed_data.user_id)
            feed_basic_data = {
                    'feed_id': feed_id,
                    'feed_user': feed_writer.nickname,
                    'feed_user_id': feed_writer.id,
                    'feed_writer_about': feed_writer.about,
                    'created_at': feed_data.created_at,
                    'description': feed_data.description,
                    'like_number': feed_data.like_number,
                    'tag_item_number': feed_data.tag_item_number,
            }

            product_id      = feed_data.product_id
            product_data    = []
            if product_id:
                product         = Product.objects.get(id=product_id)
                product_data    = [{
                    'id'            : product_id,
                    'product_name'  : product.name,
                    'price'         : product.price,
                    'discount_rate' : product.discount_rate,
                    'product_image' : ProductImageUrl.objects.filter(product_id=product_id, is_main=1)[0].image_url
                }]

            comment_list = []
            for item in list(feed_data.comment_set.all()):
                comment = {
                    'user'          : User.objects.get(id=item.user_id).nickname,
                    'user_id'       : item.user_id,
                    'content'       : item.content,
                    'created_at'    : item.created_at,
                }
                comment_list.append(comment)
            
            comment_data = {
                'feed_comment_count'    : len(feed_data.comment_set.all()),
                'comment_list'          : comment_list,
            }

            image_data = []
            i = 0
            for item in list(feed_data.imageurl_set.all()):
                image_data.append({i : item.image_url})
                i += 1

            return JsonResponse({
                'current_user_id'   : current_user_id,
                'feed_basic_data'   : feed_basic_data,
                'product_data'      : product_data,
                'feed_comment_data' : comment_data,
                'feed_image_data'   : image_data,
            }, status=200)
        
        except jwt.exceptions.DecodeError:
            return JsonResponse({'MESSAGE' : 'INVALID_TOKEN'}, status=400)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)



    #def patch(self, request, feed_id):  # feed U
        # 로그인 확인 + 해당 feed를 작성한 사용자인지 확인
        # -> 로그인 데코레이터 사용하고 user_id = request.user로 user_id 뽑아내기
        # 그 후 


    #@login_decorator
    #def delete(self, request, feed_id):
        #로그인 확인 + 해당 feed를 작성한 사용자인지 확인
        #try:
            #target_feed = Feed.objects.get(id=feed_id)
            #if current_user_id == 
            #Feed.objects.get(id=feed_id).delete()
        




    #def post(self, request, feed_id):    # comment C
        # 로그인 확인해서 user_id 뽑아내고 그걸 comment의 user로 넣기
        # feed_id로 받은 걸 comment의 feed로 넣기.
        # body로 받은 코멘트 내용을 comment의 content로 넣기
        # created_at과 updated_at은 자동으로 들어감.

