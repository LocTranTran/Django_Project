from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    
    path('create-customer/', views.create_customer, name='create_customer'),    path('user-detail/', views.user_detail, name='user_detail'),
    path('user_profile/', views.user_profile, name='user_profile'),    
    
    path('product/', views.product, name='product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/<int:product_id>/reviews/', views.product_reviews, name='product_reviews'),
    path('products/<int:product_id>/review/create/', views.create_review, name='create_review'),
    
    path('search/', views.search_products, name='search_products'),
    path('search/results/', views.search_products, name='search_results'),
    
    
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    # path('payment/', views.payment, name='payment'),
    path('cart/', views.cart, name='cart_detail'),
    path('cart/', views.cart, name='delete_cart'),
    path('oder/', views.oder, name='oder'),
    path('check_item/', views.check_item, name='check_item'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),

]
