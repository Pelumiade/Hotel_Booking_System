from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import Room, Booking, Complaint
from .forms import BookingForm, ComplaintForm


# Create your views here.

@login_required
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'customer/room_list.html', {'rooms': rooms})


@login_required
def room_detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'customer/room_detail.html', {'room': room})


@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.room = room
            booking.save()
            messages.success(request, 'Your booking has been confirmed!')
            return redirect('customer:booking_detail', booking_id=booking.id)
    else:
        form = BookingForm()
    return render(request, 'customer/book_room.html', {'room': room, 'form': form})


@login_required
def booking_list(request):
    bookings = Booking.objects.filter(customer=request.user)
    return render(request, 'customer/booking_list.html', {'bookings': bookings})


@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, customer=request.user)
    return render(request, 'customer/booking_detail.html', {'booking': booking})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, customer=request.user)
    if booking.status == Booking.PENDING:
        booking.delete()
        messages.success(request, 'Your booking has been canceled.')
    else:
        raise PermissionDenied
    return redirect('customer:booking_list')


@login_required
def complaint_list(request):
    complaints = Complaint.objects.filter(customer=request.user)
    return render(request, 'customer/view_complaints.html', {'complaints': complaints})


@login_required
def complaint_detail(request, complaint_id):
    complaint = get_object_or_404(Complaint, pk=complaint_id, customer=request.user)
    return render(request, 'customer/complaint_detail.html', {'complaint': complaint})


@login_required
def file_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.customer = request.user
            complaint.save()
            messages.success(request, 'Your complaint has been submitted.')
            return redirect('customer:complaint_detail', complaint_id=complaint.id)
    else:
        form = ComplaintForm()
    return render(request, 'customer/file_complaint.html', {'form': form})


@login_required
def update_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, pk=complaint_id, customer=request.user)
    if complaint.status != Complaint.PENDING:
        raise PermissionDenied
    if request.method == 'POST':
        form = ComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your complaint has been updated.')
            return redirect('customer:complaint_detail', complaint_id=complaint.id)
    else:
        form = ComplaintForm()
        return render(request, 'customer/file_complaint.html', {'form': form})

