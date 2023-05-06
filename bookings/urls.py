from django.urls import path
from .import views
from .import admin_views

app_name = 'bookings'
# urlpatterns = [
#     path('rooms/', views.room_list, name='room_list'),
#     path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
#     path('rooms/<int:room_id>/book/', views.book_room, name='book_room'),
#     path('bookings/', views.booking_list, name='booking_list'),
#     path('bookings/<int:booking_id>/', views.booking_detail, name='booking_detail'),
#     path('bookings/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
#     path('complaints/', views.complaint_list, name='complaint_list'),
#     path('complaints/<int:complaint_id>/', views.complaint_detail, name='complaint_detail'),
#     path('complaints/file/', views.file_complaint, name='file_complaint'),
#     path('complaints/<int:complaint_id>/update/', views.update_complaint, name='update_complaint'),

#     # Admin views
#     #path('admin/rooms/', admin_views.room_list, name='room_list'),
#     path('admin/rooms/add/', admin_views.room_create, name='room_create'),
#     path('admin/rooms/<int:pk>/', admin_views.room_update, name='room_update'),
#     path('admin/rooms/<int:pk>/delete/',admin_views.room_delete, name='room_delete'),
#     path('admin/booking/list/', admin_views.booking_list, name='booking_list'),

    
#     path('admin/booking/<int:pk>/detail/', admin_views.booking_detail, name='booking_detail'),
#     path('admin/complaint/list/', admin_views.complaint_list, name='complaint_list'),
#     path('admin/complaint/<int:pk>/detail/', admin_views.complaint_detail, name='complaint_detail'),
#     path('admin/complaint/<int:pk>/resolve/', admin_views.complaint_resolve, name='complaint_resolve'),

         
# ]

urlpatterns = [
    # Admin URLs
    path('rooms/', views.room_list, name='room_list'),
    path('booking/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('rooms/create/', admin_views.room_create, name='room_create'),
    path('rooms/<int:pk>/update/', admin_views.room_update, name='room_update'),
    path('rooms/<int:pk>/delete/', admin_views.room_delete, name='room_delete'),
    path('bookings/', admin_views.admin_booking_list, name='admin_booking_list'),
    path('bookings/<int:pk>/accept/', admin_views.booking_accept, name='booking_accept'),
    path('bookings/<int:pk>/reject/', admin_views.booking_reject, name='booking_reject'),
    path('bookings/<int:pk>/release/', admin_views.booking_release, name='booking_release'),
    path('bookings/customer/<int:pk>/', admin_views.customer_booking_list, name= 'customer_booking_list'),
    path('complaints/', admin_views.complaint_list, name='complaint__list'),
    path('complaints/<int:pk>/solve/', admin_views.complaint_solve, name='complaint_solve'),

    # Customer URLs
    path('bookings/create/<int:pk>/', views.booking_create, name='booking_create'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:pk>/update/', views.booking_update, name='booking_update'),
    path('bookings/<int:pk>/cancel/', views.booking_cancel, name='booking_cancel'),
    path('complaints/create/', views.complaint_create, name='complaint_create'),
    path('complaints/', views.complaint_list, name='complaint_list'),
    path('complaints/<int:pk>/update/', views.complaint_update, name='complaint_update'),
    path('', views.home, name='home'),
]