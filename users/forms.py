from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import get_user_model

User = get_user_model()


class PatientSignupForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'required': True})
    )

    contact = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'required': True}),
        help_text="Mobile number or email"
    )

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")

        return username

    def clean_contact(self):
        contact = self.cleaned_data['contact'].strip()

        # Check if email
        if '@' in contact:
            try:
                validate_email(contact)
                return contact
            except ValidationError:
                raise ValidationError("Enter a valid email address")

        # Otherwise assume mobile number
        if not contact.isdigit():
            raise ValidationError("Mobile number must contain only digits")

        if len(contact) < 10 or len(contact) > 15:
            raise ValidationError("Enter a valid mobile number")

        return contact
