from django.urls    import path, include
from user.views     import SignInView, UserView

urlpatterns = [
    path('/signin', SignInView.as_view()),
    path('/signup', UserView.as_view()),
]
