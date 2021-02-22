from django.urls    import path,include
from user.views     import SignUpFinalizeView

urlpatterns = [
    path('signup/final', SignUpFinalizeView.as_view()),
]
