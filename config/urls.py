from django.urls import path, include

urlpatterns = [
    path('feed', include('feed.urls')),
    path('user', include('user.urls')),
]
