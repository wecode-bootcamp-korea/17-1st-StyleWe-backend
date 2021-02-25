import json, jwt
from json.decoder import JSONDecodeError

from django.shortcuts   import render
from django.views       import View
from django.http        import JsonResponse

from user.models        import User
from feed.models        import Feed, ImageUrl, Comment
from product.models     import Product, ProductImageUrl
from user.utils         import login_decorator, get_current_user_id

class FeedDetailView(View):
    def get(self, request, feed_id):
        try:
            current_user_id = get_current_user_id(request)

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
            product_data    = False
            if product_id:
                product         = Product.objects.get(id=product_id)
                product_data    = [{
                    'id'            : product_id,
                    'product_name'  : product.name,
                    'price'         : product.price,
                    'discount_rate' : product.discount_rate,
                    'product_image' : ProductImageUrl.objects.filter(product_id=product_id, is_main=1)[0].image_url
                }]

            comments = feed_data.comment_set.all()
            comment_list = False
            if comments:
                comment_list = []
                for item in list(comments):
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
        
        except ValueError:
            return JsonResponse({'MESSAGE' : 'INVALID_TOKEN'}, status=400)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

        except Feed.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'INVALID_FEED_ID'}, status=400)

    @login_decorator
    def patch(self, request, feed_id):
        try:
            target_feed = Feed.objects.get(id=feed_id)
            
            if target_feed.user_id == request.user.id:
                new_description = json.loads(request.body)['description']
                if not new_description:
                    return JsonResponse({'MESSAGE' : 'NO_FEED_DESCRIPTION'}, status=400)

                current_feed = Feed.objects.get(id=feed_id)
                current_feed.description = new_description
                current_feed.save()
                
                return JsonResponse({'MESSAGE' : 'FEED_DESCRIPTION_UPDATED'}, status=200)
            
            return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status=400)

        except JSONDecodeError:
            return JsonResponse({'MESSAGE' : 'NO_FEED_DESCRIPTION'}, status=400)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

        except Feed.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'INVALID_FEED_ID'}, status=400)

    @login_decorator
    def delete(self, request, feed_id):
        try:
            target_feed = Feed.objects.get(id=feed_id)
            
            if target_feed.user_id == get_current_user_id(request):
                Feed.objects.get(id=feed_id).delete()
                
                return JsonResponse({'MESSAGE' : 'FEED_DELETED'}, status=200)
            
            return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status=400)
        
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

        except Feed.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'INVALID_FEED_ID'}, status=400)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)
