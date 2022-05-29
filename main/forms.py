from django import forms
from .models import *

# It take current time as input to record attendance time.
class TimeInput(forms.TimeInput):
    input_type = 'time'
# it takes date as input to record the date
class DateInput(forms.DateInput):
    input_type = 'date'

# this is the main form used to tahe member details as input and their image to upload it to dataset.
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student_profile
        fields = '__all__'
        widgets = {
            'date': DateInput(),
        }
        exclude = ['present','updated']

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        #self.fields['date'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['roll_number'].widget.attrs['class'] = 'form-control'
        self.fields['profession'].widget.attrs['class'] = 'form-control'
        self.fields['class_name'].widget.attrs['class'] = 'form-control'
        #self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['subject_code'].widget.attrs['class'] = 'form-control'