# yourapp/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    CHOICES_USER_TYPE = (
        ('admin', 'Admin'),
        ('ted', 'TED'),
        ('s2l', 'S2L'),
    )
    balance = models.DecimalField(max_digits=200, decimal_places=2, default=0)
    loan_balance = models.DecimalField(max_digits=200, decimal_places=2, default=0)
    user_type = models.CharField(max_length=50, choices=CHOICES_USER_TYPE, default='ted')
    
    # Additional fields from your HTML snippet
    mobile = models.CharField(max_length=20, blank=True, null=True)
    
        # New fields for tracking admin's departmental funds.
    admin_ted_balance = models.DecimalField(max_digits=200, decimal_places=2, default=0)
    admin_s2l_balance = models.DecimalField(max_digits=200, decimal_places=2, default=0)

    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
