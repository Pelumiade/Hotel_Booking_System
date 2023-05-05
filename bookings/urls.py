from django.urls import path
from .import views
from .import admin_views

app_name = 'bookings'
urlpatterns = [
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    path('rooms/<int:room_id>/book/', views.book_room, name='book_room'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('bookings/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('complaints/', views.complaint_list, name='complaint_list'),
    path('complaints/<int:complaint_id>/', views.complaint_detail, name='complaint_detail'),
    path('complaints/file/', views.file_complaint, name='file_complaint'),
    path('complaints/<int:complaint_id>/update/', views.update_complaint, name='update_complaint'),

    # Admin views
    #path('admin/rooms/', admin_views.room_list, name='room_list'),
    path('admin/rooms/add/', admin_views.room_create, name='room_create'),
    path('admin/rooms/<int:pk>/', admin_views.room_update, name='room_update'),
    path('admin/rooms/<int:pk>/delete/',admin_views.room_delete, name='room_delete'),
    path('admin/booking/list/', admin_views.booking_list, name='booking_list'),

    
    path('admin/booking/<int:pk>/detail/', admin_views.booking_detail, name='booking_detail'),
    path('admin/complaint/list/', admin_views.complaint_list, name='complaint_list'),
    path('admin/complaint/<int:pk>/detail/', admin_views.complaint_detail, name='complaint_detail'),
    path('admin/complaint/<int:pk>/resolve/', admin_views.complaint_resolve, name='complaint_resolve'),

         
]

