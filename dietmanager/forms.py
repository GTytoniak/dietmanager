from django import forms
#from .models import UserData
# from django.core.validators import validate_email
# from django.core.exceptions import ValidationError
# from django.forms import ModelForm



class AddUserForm(forms.Form):
    username = forms.CharField(label= "Username", )
    password = forms.CharField(widget=forms.PasswordInput, label= "Password:")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label= "Confirm your password:")
    first_name = forms.CharField(label= "First name:")
    last_name = forms.CharField(label= "Last name:")
    email = forms.CharField(label= "Email:")

    
class LoginForm(forms.Form):
    username = forms.CharField(label= "Username")
    password= forms.CharField(widget=forms.PasswordInput, label= "Password")
    
class BmiForm(forms.Form):
    weight = forms.IntegerField(label= "Weight(kg):")
    height = forms.FloatField(label= "Height(m):")
    
class BmiModifyForm(forms.Form):
    weight = forms.IntegerField(label= "Weight(kg):")
    height = forms.FloatField(label= "Height(m):")
    
class GdaForm(forms.Form):
    SEX = (
    (1.0, "Man"),
    (0.9, "Woman"),    
    )

    ACTIVITY = (
    (1.0, "Small activity, sitting job"),
    (1.1, "Sporadic activity(once a week), sitting job"),
    (1.2, "Activity 1-2 times a week, sitting job"),
    (1.3, "Intense activity (eg. fitness) 2-3 times a week, sitting job"),
    (1.4, "Activity everyday (eg. fitness, joggin), job requires movement"),
    (1.5, "Doing a lot of movement all the time, physical job"),
    )
    weight = forms.IntegerField(label= "Weight(kg):")
    sex = forms.ChoiceField(label= "Sex:", widget=forms.RadioSelect, choices=SEX)
    activity = forms.ChoiceField(label= "Your level of activity", widget=forms.RadioSelect, choices=ACTIVITY)
    
class GdaModifyForm(forms.Form):
    SEX = (
    (1.0, "Man"),
    (0.9, "Woman"),    
    )

    ACTIVITY = (
    (1.0, "Small activity, sitting job"),
    (1.1, "Sporadic activity(once a week), sitting job"),
    (1.2, "Activity 1-2 times a week, sitting job"),
    (1.3, "Intense activity (eg. fitness) 2-3 times a week, sitting job"),
    (1.4, "Activity everyday (eg. fitness, joggin), job requires movement"),
    (1.5, "Doing a lot of movement all the time, physical job"),
    )
    weight = forms.IntegerField(label= "Weight(kg):")
    sex = forms.ChoiceField(label= "Sex:", widget=forms.RadioSelect, choices=SEX)
    activity = forms.ChoiceField(label= "Your level of activity", widget=forms.RadioSelect, choices=ACTIVITY)

