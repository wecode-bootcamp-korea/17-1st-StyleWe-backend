from django.urls    import path,include
from user.views     import SignUpFinalizeView

urlpatters = [
    path('signup/final', SignUpFinalizeView.as_view()),
]
