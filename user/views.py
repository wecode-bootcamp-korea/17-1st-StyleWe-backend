import json, bcrypt, jwt

from django.shortcuts   import render
from django.views       import View
from django.http        import JsonResponse, HttpResponse

from user.models        import User
from my_settings        import SECRET_KEY,ALGORITHM
from user.utils         import login_decorator


PASSWORD_MIN_LENGTH     = 6
USER_NAME_MIN_LENGTH    = 3
USER_NAME_MAX_LENGTH    = 32

class UserView(View):
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
                return JsonResponse({'message':'SHORT_ID'}, status=409)
            if len(user_name) > USER_NAME_MAX_LENGTH:
                return JsonResponse({'message':'LONG_ID'}, status=409)
            if len(password) < PASSWORD_MIN_LENGTH:
                return JsonResponse({'message':'SHORT_PASSWORD'}, status=409)
            
            user = User.objects.create(
                    user_name   = user_name,
                    password    = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode(),
                    nickname    = nickname,
                    email       = email
                )

            access_token   = jwt.encode({'user_id':user.id}, SECRET_KEY, algorithm=ALGORITHM)

            return JsonResponse({'message':'SUCCESS','access_token':access_token}, status=200)
        
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status=400)
    
    @login_decorator
    def patch(self, request):
        print(request)
        try:
            if not request.body:
                return JsonResponse({'message':'SUCCESS'}, status=200)

            data = json.loads(request.body)

            user    = request.user
            birth   = data.get('birth', user.birth)
            website = data.get('website', user.website)
            about   = data.get('about', user.about)

            user.birth      = birth
            user.website    = website
            user.about      = about
            user.save()
    
            return JsonResponse({'message':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status=400)
