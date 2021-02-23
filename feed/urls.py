from django.urls    import path
from .views         import FeedEntireView

urlpatterns=[
    path('', FeedEntireView.as_view())
]
