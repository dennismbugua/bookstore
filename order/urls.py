from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
	path('', views.order_list, name="order_list"),
	path('<int:id>', views.order_details, name="order_details"),
	path('shipping/', views.order_create, name="order_create"),
	path('pdf/<int:id>',views.pdf.as_view(), name="pdf"),
	path('paypal/payment/<int:order_id>/', views.paypal_payment_process, name="paypal_payment"),
	path('paypal/debug/<int:order_id>/', views.paypal_debug, name="paypal_debug"),
	path('paypal/success/<int:order_id>/', views.paypal_success, name="paypal_success"),
	path('paypal/cancel/<int:order_id>/', views.paypal_cancel, name="paypal_cancel"),
	path('paypal/create/', views.create_paypal_payment, name="create_paypal_payment"),
	path('check-payment-status/<int:order_id>/', views.check_payment_status, name="check_payment_status"),
]
