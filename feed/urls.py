from django.urls    import path

from feed.views     import FeedView, FeedDetailView

urlpatterns = [
    path('', FeedView.as_view()), 
    path('/<int:feed_id>', FeedDetailView.as_view()),
]
