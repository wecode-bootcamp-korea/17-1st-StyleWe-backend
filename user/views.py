import json, bcrypt, jwt

from django.shortcuts   import render
from django.views       import View
from django.http        import JsonResponse, HttpResponse

from user.models        import User
from my_settings        import SECRET_KEY

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            user_name   = data['user_name']
            password    = data['password']

            user = User.objects.get(user_name=user_name)
            
            password_validation = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))

            if password_validation:
                token = jwt.encode({'user_name':user.name}, SECRET_KEY, algorithm='HS256')
                token = token.decode('utf-8')

                return JsonResponse({'token':token}, status=200)
        
            return JsonResponse({'message':'SIGNIN_FAIL'}, status=401)

        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status=400)
