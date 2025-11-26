from django.conf import settings
from django.db import models

# This is the default Django User model (username, email, password, etc.)
User = settings.AUTH_USER_MODEL


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile({self.user.username})"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    label = models.CharField(
        max_length=50,
        default="Site",
        help_text="Short label like 'Home', 'Site A', etc.",
    )
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    additional_directions = models.TextField(blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.label} - {self.city}"