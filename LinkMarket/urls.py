from django.urls import path
from django.urls import path
from .views import landing_page, register, login_view, seller_account, product_edit, product_create, product_list, dash, category_create, category_list, product_delete, category_delete, category_detail, category_edit, logout_view, product_detail, buyer_account, cart, About, register_business
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('LinkMarket/', landing_page, name='landing_page'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('Market/', buyer_account, name='buyer_account'),
    path('seller dashboard/', seller_account, name='seller_account'),
    path('product_edit/<int:id>/edit/', product_edit, name='product_edit'),
    path('product_create/', product_create, name='product_create'),
    path('product/view/<int:id>/view/', product_detail, name="product_detail"),
    path('product/<int:id>/delete/', product_delete, name='product_delete'),
    path('products/', product_list, name='product_list'),
    path('dash/', dash, name="dash"),
    path('logout/', logout_view, name='logout'),
    
    # category
    path('category/',  category_create, name='category-create'),
    path('category List/', category_list, name="category_list"),
    path('categories/delete/<int:pk>/', category_delete, name='category_delete'),
    path('category/view/<int:id>/view/', category_detail, name="category_detail"),
    path('category/edit/<int:id>/view/', category_edit, name="category_edit"),
    path('cart/', cart, name='cart'),
    path('About/', About, name="about"),
    path('register_business/', register_business, name='register_business'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)