from django.db                  import models

class Menu(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'menus'

class Category(models.Model):
    menu    = models.ForeignKey('Menu', on_delete=models.SET_NULL, null=True)
    name    = models.CharField(max_length=45)
 
    class Meta:
        db_table = 'categories'

class Subcategory(models.Model):
    category    = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    name        = models.CharField(max_length=45)

    class Meta:
        db_table = 'subcategories'

class Brand(models.Model):
    name                = models.CharField(max_length=45)
    delivery_fee_cap    = models.DecimalField(max_digits=15, decimal_places=3)

    class Meta:
        db_table = 'brands'

class Product(models.Model):
    subcategory     = models.ForeignKey('Subcategory', on_delete=models.SET_NULL, null=True)
    brand           = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True)
    name            = models.CharField(max_length=100)
    price           = models.DecimalField(max_digits=15, decimal_places=3)
    discount_rate   = models.DecimalField(max_digits=2, decimal_places=2, default=0)
    is_for_sale     = models.BooleanField(default=1)
    
    class Meta:
        db_table = 'products'

class ProductImageUrl(models.Model):
    product     = models.ForeignKey('Product', on_delete=models.CASCADE)
    image_url   = models.URLField()
    is_main     = models.BooleanField(default=0)

    class Meta:
        db_table = 'product_image_urls'

class ProductOption(models.Model):
    product             = models.ForeignKey('Product', on_delete=models.PROTECT)
    color               = models.CharField(max_length=50)
    size                = models.CharField(max_length=50)
    additional_price    = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    is_for_sale         = models.BooleanField(default=1)

    class Meta:
        db_table = 'product_options'

class ProductQuestion(models.Model):
    user        = models.ForeignKey('user.User', on_delete=models.CASCADE)
    product     = models.ForeignKey('Product', on_delete=models.CASCADE)
    content     = models.CharField(max_length=100)
    created_at  = models.DateField(auto_now_add=True)
    updated_at  = models.DateField(auto_now=True)

    class Meta:
        db_table = 'product_questions'

class ProductAnswer(models.Model):
    user                = models.ForeignKey('user.User', on_delete=models.CASCADE)
    product_question    = models.ForeignKey('ProductQuestion', on_delete=models.CASCADE)
    content             = models.CharField(max_length=100)
    created_at          = models.DateField(auto_now_add=True)
    updated_at          = models.DateField(auto_now=True)

    class Meta:
        db_table = 'product_answers'
