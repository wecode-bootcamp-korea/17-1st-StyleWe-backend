from django.db      import models

class Feed(models.Model):
    product         = models.ForeignKey('product.Product', on_delete=models.CASCADE, null=True)
    user            = models.ForeignKey('user.User', on_delete=models.CASCADE)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    description     = models.CharField(max_length=2000)
    like_number     = models.IntegerField(default=0)
    tag_item_number = models.IntegerField(null=True)

    class Meta:
        db_table = 'feeds'

class Comment(models.Model):
    user        = models.ForeignKey('user.User', on_delete=models.CASCADE)
    feed        = models.ForeignKey('Feed', on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    content     = models.CharField(max_length=100)

    class Meta:
        db_table = 'comments'

class ImageUrl(models.Model):
    feed        = models.ForeignKey('Feed', on_delete=models.CASCADE)
    image_url   = models.URLField()

    class Meta:
        db_table = 'image_urls'
