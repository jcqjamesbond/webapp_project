from django import forms

from django.contrib.auth.models import User
from linterest.models import *
import datetime

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length = 20)
    email = forms.EmailField(max_length = 40)
    firstname = forms.CharField(max_length = 40)
    lastname = forms.CharField(max_length = 40)
    password1 = forms.CharField(max_length = 40, label = 'Password',
                                widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 40, label = 'ConfirmPassword',
                                widget = forms.PasswordInput())

    # Customizes form validation for properties that apply to more than one field.
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        # confirm that the two passwords fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match")
        # Generally return the cleaned data we got from our parent.
        return cleaned_data

    # Customize form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already in the User model database
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact = username):
            raise forms.ValidationError("Username is already taken")
        # Generally return the cleaned data we got from the cleaned data
        return username


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
        widgets = {
            'picture': forms.FileInput(),
            'age': forms.TextInput(),
            'bio': forms.TextInput(),
            'phone': forms.TextInput()
        }

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        age = self.cleaned_data.get('age')
        phone = self.cleaned_data.get('phone')
        if age != '':
            try:
                age = int(age)
                if age <= 0:
                    raise forms.ValidationError('Age Should Be a Positive Number')
            except ValueError:
                raise forms.ValidationError('Invalid Age Type')
        if phone != '':
            try:
                phone = int(phone)
                if phone <= 0:
                    raise forms.ValidationError('Invalid Phone Number Type')
            except ValueError:
                raise forms.ValidationError('Invalid Phone Number Type')
        return cleaned_data

# class ProfileForm(forms.Form):
#     gender = models.CharField(max_length=20)
#     age = models.CharField(max_length=10)
#     bio = models.CharField(max_length=420)
#     # picture = models.ImageField(upload_to="profile_pictures", blank=True)
#     phone = models.CharField(max_length=40)

class EventForm(forms.Form):
    type = forms.CharField(max_length = 30)
    city = forms.CharField(max_length = 100)
    # start_time = forms.DateTimeField(initial=datetime.date.today)
    # end_time = forms.DateTimeField(initial=datetime.date.today)
    start_time_text = forms.CharField(max_length = 100)
    end_time_text = forms.CharField(max_length = 100)
    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(EventForm, self).clean()
        current_time_text = str(datetime.datetime.now())
        type = self.cleaned_data.get('type')
        city = self.cleaned_data.get('city')
        start_time_text = self.cleaned_data.get('start_time_text')
        end_time_text = self.cleaned_data.get('end_time_text')
        username = self.cleaned_data.get('username')
        # Checks the validity of the form data
        if not type:
            cleaned_data['error'] = "Event type is required."
            raise forms.ValidationError("Event type is required.")
        if not city:
            cleaned_data['error'] = "City is required."
            raise forms.ValidationError("City is required.")
        if not start_time_text:
            cleaned_data['error'] = "Start time is required."
            raise forms.ValidationError("Start time is required.")
        if not end_time_text:
            cleaned_data['error'] = "End time is required."
            raise forms.ValidationError("End time is required.")
        if not (type=='meal' or type=='drink' or type=='party' or type=='movie'):
            cleaned_data['error'] = "Incorrect event type."
            raise forms.ValidationError("Incorrect event type.")
        if start_time_text < current_time_text:
            cleaned_data['error'] = "Cannot select previous date."
            raise forms.ValidationError("Cannot select previous date.")
        if start_time_text > end_time_text:
            cleaned_data['error'] = "End time should be greater than start time."
            raise forms.ValidationError("End time should be greater than start time.")

        try:
            start_time = datetime.datetime.strptime(start_time_text,'%Y-%m-%dT%H:%M')
        except ValueError:
            cleaned_data['error'] = "Start time has incorrect format."
            raise forms.ValidationError("Start time has incorrect format.")
        cleaned_data['start_time'] = start_time

        try:
            end_time = datetime.datetime.strptime(end_time_text,'%Y-%m-%dT%H:%M')
        except ValueError:
            cleaned_data['error'] = "End time has incorrect format."
            raise forms.ValidationError("End time has incorrect format.")
        cleaned_data['end_time'] = end_time

        # Generally return the cleaned data we got from our parent.
        return cleaned_data


class ForgetPasswordForm(forms.Form):
    username = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','id':'inputUsername'}))

    def clean(self):
        cleaned_data = super(ForgetPasswordForm,self).clean()
        username = cleaned_data.get('username')
        if not User.objects.filter(username=username):
            cleaned_data['error'] = "Username does not exist!"
            raise forms.ValidationError('username does not exist!')
        return cleaned_data


class PasswordResetForm(forms.Form):
        # username = forms.CharField(max_length = 20)
        password1 = forms.CharField(max_length = 200, label='',widget = forms.PasswordInput(attrs={'class': 'input','placeholder':"Password" }))
        password2 = forms.CharField(max_length = 200,  label='',widget = forms.PasswordInput(attrs={'class': 'input','placeholder':"Confirm Password" }))

        def clean(self):
                cleaned_data = super(PasswordResetForm,self).clean()
                password1 = cleaned_data.get('password1')
                password2 = cleaned_data.get('password2')
                if password1 and password2 and password1 != password2:
                        raise forms.ValidationError("Password did not match.")
