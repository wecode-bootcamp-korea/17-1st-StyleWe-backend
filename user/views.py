import json, bcrypt, jwt

from django.shortcuts       import render
from django.views           import View
from django.http            import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from user.models        import User
from my_settings        import SECRET_KEY, AL

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            user_name   = data['user_name']
            password    = data['password']
            
            try:
                user = User.objects.get(user_name=user_name)
            except ObjectDoesNotExist:
                return JsonResponse({'message':'INVALID_USER'}, status=401)

            password_validation = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))

            if password_validation:
                acces_token = jwt.encode({'user_id':user.id}, SECRET_KEY, algorithm=AL)

                return JsonResponse({'message':'SUCESS', "token":acces_token}, status=200)
            return JsonResponse({'message':'SIGNIN_FAIL'}, status=401)
        
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status=400)
