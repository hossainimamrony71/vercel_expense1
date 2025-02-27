from django import forms
from .models import ExpenseCategory,Transaction
from django import forms
from .models import Transaction
from django import forms
from .models import MoneyAllocation
from account.models import User


from django import forms
from django.forms import inlineformset_factory
from .models import ExpenseCategory, ExpenseSubCategory

class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ['name', 'description', ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ExpenseSubCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseSubCategory
        fields = ['name', 'description', ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'name': forms.TextInput(),
        }


ExpenseSubCategoryFormSet = inlineformset_factory(
    ExpenseCategory,
    ExpenseSubCategory,
    form=ExpenseSubCategoryForm,
    extra=1,
    can_delete=True,
    fields=['name',  'description']
)


from django import forms
from .models import Transaction, ExpenseCategory, ExpenseSubCategory

# forms.py
from django import forms
from django.forms.widgets import DateInput
from .models import Transaction, ExpenseCategory

class TransactionForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=ExpenseCategory.objects.all(),
        required=True,
        label="Category",
        widget=forms.Select(attrs={
            'id': 'category_select',
            'class': 'form-control'
        })
    )
    # Declare subcategory as a standalone field.
    subcategory = forms.CharField(
        required=True,
        label="Subcategory",
        widget=forms.Select(attrs={
            'id': 'subcategory_select',
            'class': 'form-control'
        })
    )
    # Add an optional created_at field.
    created_at = forms.DateTimeField(
        required=False,
        label="Exact Date",
        widget=DateInput(attrs={
            'type': 'date',  # HTML5 date picker
            'class': 'form-control'
        })
    )

    class Meta:
        model = Transaction
        fields = ['ammount', 'voucher', 'category', 'source', 'created_at']

        
        
from django import forms
from decimal import Decimal
from .models import MoneyAllocation
from account.models import User

class MoneyAllocationForm(forms.ModelForm):
    # Extra fields for when the admin is allocating money to themselves.
    ted_amount = forms.DecimalField(
        required=False,
        min_value=Decimal('0.01'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Enter amount for TED'
        })
    )
    s2l_amount = forms.DecimalField(
        required=False,
        min_value=Decimal('0.01'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Enter amount for S2L'
        })
    )

    class Meta:
        model = MoneyAllocation
        fields = ['allocated_to', 'amount', 'source', 'department']
        widgets = {
            'allocated_to': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Enter Amount'
            }),
            'source': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Source',
                'required': 'true',
            }),
            'department': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MoneyAllocationForm, self).__init__(*args, **kwargs)
        allowed_types = ['admin', 'ted', 's2l']
        self.fields['allocated_to'].queryset = User.objects.filter(user_type__in=allowed_types)
        if self.request:
            self.admin_id = self.request.user.id
        else:
            self.admin_id = None

        # Remove HTML5 required attribute for these fields to prevent browser validation errors
        self.fields['amount'].required = False
        self.fields['department'].required = False
        self.fields['amount'].widget.attrs.pop('required', None)
        self.fields['department'].widget.attrs.pop('required', None)

    def clean(self):
        cleaned_data = super().clean()
        allocated_to = cleaned_data.get('allocated_to')

        # Only an admin may allocate money.
        if self.request and self.request.user.user_type != 'admin':
            raise forms.ValidationError("Only an admin can allocate money.")

        if allocated_to and str(allocated_to.id) == str(self.admin_id):
            # Self-allocation: Validate that at least one departmental field is provided.
            ted_amount = cleaned_data.get('ted_amount')
            s2l_amount = cleaned_data.get('s2l_amount')
            if (not ted_amount or ted_amount <= 0) and (not s2l_amount or s2l_amount <= 0):
                raise forms.ValidationError("Enter a valid amount for at least one department (TED or S2L).")
            # Remove the non-applicable fields.
            self.cleaned_data.pop('amount', None)
            self.cleaned_data.pop('department', None)
        else:
            # Allocation to others:
            # Validate the amount field.
            amount = cleaned_data.get('amount')
            if not amount or amount <= 0:
                self.add_error('amount', "Amount must be greater than zero.")
            # Auto-set department based on recipient’s user type.
            if allocated_to:
                if allocated_to.user_type in ['ted', 's2l']:
                    self.cleaned_data['department'] = allocated_to.user_type
                else:
                    self.add_error('allocated_to', "Recipient must be either TED or S2L.")
            else:
                self.add_error('allocated_to', "Please select a recipient.")
            # Remove self-allocation fields.
            self.cleaned_data.pop('ted_amount', None)
            self.cleaned_data.pop('s2l_amount', None)
        return cleaned_data

    def save(self, commit=True):
        allocated_by = self.request.user
        allocated_to = self.cleaned_data['allocated_to']
        source = self.cleaned_data.get('source', '')

        if str(allocated_to.id) == str(self.admin_id):
            # Self-allocation: Create separate records for each department.
            allocations = []
            ted_amount = self.cleaned_data.get('ted_amount')
            s2l_amount = self.cleaned_data.get('s2l_amount')
            if ted_amount and ted_amount > 0:
                allocation = MoneyAllocation(
                    allocated_by=allocated_by,
                    allocated_to=allocated_by,
                    amount=ted_amount,
                    source=source,
                    department='ted'
                )
                allocation.full_clean()
                allocation.save()
                allocations.append(allocation)
            if s2l_amount and s2l_amount > 0:
                allocation = MoneyAllocation(
                    allocated_by=allocated_by,
                    allocated_to=allocated_by,
                    amount=s2l_amount,
                    source=source,
                    department='s2l'
                )
                allocation.full_clean()
                allocation.save()
                allocations.append(allocation)
            return allocations
        else:
            # Allocation to others uses the provided amount and the auto-set department.
            allocation = super().save(commit=False)
            allocation.allocated_by = allocated_by
            allocation.full_clean()
            allocation.save()
            return allocation


# forms.py
from django import forms
from .models import LoanRequest, User

class LoanRequestForm(forms.ModelForm):
    class Meta:
        model = LoanRequest
        fields = ['to_department', 'amount']
        widgets = {
            'to_department': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter Amount'}),
        }
    
    def __init__(self, *args, **kwargs):
        # Pop the current user from the keyword arguments.
        self.user = kwargs.pop('user', None)
        super(LoanRequestForm, self).__init__(*args, **kwargs)
        if self.user:
            # If the user is from TED, they can only request from S2L (and vice versa).
            if self.user.user_type == 'ted':
                self.fields['to_department'].choices = [('s2l', 'S2L Department')]
            elif self.user.user_type == 's2l':
                self.fields['to_department'].choices = [('ted', 'TED Department')]
            else:
                # For admin (or any other type) you could either disable this form or allow both.
                self.fields['to_department'].choices = [choice for choice in User.CHOICES_USER_TYPE if choice[0] in ['ted', 's2l']]
