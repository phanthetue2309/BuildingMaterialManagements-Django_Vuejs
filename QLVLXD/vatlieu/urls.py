from django.urls import path
from .views import views, views_api
from .views.views import *
from .views.views_api import *

# mô hình di chuyển của web blog -> templates -> blog -> template.html
urlpatterns = [
    path('', views.home, name='vatlieu-home'),

    # search
    path('search/', views.search, name='search'),

    # views.index là hàm với từ ở sau name ="" cho dễ nhận dạng
    path('list/input_bill', InputBillListView.as_view(), name='list-input-bill'),
    path('staff/input_bill/<str:username>', UserInputBillListView.as_view(), name='staff-input-bill'),
    path('input_bill/<int:pk>', views.all_detail_input_bill, name='input-bill-detail'),
    path('input_bill/<int:pk>/update/', InputBillUpdateView.as_view(), name='input-bill-update'),
    path('input_bill/<int:pk>/delete/', InputBillDeleteView.as_view(), name='input-bill-delete'),
    path('input_bill/new/', InputBillCreateView.as_view(), name='input-bill-create'),

    # show the detail input bill
    path('detail_input_bill/<int:pk>/', views.create_detail_inputbill, name='input-bill-detail-create'),
    path('update_detail_input_bill/<int:pk>/', DetailInputUpdateView.as_view(), name='update-detail-input-bill'),
    path('delete_detail_input_bill/<int:pk>/', DetailInputDeleteView.as_view(), name='delete-detail-input-bill'),

    # output bill
    path('list/output_bill', OutputBillListView.as_view(), name='list-output-bill'),
    path('output_bill/new/', OutputBillCreateView.as_view(), name='output-bill-create'),
    path('output_bill/<int:pk>', views.all_detail_output_bill, name='output-bill-detail'),
    path('output_bill/<int:pk>/update/', OutputBillUpdateView.as_view(), name='output-bill-update'),
    path('output_bill/<int:pk>/delete/', OutputBillDeleteView.as_view(), name='output-bill-delete'),
    path('staff/output_bill/<str:username>', UserOutputBillListView.as_view(), name='staff-output-bill'),
    # show the detail output bill
    path('detail_output_bill/<int:pk>/', views.create_detail_outputbill, name='output-bill-detail-create'),
    path('update_detail_output_bill/<int:pk>/', DetailOutputUpdateView.as_view(), name='update-detail-output-bill'),
    path('delete_detail_output_bill/<int:pk>/', DetailOutputDeleteView.as_view(), name='delete-detail-output-bill'),

    # show about
    path('about', views.about, name='vatlieu-about'),
    # category
    path('list/', views.list_all, name='list-all'),
    # provider
    path('list/provider', ProviderListView.as_view(), name='list-provider'),
    path('provider/new', ProviderCreateView.as_view(), name="provider-create"),
    path('provider/<int:pk>/update/', ProviderUpdateView.as_view(), name='provider-update'),
    path('provider/<int:pk>/delete/', ProviderDeleteView.as_view(), name='provider-delete'),
    path('provider/<int:pk>', ProviderDetailView.as_view(), name='provider-detail'),
    # product
    path('list/product', ProductListView.as_view(), name='list-product'),
    path('product/new', ProductCreateView.as_view(), name="product-create"),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product-detail'),
    path('product/<str:type_product>', views.List_typeProduct, name='product-list-type'),

    # customer
    path('list/customer', CustomerListView.as_view(), name='list-customer'),
    path('customer/new', CustomerCreateView.as_view(), name="customer-create"),
    path('customer/<int:pk>/update/', CustomerUpdateView.as_view(), name='customer-update'),
    path('customer/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer-delete'),
    path('customer/<int:pk>', CustomerDetailView.as_view(), name='customer-detail'),
    path('customer/shopping', views.customer_shopping, name="customer-shopping"),
    path('customer/buy_products', views.buy_products, name="customer-buy-products"),
    path('customer/buying/<str:username>', UserShopping_Buying.as_view(), name="customer-buying"),
    path('customer/buying/<str:username>/<int:pk>', views.CustomerReceiveBuying, name="customer-change-flag"),
    path('customer/received/<str:username>', UserShopping_Received.as_view(), name="customer-received"),
    # warehouse
    path('warehouse/', WarehouseListView.as_view(), name='warehouse'),

    # api riêng cho từng cái 
    path('api/customer/', views_api.CustomerListAPIView.as_view(), name="customers-api"), 
    path('api/customer/<int:id>', views_api.CustomerDetailAPIView.as_view(), name="customer-api"),

]
