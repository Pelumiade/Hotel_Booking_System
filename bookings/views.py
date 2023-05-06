from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import Room, Booking, Complaint
from .forms import BookingForm, ComplaintForm


# Create your views here.

@login_required
def home(request):
    upcoming_bookings = Booking.objects.filter(user=request.user)
    context = {
        'upcoming_bookings': upcoming_bookings,
    }
  
  
    return render(request, 'base.html', context)
@login_required
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms})


@login_required
def booking_create(request, pk):
    room = get_object_or_404(Room, pk=pk)
    form = BookingForm(request.POST or None)
    if form.is_valid():
        booking = form.save(commit=False)
        booking.room = room
        booking.save()
        return redirect('home')
    return render(request, 'bookings/booking_create.html', {'form': form, 'room': room})


@login_required
def booking_list(request):
    #bookings = Booking.objects.filter(customer=request.user)
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking_list.html', {'bookings': bookings})

@login_required
def booking_update(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.save()
            messages.success(request, 'Booking updated successfully.')
            return redirect('booking_list')
    else:
        form = BookingForm(instance=booking)
    
    
    return render(request, 'booking_update.html', {'form': form, 'booking': booking})
@login_required

def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, customer=request.user)
    return render(request, 'booking_detail.html', {'booking': booking})

@login_required
def booking_cancel(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.delete()
    messages.success(request, 'Booking cancelled successfully.')
    return redirect('booking_list')

@login_required
def complaint_create(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.customer = request.user
            complaint.save()
            messages.success(request, 'Your complaint has been submitted.')
            return redirect('complaint_list')
            #return redirect('customer:complaint_detail', complaint_id=complaint.id)
    else:
        form = ComplaintForm()
    return render(request, 'complaint_create.html', {'form': form})

@login_required
def complaint_list(request, complaint_id):
    complaint = get_object_or_404(Complaint, pk=complaint_id, customer=request.user)
    return render(request, 'complaint_list.html', {'complaint': complaint})




@login_required
def complaint_update(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)

    # Only allow updates if status is pending
    if complaint.status != 'pending':
        messages.error(request, 'Complaint cannot be updated as it is no longer pending.')
        return redirect('complaint_detail', pk=complaint.pk)

    if request.method == 'POST':
        form = ComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.customer = request.user
            complaint.save()
            messages.success(request, 'Complaint updated successfully.')
            return redirect('complaint_list')
    else:
        form = ComplaintForm(instance=complaint)

    return render(request, 'complaint_update.html', {'form': form, 'complaint': complaint})
