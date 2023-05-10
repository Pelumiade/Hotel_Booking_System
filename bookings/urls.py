from django.urls import path
from .import views
from .import admin_views

app_name = 'bookings'
         
# ]
urlpatterns = [
    # Admin URLs
    path('rooms/', views.room_list, name='room_list'),
    #path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('rooms/create/', admin_views.room_create, name='room_create'),
    path('rooms/<int:pk>/update/', admin_views.room_update, name='room_update'),
    path('rooms/<int:pk>/delete/', admin_views.room_delete, name='room_delete'),
    path('bookings/', admin_views.admin_booking_list, name='admin_booking_list'),
    #path('bookings/<int:pk>/accept/', views.booking_accept, name='booking_accept'),
    path('bookings/<int:pk>/reject/', admin_views.booking_reject, name='booking_reject'),
    path('bookings/<int:pk>/release/', admin_views.booking_release, name='booking_release'),
    path('bookings/customer/<int:pk>/', admin_views.customer_booking_list, name= 'customer_booking_list'),
    #path('complaints/', admin_views.complaint_list, name='complaint__list'),
    path('complaints/<int:pk>/solve/', admin_views.complaint_solve, name='complaint_solve'),

    # Customer URLs
   # path('complaints/<int:id>/create/', views.complaint_create, name='complaint_create'),
    path('bookings/<int:id>/create/', views.booking_create, name='booking_create'),
   # path('bookings/', views.BookingListView.as_view(), name='booking_list'),
    path('admin_bookings/', views.admin_booking_list, name='admin_booking_list'),
    path('bookings/<int:pk>/update/', views.booking_update, name='booking_update'),
    #path('bookings/<int:pk>/cancel/', views.booking_cancel, name='booking_cancel'),
    path('rooms/<int:pk>/', views.RoomDetailView.as_view(), name='room_detail'),
    path('booking/', views.booking_detail, name='booking_detail'),
    #path('complaints/', views.complaint_list, name='complaint_list'),
    path('complaints/<int:pk>/update/', views.complaint_update, name='complaint_update'),
    path('admin/', views.admin_home, name='admin_home'),
    path('admin/', views.admin_home, name='admin_home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('admin_room_list/', views.admin_room_list, name='admin_room_list'),
    #path('complaints/', views.ComplaintListView.as_view(), name='complaint_list'),
    path('complaints/', views.complaint_detail, name='complaint_detail'),
    path('admin_complaints/', views.admin_complaint_list, name='admin_complaint_list'),
    path('complaint_edit/<int:complaint_id>/', views.complaint_edit, name='complaint_edit'),
    path('booked_room_list/', views.booked_rooms_list, name='booked_room_list'),
    path('customer_info/', views.customer_info, name='customer_info'),
    path('complaints/create/', views.ComplaintCreateView.as_view(), name='complaint_create'),
    path('home_page/', views.home_page, name='home_page'),
]
