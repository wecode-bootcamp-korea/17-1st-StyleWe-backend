from django.urls    import path, include
from product.views  import ProductView

urlpatterns = [
        path('/detail/<int:product_id>', ProductView.as_view())
    ]
