from django.urls    import path, include
from user.views     import UserView

urlpatterns = [
        path('/signup', UserView.as_view()),
]
