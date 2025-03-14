from django.urls import path
from . import views
from paypal.standard.ipn import views as paypal_views

urlpatterns = [
    path('', views.Home, name='home'),
    path('about/', views.About, name='about'),
    path('contact/', views.Contact, name='contact'),
    path('testimonial/', views.Testimonials, name='testimonial'),
    path('team/', views.Team, name='team'),
    path('courses/', views.Courses, name='courses'),
    path('<str:slug>/', views.Course_details, name='details'),
    path('404', views.PAGE_NOT_FOUND,name='404'),
    path('checkout/<int:course_id>/', views.Checkout, name='checkout'),
    path('paypal-ipn/', paypal_views.ipn, name='paypal-ipn'),
    path('payment-success/<int:product_id>/', views.PaymentSuccessful, name='payment-success'),
    path('payment-failed/<int:product_id>/', views.paymentFailed, name='payment-failed'),
]
