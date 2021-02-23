from django.urls    import path, include
from user.views     import UserView

urlpatterns = [
        path('/signup/initial', UserView.as_view()),
        path('/signup/fianl', UserView.as_view()),
]
