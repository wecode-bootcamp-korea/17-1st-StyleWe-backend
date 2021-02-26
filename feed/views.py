import json, jwt
from json.decoder       import JSONDecodeError

from django.views       import View
from django.http        import JsonResponse

from user.utils         import login_decorator, get_current_user_id
from user.models        import User
from feed.models        import Feed, ImageUrl, Comment
from product.models     import Product, ProductImageUrl

class FeedView(View):
    def get(self, request):
        try:
            MAXIMUM_COMMENT = 2
            feed_list   = []
            offset      = int(request.GET.get('offset', 0))
            limit       = int(request.GET.get('limit', 30))
        
            for feed in Feed.objects.all().order_by('-id'):
                feed_data = {
                    'feed_basic_data' : {
                        'feed_id'         : feed.id, 
                        'feed_user'       : feed.user.nickname,
                        'created_at'      : feed.created_at,
                        'description'     : feed.description,
                        'like_number'     : feed.like_number,
                        'tag_item_number' : feed.tag_item_number,
                        'feed_main_image' : feed.imageurl_set.values('image_url').first()
                        },
    
                    'product_data'   : {
                        'product_id'     : feed.product_id,
                        'product_name'   : feed.product.name,
                        'discount_rate'  : feed.product.discount_rate,
                        'price'          : feed.product.price,
                        'product_image'  : feed.product.productimageurl_set.get(is_main=1).image_url
                        } if feed.product_id else {
                        'product_id'     : '',
                        'product_name'   : '',
                        'discount_rate'  : '',
                        'price'          : '',
                        'product_image'  : ''
                        },
    
                    'feed_comment_data'  : {
                        'feed_comment_count' : feed.comment_set.count(),
                        'comment_list'       : [{
                                'user'      : comment.user.nickname,
                                'content'   : comment.content
                            } for comment in feed.comment_set.all().order_by('-created_at')[:MAXIMUM_COMMENT]
                            ] if feed.comment_set.exists() else
                            [{
                                'user':'',
                                'content':''
                            }]
                        }
                    }
    
                feed_list.append(feed_data)
            feed_list = feed_list[offset:offset+limit]
    
            return JsonResponse({'feed_list': feed_list}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status=404)

class FeedDetailView(View):
    def get(self, request, feed_id):
        try:
            feed_data   = Feed.objects.get(id=feed_id)
            feed_writer = feed_data.user
            product_data = []
            if feed_data.product_id:
                product      = Product.objects.get(id=feed_data.product_id)
                product_data = [{
                    'id'            : product.id,
                    'product_name'  : product.name,
                    'price'         : product.price,
                    'discount_rate' : product.discount_rate,
                    'product_image' : ProductImageUrl.objects.filter(product_id=feed_data.product_id, is_main=1)[0].image_url
                }]
            else:
                product_data = False

            if feed_data.comment_set.exists():
                comment_list = []
                for item in feed_data.comment_set.all():
                    comment = {
                        'user'          : User.objects.get(id=item.user_id).nickname,
                        'user_id'       : item.user_id,
                        'content'       : item.content,
                        'created_at'    : item.created_at,
                    }
                    comment_list.append(comment)
            else:
                comment_list = False

            return JsonResponse({
                'current_user_id'   : get_current_user_id(request),
                'feed_basic_data'   : {
                    'feed_id'           : feed_id,
                    'feed_user'         : feed_writer.nickname,
                    'feed_user_id'      : feed_writer.id,
                    'feed_writer_about' : feed_writer.about,
                    'created_at'        : feed_data.created_at,
                    'description'       : feed_data.description,
                    'like_number'       : feed_data.like_number,
                    'tag_item_number'   : feed_data.tag_item_number,
                },
                'product_data'      : product_data,
                'feed_comment_data' : {
                    'feed_comment_count' : feed_data.comment_set.count(),
                    'comment_list'       : comment_list,
                },
                'feed_image_data'   : [{'url' : item.image_url} for item in feed_data.imageurl_set.all()],
            }, status=200)

        except ValueError:
            return JsonResponse({'MESSAGE' : 'INVALID_VALUE_TYPE'}, status=400)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

        except Feed.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'INVALID_FEED_ID'}, status=404)

        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'INVALID_PRODUCT_ID'}, status=404)

    @login_decorator
    def patch(self, request, feed_id):
        try:
            target_feed = Feed.objects.get(id=feed_id)
            
            if target_feed.user_id == request.user.id:
                new_description = json.loads(request.body)['description']
                if not new_description:
                    return JsonResponse({'MESSAGE' : 'NO_FEED_DESCRIPTION'}, status=400)

                target_feed.description = new_description
                target_feed.save()
                
                return JsonResponse({'MESSAGE' : 'FEED_DESCRIPTION_UPDATED'}, status=200)
            
            return JsonResponse({'MESSAGE' : 'USER_WITHOUT_AUTHORITY'}, status=403)

        except ValueError:
            return JsonResponse({'MESSAGE' : 'INVALID_VALUE_TYPE'}, status=400)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

        except Feed.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'INVALID_FEED_ID'}, status=404)

    @login_decorator
    def delete(self, request, feed_id):
        try:
            target_feed = Feed.objects.get(id=feed_id)
            
            if target_feed.user_id == get_current_user_id(request):
                Feed.objects.get(id=feed_id).delete()
                
                return JsonResponse({'MESSAGE' : 'FEED_DELETED'}, status=204)
            
            return JsonResponse({'MESSAGE' : 'USER_WITHOUT_AUTHORITY'}, status=403)
        
        except ValueError:
            return JsonResponse({'MESSAGE' : 'INVALID_VALUE_TYPE'}, status=400)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

        except Feed.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'INVALID_FEED_ID'}, status=404)
