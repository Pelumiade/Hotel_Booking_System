# yourapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('dashboard/', views.dashboard_view, name='dashboard'),
    # path('bookings/', views.bookings_view, name='bookings'),
    #path('bookings/<int:booking_id>/', views.booking_details_view, name)
]