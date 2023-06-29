"""
URL configuration for DNICK5 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ShopApp import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

from ShopApp.views import out_of_stock

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ProductListView.as_view(), name='product_list'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('create-product/', views.ProductCreateView.as_view(), name='create_product'),
    path('cart/', views.CartView.as_view(), name='cart'),
    #path('payment/', views.PaymentView.as_view(), name='payment'),
    path('payment/', views.payment, name='payment'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('product-details/<int:product_id>/', views.product_details, name='product_details'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('out-of-stock/', out_of_stock, name='out_of_stock'),
    path('product/delete/<int:product_id>/', views.ProductDeleteView.as_view(), name='delete_product'),
    path('payment/success/', views.payment_success, name='payment_success'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
