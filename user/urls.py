from django.urls    import path,include
from user.views     import UserUpdateView

urlpatterns = [
    path('/signup/final', UserUpdateView.as_view()),
]
