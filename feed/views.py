import json, jwt

from django.shortcuts   import render
from django.views       import View
from django.http        import JsonResponse

from user.models        import User
from feed.models        import Feed, ImageUrl, Comment
from product.models     import Product, ProductImageUrl

class FeedDetailView(View):
    # feed C (post)
            # product_id : 커뮤니티 메인 화면에서 피드 작성시 화면에 없음. 연결할 상품을 shell에서 지정해주기.후기는 자기가 구매한 제품에서 쓸 수 있어서..(자기 구매내역이라든가.. 상품 상세페이지에서는 아니고.)
            # 사용자가 누군지는 로그인 판별 데코레이터에서 받아오기.. 여기서는 request.user로 user_id를 알 수 있음.
            # created_at, updated_at은 자동으로 들어감
            # description은 반드시 값 받아야 됨
            # like_number은 피드 생성시에는 값을 받을 수 없음. default=0으로 해줘야 됨.
            # tag_item_number은 일단 값을 받지 않고 null로 두기.. 추후 shell에서 넣어주기

    # 데코레이터로 로그인 판단 하지 않기. 미가입자여도 feed R할 수 있어야 됨.
    def get(self, request, feed_id):    # feed R
        try:
            feed_data = Feed.objects.get(id=feed_id)

            current_user_id = 1 # 임시
            # token 발급 코드 합치고 테스트하기
            # current_user_id = request.headers.get('AUTHORIZATION')
            # if current_user_id:
                # current_user_id = jwt.decode(current_user_id, JWT_AUTH['SECRET_KEY'],
                        # algorithms=JWT_AUTH['ALGORITHM'])['id']

            feed_writer         = User.objects.get(feed=feed_data['user'])
            feed_writer_data    = [{
                'id'    : feed_writer.id,
                'name'  : feed_writer.name,
                'about' : feed_writer.get('about')
            }]

            product_id      = feed_data.get('product')
            product         = Product.objects.filter(id=product_id)
            product_data    = []
            if product_id:
                product_data = [{
                    'id'            : product_id,
                    'name'          : product['name'],
                    'price'         : product['price'],
                    'discount_rate' : product['discount_rate'],
                    'main_image'    : ProductImageUrl.objects.filter(product=product_id,
                        is_main=1)[0].get('image_url')
                }]


            # image_urls table에서 해당 feed_id를 가진 이미지 다 가져오기
            image_list      = list(ImageUrl.objects.filter(feed=feed_id).values())
            comment_list    = list(Comment.objects.filter(feed=feed_id).values())

            return JsonResponse({
                'user_id'           : current_user_id,  # 미가입자는 null
                'feed_writer'       : feed_writer_data, # feed 작성자에 대한 정보. key: id, name, about
                'feed_id'           : feed_id,
                'created_at'        : feed_data.created_at,
                'description'       : feed_data.description,
                'image_list'        : image_list,   # feed의 이미지 모음. key: feed(feed의 id), image_url
                'like_number'       : feed_data.like_number,
                'tag_item_number'   : feed_data.tag_item_number,
                'product'           : product_data, # 후기가 아니라면 빈 배열, 후기라면 product에 대한 정보가 든 배열. key: id, name, price, discount_rate, main_image
                'comment'           : comment_list, # feed의 comment들을 모은 배열. key: user(user의 id), feed(feed의 id), created_at, updated_at, content(comment의 내용)

                # column명(user_id)으로 나오는지 변수명(user)으로 나오는지 체크하기
            }, status=200)
        
        except jwt.exceptions.DecodeError:
            return JsonResponse({'MESSAGE' : 'INVALID_TOKEN'}, status=400)

        # except User.DoesNotExist:
            # return JsonResponse({'MESSAGE : INVALID_USER'}, status=400)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)



    #def patch(self, request, feed_id):  # feed U
        # 로그인 확인 + 해당 feed를 작성한 사용자인지 확인
        # -> 로그인 데코레이터 사용하고 user_id = request.user로 user_id 뽑아내기
        # 그 후 



    #def delete(self, request, feed_id): # feed D
        # 로그인 확인 + 해당 feed를 작성한 사용자인지 확인



    #def post(self, request, feed_id):    # comment C
        # 로그인 확인해서 user_id 뽑아내고 그걸 comment의 user로 넣기
        # feed_id로 받은 걸 comment의 feed로 넣기.
        # body로 받은 코멘트 내용을 comment의 content로 넣기
        # created_at과 updated_at은 자동으로 들어감.

