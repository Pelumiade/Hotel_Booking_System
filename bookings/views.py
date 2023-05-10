from django.shortcuts import render, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages
from .models import Room, Booking, Complaint
from .forms import BookingForm, ComplaintForm, BookingStatusForm, RoomForm, ComplaintStatusForm
from django.views.generic import DetailView, FormView
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.template import RequestContext
from accounts.forms import CustomerCreationForm
from django.core.mail import send_mail
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


User = get_user_model()
# Create your views here.


def home_page(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'home_page.html', context)


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
def admin_room_list(request):
    rooms = Room.objects.all()

    if request.method == 'POST':
        if 'create' in request.POST:
            form = RoomForm(request.POST, request.FILES)
            if form.is_valid():
                room = form.save(commit=False)
                room.admin_user = request.user
                room.user_id = request.user.id
                room.save()
                messages.success(request, 'Room created successfully.')
            else:
                messages.error(request, 'Error creating room.')
        elif 'update' in request.POST:
            room_id = request.POST.get('room_id')
            room = Room.objects.get(pk=room_id)
            form = RoomForm(request.POST, request.FILES, instance=room)  # pass the room instance to the form
            if form.is_valid():
                form.save()
                messages.success(request, 'Room updated successfully.')
            else:
                messages.error(request, 'Error updating room.')
        elif 'delete' in request.POST:
            room_id = request.POST.get('room_id')
            room = Room.objects.get(pk=room_id)
            room.delete()
            messages.success(request, 'Room deleted successfully.')

        return redirect('bookings:admin_room_list')
    else:
        form = RoomForm()

    return render(request, 'admin_room_list.html', {'rooms': rooms, 'form': form})


def booking_create(request, id):
    room = get_object_or_404(Room, id=id)
    if request.method == 'POST':
        form = BookingForm(request.POST or None)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.save()
            messages.success(request, 'Your booking has been created!')
            #return redirect('booking_list')
            return redirect('bookings:home')
            #return redirect('customer:booking_detail', booking_id=booking.id)
    else:
        form = BookingForm()
    return render(request, 'book_room.html', {'room': room, 'form': form})

# @login_required
# def complaint_create(request, id):
#     complaint = get_object_or_404(Booking, id=id)
#     if request.method == 'POST':
#         form = ComplaintForm(request.POST or None)  # pass booking object as parameter
#         if form.is_valid():
#             complaint = form.save(commit=False)
#             complaint.complaint = complaint  # set the booking object
#             complaint.user = request.user
#             complaint.save()
#             messages.success(request, 'Your complaint has been submitted.')
#             return redirect('bookings:home')
#     else:
#         form = ComplaintForm  # pass booking object as parameter
#     return render(request, 'complaint_create.html', {'form': form})

@login_required
def complaint_create(request, id):
    booking = get_object_or_404(Booking, pk=id)
    if request.method == 'POST':
        form = ComplaintForm(request.POST, pk=booking)  # pass booking object as parameter
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.booking = booking  # set the booking object
            complaint.customer = request.user
            complaint.save()
            messages.success(request, 'Your complaint has been submitted.')
            return redirect('complaint_list')
    else:
        form = ComplaintForm(pk=id)  # pass booking object as parameter
    return render(request, 'complaint_create.html', {'form': form})

@login_required
def admin_booking_list(request):
    bookings = Booking.objects.all()
    if request.method == 'POST':
        form = BookingStatusForm(request.POST)
        booking_id=request.POST.get('booking_id')
        booking = Booking.objects.get(pk=booking_id)
        if 'accept' in request.POST:
            booking.status = 'accepted'
            booking.save()
            # send email notification to customer
            send_mail(
                'Booking Accepted',
                'Your booking has been accepted!',
                'fecoyifemi@gmail',  # sender's email
                [booking.customer_email],  # recipient's email
                fail_silently=False,
            )
        elif 'reject' in request.POST:
            booking.status = 'rejected'
            booking.save()
            # send email notification to customer
            send_mail(
                'Booking Rejected',
                'Sorry, your booking has been rejected.',
                'fecoyifemi@gmail.com',  # sender's email
                [booking.customer_email],  # recipient's email
                fail_silently=False,
            )
        return redirect('bookings:admin_booking_list')
    else:
        form = BookingStatusForm()

    context = {'bookings': bookings, 'form': form}
    return render(request, 'booking_list.html', context)



# @login_required
# def booking_accept(request, pk):
#     if not request.user.is_superuser:
#         return("you are not allowed in")
#     user=User.objects.filter(id=pk).first()
#     bookings = Booking.objects.filter(admin_user=user)
#     for booking in bookings:
#         if booking.status=='pending' or booking.status=='rejected':
#             booking.status ='accepted' 
#             booking.save()
#             break   

#     redirect_url = reverse('bookings:booking_list') 
#     return HttpResponseRedirect (redirect_url)


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
def booking_detail(request):
    bookings = Booking.objects.filter(user=request.user)
    print(bookings)
    return render(request, 'booking_detail.html', {'bookings': bookings})



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





class RoomDetailView(DetailView):
    model = Room
    template_name = 'room_detail.html'
    context_object_name = 'room'


    def get_success_url(self):
        return reverse('room_detail', kwargs={'pk': self.object.room.pk})
    


@login_required
def admin_home(request):
    current_bookings = Booking.objects.filter(status='current')
    past_bookings = Booking.objects.filter(status='past')
    complaints = Complaint.objects.all()
    return render(request, 'admin_home.html', {'current_bookings': current_bookings, 'past_bookings': past_bookings, 'complaints': complaints})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('bookings:home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import login
#from django.contrib.auth.forms import UserCreationForm
from .forms import CustomerSignUpForm




User = get_user_model()

def signup(request):
    if request.method == 'POST':
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            print(form.errors)

            user = form.save(commit=False)
            user.is_customer = True
            user.save()
            form.save_m2m()
            login(request, user)
            return redirect('bookings:login')
    else:
        form = CustomerSignUpForm()
    return render(request, 'signup.html', {'form': form})


from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import Complaint

class ComplaintListView(ListView):
    model = Complaint
    template_name = 'complaint_list.html'
    context_object_name = 'complaints'

from django.contrib import messages
class ComplaintCreateView(CreateView):
    model = Complaint
    form_class = ComplaintForm
    template_name = 'complaint_create.html'
    success_url = reverse_lazy('bookings:home')
    

    def form_valid(self, form):
        form.instance.user = self.request.user
        booking_id = self.request.GET.get('booking_id')
        form.instance.booking_id = booking_id
        response = super().form_valid(form)
        messages.success(self.request, 'Your complaint has been submitted successfully!')
        return response

from django.views.generic import DetailView
from .models import Complaint

class ComplaintDetailView(DetailView):
    model = Complaint
    template_name = 'complaint_detail.html'

class ComplaintStatusView(FormView):
    form_class = ComplaintStatusForm
    template_name = 'complaint_status.html'

    def form_valid(self, form):
        complaint = get_object_or_404(Complaint, pk=self.kwargs['pk'])
        complaint.status = form.cleaned_data['status']
        complaint.save()
        return redirect('complaint_detail', pk=complaint.pk)


@login_required
def complaint_detail(request):    
    complaint = Complaint.objects.filter(user=request.user)
    print(complaint)
    return render(request, 'complaint_detail.html', {'complaint': complaint})


@login_required
def admin_complaint_list(request):
    complaints = Complaint.objects.all()
    if request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')
        complaint = Complaint.objects.get(pk=complaint_id)
        if 'mark_as_solved' in request.POST:
            complaint.status = 'solved'
            complaint.admin_user = request.user
            complaint.save()
            messages.success(request, 'Complaint marked as solved!')
        elif 'mark_as_pending' in request.POST:
            complaint.status = 'pending'
            complaint.admin_user = request.user
            complaint.save()
            messages.success(request, 'Complaint marked as pending!')
        return redirect('bookings:admin_complaint_list')
    context = {'complaints': complaints}
    return render(request, 'complaint_list.html', context)

@login_required
def complaint_edit(request, complaint_id):
    complaint = get_object_or_404(Complaint, pk=complaint_id)

    # Check if the complaint belongs to the current user
    if request.user != complaint.user:
        return HttpResponseForbidden()

    # Check if the complaint is already solved
    if complaint.status == 'solved':
        return HttpResponseBadRequest("Cannot edit a solved complaint.")

    if request.method == 'POST':
        form = ComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            complaint = form.save()
            messages.success(request, 'Complaint updated successfully.')
            return redirect('bookings:complaint_detail')
    else:
        form = ComplaintForm(instance=complaint)

    return render(request, 'complaint_update.html', {'form': form, 'complaint': complaint})

from django.shortcuts import render
from django.utils import timezone
from .models import Booking

def booked_rooms_list(request):
    current_bookings = Booking.objects.filter(check_out__gte=timezone.now())
    past_bookings = Booking.objects.filter(check_out__lt=timezone.now())

    context = {
        'current_bookings': current_bookings,
        'past_bookings': past_bookings,
    }

    return render(request, 'booked_rooms_list.html', context)

# views.py
from django.shortcuts import render
from .models import Booking

def customer_info(request):
    bookings = Booking.objects.all()
    return render(request, 'customer_info.html', {'bookings': bookings})
