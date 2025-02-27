from django.db import models
from account.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


from django.db import models
from django.core.exceptions import ValidationError
from account.models import User


class ExpenseCategory(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense_categories')
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ExpenseSubCategory(models.Model):
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    parent = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.CASCADE,
        related_name='subcategories'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    ammount = models.DecimalField(max_digits=200, decimal_places=2)
    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.CASCADE,
        related_name="transactions",

    )
    subcategory = models.ForeignKey(
        ExpenseSubCategory,
        on_delete=models.CASCADE,
        related_name="transactions",

    )
    source = models.CharField(max_length=150, default="cash")
    voucher = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(blank=True, null=True)  # Allow null values initially

    def save(self, *args, **kwargs):
        if not self.created_at:  # If no date is provided, set it to now
            self.created_at = timezone.now()
        super().save(*args, **kwargs)
        
    def __str__(self):
        # Safely get category and subcategory names
        category_name = self.category.name if self.category else "No Category"
        subcategory_name = self.subcategory.name if self.subcategory else "No Subcategory"
        return f"{self.user.username} -- {self.ammount} -- {category_name} / {subcategory_name}"

# models.py

from django.db import models, transaction
from django.core.exceptions import ValidationError
from account.models import User  # Assuming your custom User model is in account.models
from django.utils.timezone import now

class MoneyAllocation(models.Model):
    DEPARTMENT_CHOICES = (
        ('ted', 'TED'),
        ('s2l', 'S2L'),
    )

    allocated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='allocations_made',
        help_text="Admin user who makes this allocation."
    )
    allocated_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='allocations_received',
        help_text="The user who receives the allocated money."
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="The amount to allocate (must be greater than zero)."
    )
    source = models.CharField(max_length=50, null=True, blank=True)
    department = models.CharField(
        max_length=10,
        choices=DEPARTMENT_CHOICES,
        help_text="Department fund to use for this allocation."
    )
    created_at = models.DateTimeField(default=now)

    # def clean(self):
    #     # Validate amount and department. For allocations to others,
    #     # the department is auto-set in save(), but we still require a valid value.
    #     if self.amount is None or self.amount <= 0:
    #         raise ValidationError("Amount must be greater than zero.")
    #     if not self.department:
    #         raise ValidationError("Department must be selected.")
    #     elif self.department not in dict(self.DEPARTMENT_CHOICES):
    #         raise ValidationError("Invalid department selected.")

    def save(self, *args, **kwargs):
        # Prevent updates to an existing record.
        if self.pk is not None:
            raise ValidationError("Updates are not allowed for MoneyAllocation once created.")
        # Only an admin can perform an allocation.
        if self.allocated_by.user_type != 'admin':
            raise ValidationError("Only an admin can allocate money.")

        # For allocations to others, auto-set the department based on the recipient’s user type.
        if self.allocated_to != self.allocated_by:
            if self.allocated_to.user_type in ['ted', 's2l']:
                self.department = self.allocated_to.user_type
            else:
                raise ValidationError("Recipient must be either TED or S2L.")

        # Validate the instance.
        self.full_clean()

        admin = self.allocated_by

        with transaction.atomic():
            if self.allocated_to == admin:
                # Self-allocation: Admin is adding funds to one of their departmental pools.
                if self.department == 'ted':
                    admin.admin_ted_balance += self.amount
                elif self.department == 's2l':
                    admin.admin_s2l_balance += self.amount
                # Update overall admin balance as the sum of departmental funds.
                admin.balance = admin.admin_ted_balance + admin.admin_s2l_balance
                admin.save()
            else:
                # Allocation to another user:
                if self.department == 'ted':
                    if admin.admin_ted_balance < self.amount:
                        raise ValidationError("Insufficient TED funds.")
                    admin.admin_ted_balance -= self.amount
                elif self.department == 's2l':
                    if admin.admin_s2l_balance < self.amount:
                        raise ValidationError("Insufficient S2L funds.")
                    admin.admin_s2l_balance -= self.amount

                # Update overall admin balance after deduction.
                admin.balance = admin.admin_ted_balance + admin.admin_s2l_balance
                admin.save()

                # Credit the recipient's balance.
                self.allocated_to.balance += self.amount
                self.allocated_to.save()

            # Finally, save the allocation record.
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Deletion of MoneyAllocation records is not allowed.")

    def __str__(self):
        return f"Allocation of {self.amount} to {self.allocated_to.username} by {self.allocated_by.username} ({self.department})"





class LoanRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    )
    
    from_department = models.CharField(max_length=50, choices=User.CHOICES_USER_TYPE)
    to_department = models.CharField(max_length=50, choices=User.CHOICES_USER_TYPE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='approved_loans'
    )

    def __str__(self):
        return f"Loan from {self.get_from_department_display()} to {self.get_to_department_display()} - {self.amount}"
    
    def approve(self, user):
        if self.status != 'pending':
            raise ValueError('Loan is not pending')
        
        # Find users by department type (this example assumes one user per department)
        from_user = User.objects.filter(user_type=self.from_department).first()
        to_user = User.objects.filter(user_type=self.to_department).first()
        
        if not to_user or not from_user:
            raise ValueError('User not found')
        
        if self.amount > to_user.balance:
            raise ValueError('Insufficient balance')
        
        self.status = 'approved'
        self.approved_at = timezone.now()
        self.approved_by = user
        self.save()
        
        # Update balances
        to_user.balance -= self.amount
        from_user.balance += self.amount
        
        # Update loan balances
        to_user.loan_balance += self.amount
        from_user.loan_balance -= self.amount
        
        to_user.save()
        from_user.save()
    
    def decline(self, user):
        if self.status != 'pending':
            raise ValueError('Loan is not pending')
        self.status = 'declined'
        self.approved_at = timezone.now()
        self.approved_by = user
        self.save()
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            original = LoanRequest.objects.get(pk=self.pk)
            if original.status == 'approved':
                raise ValidationError('Approved loan requests cannot be updated.')
        super().save(*args, **kwargs)