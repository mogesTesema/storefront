from django.urls import path,include
from rest_framework.routers import SimpleRouter,DefaultRouter
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('products',views.ProductViewSet,basename='products')
router.register('collections',views.CollectionViewSet,basename='collections')
router.register('carts',views.CartViewSet,basename='carts')
router.register('customers',views.CustomerViewSet,basename='customer')
router.register('orders',views.OrderViewSet,basename='orders')


products_router = routers.NestedDefaultRouter(router,'products',lookup='product')
products_router.register('reviews',views.ReviewViewSet,basename='product-reviews')
products_router.register('images',views.ProductImageViewSet,basename='product-images')


carts_router = routers.NestedDefaultRouter(router,'carts',lookup='cart')
carts_router.register('items',views.CartItemViewSet,basename='cart-items')



urlpatterns = [
    path('',include(router.urls)),
    path('',include(products_router.urls)),
    path('',include(carts_router.urls))
]

# urlpatterns = [
#     path('',include(router.urls))
#     # path('products/',views.ProductList.as_view()),
#     # path('products/<int:pk>/',views.ProductDetail.as_view()),
#     # path('collections/',views.CollectionList.as_view()),
#     # path('collections/<int:pk>/',views.CollectionDetail.as_view(),name='collection-detail')
# ]