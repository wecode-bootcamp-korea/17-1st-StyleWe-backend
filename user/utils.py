import jwt
import json

from django.http        import JsonResponse

from my_settings        import SECRET_KEY, ALGORITHM
from user.models        import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token    = request.headers['Authorization']
            payload         = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
            user            = User.objects.get(id=payload['user_id'])
            request.user    = user

            return func(self, request, *args, **kwargs)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'MESSAGE':'INVALID_TOKEN'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'INVALID_USER'}, status=400)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'NEED_TO_SIGNIN'}, status=401)

    return wrapper

def get_current_user_id(request):
    try:
        if request.headers.get('AUTHORIZATION'):
            return User.objects.get(id=jwt.decode(request.headers['AUTHORIZATION'], SECRET_KEY, algorithms=ALGORITHM)['user_id']).id
        return 0
    
    except jwt.exceptions.DecodeError:
        return JsonResponse({'MESSAGE':'INVALID_TOKEN'}, status=400)

    except User.DoesNotExist:
        return JsonResponse({'MESSAGE':'INVALID_USER'}, status=400)
