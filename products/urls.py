
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import ProductListView,ProductDetailView,ProductUpdateView,ProductDeleteView


router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'categories', views.CategoryViewSet)

app_name = 'products'

urlpatterns = [
    # Traditional Django Views for page rendering
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/',ProductDeleteView.as_view(), name='product_delete'),

    # DRF API Endpoints
    path('api/', include(router.urls)),
]