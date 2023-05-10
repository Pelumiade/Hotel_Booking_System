from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, Booking, Complaint
from .forms import RoomForm, BookingForm, ComplaintForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User

@login_required
def room_create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room created successfully.')
            return redirect('room_list')
    else:
        form = RoomForm()
    return render(request, 'room_create.html', {'form': form})

@login_required
def room_update(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room updated successfully.')
            return redirect('room_list')
    else:
        form = RoomForm(instance=room)
    return render(request, 'room_update.html', {'form': form})

@login_required
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Room deleted successfully.')
        return redirect('room_list')
    #return render(request, 'room_delete.html', {'room': room})

@login_required
def admin_booking_list(request):
    current_bookings = Booking.objects.filter(status='current')
    past_bookings = Booking.objects.filter(status='past')
    return render(request, 'admin_booking_list.html', {'current_bookings': current_bookings, 'past_bookings': past_bookings})

# @login_required
# def booking_accept(request, pk):
#     booking = get_object_or_404(Booking, pk=pk)
#     booking.status = 'accepted'
#     booking.save()
#     send_mail(
#         'Your booking has been accepted',
#         'Dear {0}, your booking for room {1} has been accepted.'.format(booking.customer.username, booking.room.room_number),
#         'admin@example.com',
#         [booking.customer.email],
#         fail_silently=False,
#     )
    messages.success(request, 'Booking accepted and email sent.')
    return redirect('admin_booking_list')

@login_required
def booking_reject(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.status = 'rejected'
    booking.save()
    send_mail(
        'Your booking has been rejected',
        'Dear {0}, your booking for room {1} has been rejected.'.format(booking.customer.username, booking.room.room_number),
        'fecoyifemi@gmail.com',
        [booking.customer.email],
        fail_silently=False,
    )
    messages.success(request, 'Booking rejected and email sent.')
    return redirect('admin_booking_list')


@login_required
def booking_release(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.status = 'available'
    booking.save()
    messages.success(request, 'Room released successfully.')
    return redirect('admin_booking_list')

@login_required
def customer_booking_list(request, username):
    customer = get_object_or_404(User, username=username)
    bookings = Booking.objects.filter(customer=customer)
    return render(request, 'customer_booking_list.html', {'bookings': bookings})

@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'booking_detail.html', {'booking': booking})

@login_required
def complaint_list(request):
    complaints = Complaint.objects.all()
    return render(request, 'complaint_list.html', {'complaints': complaints})

@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    return render(request, 'complaint_detail.html', {'complaint': complaint})


@login_required
def complaint_solve(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        complaint.status = request.POST['status']
        complaint.save()
        messages.success(request, 'Complaint status updated successfully.')
        return redirect('complaint_list')
    return render(request, 'complaint_solve.html', {'complaint': complaint})
