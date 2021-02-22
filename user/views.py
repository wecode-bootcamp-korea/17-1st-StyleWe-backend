import json, bcrypt, jwt

from django.shortcuts   import render
from django.views       import View
from django.http        import JsonResponse, HttpResponse

from user.models        import User
from my_settings        import SECRET_KEY,AL
from user.utils         import login_decorator


PASSWORD_MIN_LENGTH     = 6
USER_NAME_MIN_LENGTH    = 3
USER_NAME_MAX_LENGTH    = 32

class SignUpInitializeView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            user_name   = data['user_name']
            password    = data['password']
            nickname    = data['nickname']
            email       = data['email']

            if User.objects.filter(user_name=user_name).exists():
                return JsonResponse({'message':'USER_NAME_ALREADY_EXISTS'}, status=409)
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message':'EMAIL_ALREADY_EXISTS'}, status=409)

            if len(user_name) < USER_NAME_MIN_LENGTH:
                return JsonResponse({'message':'SHORT_ID'}, status=400)
            if len(user_name) > USER_NAME_MAX_LENGTH:
                return JsonResponse({'message':'LONG_ID'}, status=409)
            if len(password) < PASSWORD_MIN_LENGTH:
                return JsonResponse({'message':'SHORT_PASSWORD'}, status=409)
            
            User.objects.create(
                user_name   = user_name,
                password    = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode(),
                nickname    = nickname,
                email       = email
            )

            user    = User.objects.get(user_name=user_name)
            token   = jwt.encode({'user_id':user.id}, SECRET_KEY, algorithm=AL)

            return JsonResponse({'message':'SUCESS','token':token}, status=200)
        
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status=400)
