"""ecommerce2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from carts.views import (
    CartView,
    ItemCountView,
    CheckoutView,
    CheckoutFinalView,
    CartAPIView,
)
from orders.views import (
    AddressSelectFormView,
    UserAddressCreateView,
    OrderList,
    OrderDetail,
    UserCheckoutAPI,
)
from products.views import(
    APIHomeView,
    CategoryListAPIView,
    CategoryRetrieveAPIView,
    ProductListAPIView,
    ProductRetrieveAPIView,
)

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('newsletter.urls', namespace='newsletter')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^products/', include('products.urls', namespace='products')),
    url(r'^categories/', include(
        'products.urls_categories', namespace='categories')),
    url(r'^orders/$', OrderList.as_view(), name='orders'),
    url(r'^orders/(?P<pk>[0-9]+)/$',
        OrderDetail.as_view(), name='order_detail'),
    url(r'^cart/$', CartView.as_view(), name='cart'),
    url(r'^cart/count/$', ItemCountView.as_view(), name='item_count'),
    url(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
    url(r'^checkout/address/$',
        AddressSelectFormView.as_view(), name='order_address'),
    url(r'^checkout/address/add/$',
        UserAddressCreateView.as_view(), name='user_address_create'),
    url(r'^checkout/final/$',
        CheckoutFinalView.as_view(), name='checkout_final'),

]


# API Patterns
urlpatterns += [
    url(r'^api/$', APIHomeView.as_view(), name='home_api'),
    url(r'^api/cart/$', CartAPIView.as_view(), name='cart_api'),
    url(r'^api/auth/token/$', obtain_jwt_token),
    url(r'^api/auth/token/refresh/$', refresh_jwt_token),
    url(r'^api/user/checkout/$',
        UserCheckoutAPI.as_view(), name='user_checkout_api'),
    url(r'^api/categories/$',
        CategoryListAPIView.as_view(), name='categories_api'),
    url(r'^api/category/(?P<pk>[0-9]+)/$',
        CategoryRetrieveAPIView.as_view(), name='category_detail_api'),

    url(r'^api/products/$',
        ProductListAPIView.as_view(), name='products_api'),
    url(r'^api/product/(?P<pk>[0-9]+)/$',
        ProductRetrieveAPIView.as_view(), name='product_detail_api'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns += static(
#         settings.STATIC_URL,
#         document_root=settings.STATIC_ROOT
#     )
