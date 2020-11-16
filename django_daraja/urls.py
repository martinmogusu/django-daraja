from django.conf.urls import url, include
from . import views

test_patterns = [
	url(r'^$', views.index, name='django_daraja_index'),
	url(r'^oauth/success', views.oauth_success, name='test_oauth_success'),
	url(r'^stk-push/success', views.stk_push_success, name='test_stk_push_success'),
	url(r'^business-payment/success', views.business_payment_success, name='test_business_payment_success'),
	url(r'^salary-payment/success', views.salary_payment_success, name='test_salary_payment_success'),
	url(r'^promotion-payment/success', views.promotion_payment_success, name='test_promotion_payment_success'),
]

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^tests/', include(test_patterns)),
]

