from django.db                  import models

class User(models.Model):
    gender          = models.ForeignKey('Gender', on_delete=models.PROTECT, null=True)
    admin_level     = models.ForeignKey('AdminLevel', on_delete=models.PROTECT, default=1)
    user_name       = models.CharField(max_length=32, unique=True)
    password        = models.CharField(max_length=2000)
    nickname        = models.CharField(max_length=45)
    email           = models.CharField(max_length=2000)
    birth           = models.DateField(null=True, blank=True)
    website         = models.URLField(null=True)
    about           = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'users'

class Gender(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'genders'

class AdminLevel(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'admin_levels'

