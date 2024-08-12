from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name=("Phone Number"))
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name=("Address"))
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name=("City"))
    state = models.CharField(max_length=100, blank=True, null=True, verbose_name=("State"))
    zip_code = models.CharField(max_length=20, blank=True, null=True, verbose_name=("ZIP Code"))
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name=("Country"))
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, verbose_name=("Profile Picture"))
    date_of_birth = models.DateField(blank=True, null=True, verbose_name=("Date of Birth"))
    gender = models.CharField(max_length=10, blank=True, null=True, verbose_name=("Gender"))
    preferred_language = models.CharField(max_length=50, blank=True, null=True, verbose_name=("Preferred Language"))
    currency = models.CharField(max_length=10, blank=True, null=True, verbose_name=("Currency"))
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=("Date Joined"))
    last_login = models.DateTimeField(auto_now=True, verbose_name=("Last Login"))
    is_verified = models.BooleanField(default=False, verbose_name=("Is Verified"))
    token_created_at = models.DateTimeField(null=True, blank=True)
    activation_token = models.CharField(max_length=64, null=True, blank=True)
    reset_token_created_at = models.DateTimeField(null=True, blank=True)
    reset_password_token = models.CharField(max_length=64, null=True, blank=True)

    def is_token_expired(self):
        if self.token_created_at:
            expiration_time = self.token_created_at + timedelta(hours=2)
            return timezone.now() > expiration_time
        return True

    def reset_token_expired(self):
        if self.reset_token_created_at:
            expiration_time = self.reset_token_created_at + timedelta(hours=1)
            return timezone.now() > expiration_time
        return True
    
    def __str__(self) -> str:
        return self.user.username
