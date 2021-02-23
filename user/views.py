import json, bcrypt, jwt

from django.shortcuts   import render
from django.views       import View
from django.http        import JsonResponse, HttpResponse

from user.models        import User
from my_settings        import SECRET_KEY
from user.utils         import login_decorator

class UserUpdateView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body or 'null')
            
            if data is None:
                return JsonResponse({'message':'SKIP'}, status=200)

            birth   = data.get('birth', None)
            country = data.get('country', None)
            website = data.get('website', None)
            about   = data.get('about', None)

            user_id         = request.user.id
            user            = User.objects.get(id=user_id)
            user.birth      = birth
            user.country    = country
            user.website    = website
            user.about      = about
            user.save()

            return JsonResponse({'message':'SUCESS'}, status=200)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status=400)
