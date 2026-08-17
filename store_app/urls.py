from .views import RegisterView, LoginAPIView
from rest_framework import routers
from django.urls import path,include


from .views import (UserProfileViewSet,CategoryListAPIView, CategoryDetailAPIView,SubCategoryListAPIView,SubCategoryDetailAPIView,
                    ProductListAPIView,ProductDetailAPIView,ReviewViewSet,CartViewSet,CartItemViewSet)
from .views import (UserProfileViewSet, CategoryListAPIView, LoginAPIView )

router = routers.DefaultRouter()

router.register(r'user', UserProfileViewSet)
router.register(r'review', ReviewViewSet)
router.register(r'cart', CartViewSet)
router.register(r'cartitem', CartItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('subcategory/', SubCategoryListAPIView.as_view(), name='subcategory_list'),
    path('subcategory/<int:pk>/', SubCategoryDetailAPIView.as_view(), name='subcategory_detail'),
    path('product/', ProductListAPIView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view(), name='product_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),

]