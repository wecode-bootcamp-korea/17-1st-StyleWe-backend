from django.urls    import path, include
from user.views     import SignUpInitializeView

urlpatterns = [
        path('signup/initial', SignUpInitializeView.as_view())        
]
