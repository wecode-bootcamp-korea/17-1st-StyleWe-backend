from django.urls    import path

from feed.views     import FeedDetailView

urlpatterns = [
        path('/<int:feed_id>', FeedDetailView.as_view()),
]
