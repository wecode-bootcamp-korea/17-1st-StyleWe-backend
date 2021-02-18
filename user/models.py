from django.db                  import models
from django.db.models.deletion  import CASCADE

class User(models.Model):
    gender_id       = models.ForeignKey('Gender', on_delete=models.PROTECT, null=True)
    admin_level_id  = models.ForeignKey('AdminLevel', on_delete=models.PROTECT)
    user_name       = models.CharField(max_length=32)
    password        = models.CharField(max_length=45)
    nickname        = models.CharField(max_length=45)
    email           = models.CharField(max_length=2000)
    birth           = models.DateField(null=True)
    website         = models.URLField(null=True)
    about           = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'users'

class Gender(models.Model):
    name    = models.CharField(max_length=45)

    class Meta:
        db_table = 'genders'

class AdminLevel(models.Model):
    brand_id    = models.ForeignKey('product.Brand', on_delete=models.CASCADE, null=True)
    name        = models.CharField(max_length=45)

    class Meta:
        db_table = 'admin_levels'

