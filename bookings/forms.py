from django import forms
from .models import Booking, Complaint,Room

# class BookingForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = ['customer_name', 'customer_email', 'check_in_date', 'check_out_date']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['customer_name', 'customer_email', 'check_in_date', 'check_out_date', 'number_of_guests']

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get("check_in_date")
        check_out_date = cleaned_data.get("check_out_date")
        if check_in_date and check_out_date:
            if check_in_date >= check_out_date:
                raise forms.ValidationError(
                    "Check-in date should be before check-out date."
                )
        return cleaned_data



# class ComplaintForm(forms.ModelForm):
#     class Meta:
#         model = Complaint
#         fields = ['title', 'description']

#     def clean_title(self):
#         title = self.cleaned_data['title']
#         if len(title) < 5:
#             raise forms.ValidationError("Title should be at least 5 characters long.")
#         return title


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['subject', 'message']

    def clean_title(self):
        subject = self.cleaned_data['subject']
        if len(subject) < 5:
            raise forms.ValidationError("Title should be at least 5 characters long.")
        return subject
    

#ADMIN
# from django import forms
# from .models import Room, Booking, Complaint

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'price']

# class BookingForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = ['check_in', 'check_out', 'guest_name']

# class ComplaintForm(forms.ModelForm):
#     class Meta:
#         model = Complaint
#         fields = ['resolution_description', 'resolution_date']
# from django import forms
# from .models import Complaint

# class ComplaintForm(forms.ModelForm):
#     class Meta:
#         model = Complaint
#         fields = ['subject', 'message']
#         widgets = {
#             'message': forms.Textarea(attrs={'rows': 4}),
#         }
