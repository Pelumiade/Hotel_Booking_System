from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, Booking, Complaint
from .forms import RoomForm, BookingForm, ComplaintForm

def room_create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm()
    return render(request, 'admin/room_create.html', {'form': form})

def room_update(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm(instance=room)
    return render(request, 'admin/room_update.html', {'form': form})

def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('room_list')
    return render(request, 'admin/room_delete.html', {'room': room})

def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'admin/booking_list.html', {'bookings': bookings})

def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'admin/booking_detail.html', {'booking': booking})

def complaint_list(request):
    complaints = Complaint.objects.all()
    return render(request, 'admin/complaint_list.html', {'complaints': complaints})

def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    return render(request, 'admin/complaint_detail.html', {'complaint': complaint})

def complaint_resolve(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        form = ComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            return redirect('complaint_list')
    else:
        form = ComplaintForm(instance=complaint)
    return render(request, 'admin/complaint_resolve.html', {'form': form})
