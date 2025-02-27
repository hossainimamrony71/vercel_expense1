from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, View
from .models import ExpenseCategory, User, MoneyAllocation, Transaction
from .forms import ExpenseCategoryForm, MoneyAllocationForm
from django.utils import timezone
from django.core.exceptions import PermissionDenied

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib.auth.decorators import login_required
from .forms import MoneyAllocationForm
from .models import MoneyAllocation

@login_required
def allocated_money(request):
    if request.user.user_type != 'admin':
        raise PermissionDenied("Only an admin can allocate money.")

    if request.method == 'POST':
        form = MoneyAllocationForm(request.POST, request=request)
        if form.is_valid():
            try:
                result = form.save()
                if isinstance(result, list):
                    messages.success(request, "Your departmental funds have been updated successfully.")
                else:
                    messages.success(request, f"Money allocated successfully to {result.allocated_to.username}.")
                return redirect('allocated_money')
            except ValidationError as e:
                form.add_error(None, e.messages[0])
                messages.error(request, e.messages[0])
            except Exception as e:
                form.add_error(None, str(e))
                messages.error(request, f"An error occurred: {str(e)}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = MoneyAllocationForm(request=request)

    allocations = MoneyAllocation.objects.all().order_by('-created_at')
    paginator = Paginator(allocations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    current_page = page_obj.number
    total_pages = paginator.num_pages
    max_pages_to_show = 4
    half_window = max_pages_to_show // 2

    if total_pages <= max_pages_to_show:
        start_page = 1
        end_page = total_pages
    else:
        if current_page - half_window <= 0:
            start_page = 1
            end_page = max_pages_to_show
        elif current_page + half_window > total_pages:
            start_page = total_pages - max_pages_to_show + 1
            end_page = total_pages
        else:
            start_page = current_page - half_window
            end_page = current_page + half_window - (1 if max_pages_to_show % 2 == 0 else 0)
    page_range = range(start_page, end_page + 1)

    context = {
        'form': form,
        'page_obj': page_obj,
        'page_range': page_range,
        'start_page': start_page,
        'end_page': end_page,
    }
    return render(request, 'allocated_money.html', context)





class TedS2lCategoryList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ExpenseCategory
    template_name = 'categorylist.html'
    context_object_name = 'categories'
    paginate_by = 8
    
    def get_queryset(self):
        user_type = self.kwargs.get('user_type')
        if user_type not in user_type:
            return ExpenseCategory.objects.none()  

        return ExpenseCategory.objects.filter(
            created_by__user_type=user_type
        ).order_by('-created_at')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_button'] = self.request.user.user_type != 'admin' 
        return context
    
    def test_func(self):
        return self.request.user.user_type == 'admin' or self.request.user.is_superuser






from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib.auth.decorators import login_required
from .forms import MoneyAllocationForm
from .models import MoneyAllocation

@login_required
def allocated_money(request):
    if request.user.user_type != 'admin':
        raise PermissionDenied("Only an admin can allocate money.")

    if request.method == 'POST':
        form = MoneyAllocationForm(request.POST, request=request)
        if form.is_valid():
            try:
                result = form.save()
                if isinstance(result, list):
                    messages.success(request, "Your departmental funds have been updated successfully.")
                else:
                    messages.success(request, f"Money allocated successfully to {result.allocated_to.username}.")
                return redirect('allocated_money')
            except ValidationError as e:
                form.add_error(None, e.messages[0])
                messages.error(request, e.messages[0])
            except Exception as e:
                form.add_error(None, str(e))
                messages.error(request, f"An error occurred: {str(e)}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = MoneyAllocationForm(request=request)

    allocations = MoneyAllocation.objects.all().order_by('-created_at')
    paginator = Paginator(allocations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    current_page = page_obj.number
    total_pages = paginator.num_pages
    max_pages_to_show = 4
    half_window = max_pages_to_show // 2

    if total_pages <= max_pages_to_show:
        start_page = 1
        end_page = total_pages
    else:
        if current_page - half_window <= 0:
            start_page = 1
            end_page = max_pages_to_show
        elif current_page + half_window > total_pages:
            start_page = total_pages - max_pages_to_show + 1
            end_page = total_pages
        else:
            start_page = current_page - half_window
            end_page = current_page + half_window - (1 if max_pages_to_show % 2 == 0 else 0)
    page_range = range(start_page, end_page + 1)

    context = {
        'form': form,
        'page_obj': page_obj,
        'page_range': page_range,
        'start_page': start_page,
        'end_page': end_page,
    }
    return render(request, 'allocated_money.html', context)





from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal
from datetime import datetime
from .models import Transaction, ExpenseCategory

from datetime import datetime
from decimal import Decimal
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from account.models import User  # Adjust this import as needed.
from .models import Transaction, ExpenseCategory
from django.utils.timezone import make_aware



class TedS2lExpenseListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Transaction
    template_name = 'expenselist.html'
    context_object_name = 'expenses'
    paginate_by = 10

    def get_queryset(self):
        user_type = self.kwargs.get('user_type')
        qs = Transaction.objects.filter(user__user_type=user_type)
        
        # Date filter
        date_str = self.request.GET.get('date')
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                qs = qs.filter(created_at__date=date_obj)
            except ValueError:
                pass

        # Category filter
        category = self.request.GET.get('category')
        if category:
            qs = qs.filter(category_id=category)

        # Amount filter
        amount = self.request.GET.get('amount')
        if amount:
            try:
                amount_val = Decimal(amount)
                qs = qs.filter(ammount=amount_val)
            except Exception:
                pass

        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_type = self.kwargs.get('user_type')
        now = timezone.now()
        if timezone.is_naive(now):
            now = make_aware(now)  # Convert to an aware datetime
        now = timezone.localtime(now)  # Convert to Bangladesh time
        
        
        # Today's boundaries
        start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_today = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Aggregates
        today_expense = Transaction.objects.filter(
            user__user_type=user_type,
            created_at__range=(start_of_today, end_of_today)
        ).aggregate(total=Sum('ammount'))['total'] or 0

        total_expense = Transaction.objects.filter(
            user__user_type=user_type
        ).aggregate(total=Sum('ammount'))['total'] or 0

        user_stats = User.objects.filter(user_type=user_type).aggregate(
            total_balance=Sum('balance'),
            total_loan_balance=Sum('loan_balance')
        )
        user_type = self.kwargs.get('user_type')
        context['user_type'] = user_type 
        context['show_button'] = self.request.user.user_type == 'admin'
        context['show_add_button'] = False
        context.update({
            
            'today_expense': today_expense,
            'total_expense': total_expense,
            'balance': user_stats['total_balance'] or 0,
            'loan_balance': user_stats['total_loan_balance'] or 0,
            'categories': ExpenseCategory.objects.filter(created_by=self.request.user)
        })
        return context

    def test_func(self):
        return self.request.user.user_type == 'admin' or self.request.user.is_superuser





from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ExpenseCategory
from .forms import ExpenseCategoryForm, ExpenseSubCategoryFormSet

# ---------------------------------------------------------------------
# List View: Display all categories created by the current user.
# ---------------------------------------------------------------------
class ExpenseCategoryListView(LoginRequiredMixin, ListView):
    model = ExpenseCategory
    template_name = 'categorylist.html'
    context_object_name = 'categories'
    paginate_by = 8
    
    def get_queryset(self):
        return ExpenseCategory.objects.filter(created_by=self.request.user).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_button'] = True
        return context

# ---------------------------------------------------------------------
# Create View: Add a new expense category along with subcategories.
# ---------------------------------------------------------------------
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ExpenseCategory
from .forms import ExpenseCategoryForm, ExpenseSubCategoryFormSet

from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ExpenseCategory, ExpenseSubCategory
from .forms import ExpenseCategoryForm, ExpenseSubCategoryFormSet

class ExpenseCategoryCreateView(LoginRequiredMixin, CreateView):
    model = ExpenseCategory
    form_class = ExpenseCategoryForm
    template_name = 'addcategory.html'
    success_url = reverse_lazy('category-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ExpenseCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = ExpenseCategory
    form_class = ExpenseCategoryForm
    template_name = 'addcategory.html'
    success_url = reverse_lazy('category-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['subcategories'] = ExpenseSubCategoryFormSet(
                self.request.POST, 
                instance=self.object,
                prefix='subcategories'
            )
        else:
            context['subcategories'] = ExpenseSubCategoryFormSet(
                instance=self.object,
                prefix='subcategories'
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        subcategories = context['subcategories']
        if subcategories.is_valid():
            self.object = form.save()
            subcategories.instance = self.object
            subcategories.save()
            return super().form_valid(form)
        return self.render_to_response(self.get_context_data(form=form))

# views.py
from django.http import JsonResponse
from .models import ExpenseSubCategory

def load_subcategories(request):
    category_id = request.GET.get('category')
    subcategories = ExpenseSubCategory.objects.filter(parent_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

# ---------------------------------------------------------------------
# AJAX Delete View: Delete a category inline via AJAX from the list page.
# ---------------------------------------------------------------------
class ExpenseCategoryAjaxDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        try:
            category = ExpenseCategory.objects.get(pk=pk, created_by=request.user)
            category.delete()
            return JsonResponse({'success': True})
        except ExpenseCategory.DoesNotExist:
            return JsonResponse(
                {'success': False, 'error': 'Category not found.'},
                status=404
            )


from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django import forms

  # Added import for User

from .models import Transaction, ExpenseCategory
from .forms import TransactionForm


from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction, ExpenseCategory, ExpenseSubCategory
from .forms import TransactionForm

class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'addexpense.html'
    success_url = reverse_lazy('expense-list')

    def form_valid(self, form):
        with transaction.atomic():
            user = self.request.user
            amount = form.cleaned_data['ammount']

            # Check if the user has sufficient balance
            if user.balance < amount:
                form.add_error('ammount', 'Insufficient balance.')
                return self.form_invalid(form)

            # Deduct the amount from the user's balance
            user.balance -= amount
            user.save()

            form.instance.user = user

            # Pop the subcategory value so it's not automatically assigned.
            subcategory_value = form.cleaned_data.pop('subcategory')
            print("Subcategory value:", subcategory_value, type(subcategory_value))
            
            # If the value is all digits, treat it as an existing subcategory ID.
            if str(subcategory_value).isdigit():
                try:
                    subcat = ExpenseSubCategory.objects.get(id=int(subcategory_value))
                except ExpenseSubCategory.DoesNotExist:
                    form.add_error('subcategory', 'Selected subcategory does not exist.')
                    return self.form_invalid(form)
            else:
                # Otherwise, create a new subcategory under the selected category.
                category_instance = form.cleaned_data['category']
                subcat, created = ExpenseSubCategory.objects.get_or_create(
                    parent=category_instance,
                    name=subcategory_value,
                    defaults={'description': ''}
                )
                print("New subcategory created:", created)
                    
            # Assign the ExpenseSubCategory instance to the transaction
            form.instance.subcategory = subcat

            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Provide the categories list for the select dropdown
        context['categories'] = ExpenseCategory.objects.filter(
            created_by=self.request.user
        ).order_by('-created_at')
        # Subcategories will be loaded via AJAX, so we initialize it as empty.
        context['subcategories'] = []
        context['is_update'] = False  # flag for template usage
        return context

# AJAX view to load subcategories for a selected category
def load_subcategories(request):
    category_id = request.GET.get('category')
    subcategories = []
    if category_id:
        qs = ExpenseSubCategory.objects.filter(parent_id=category_id).order_by('name')
        for sub in qs:
            subcategories.append({'id': sub.id, 'name': sub.name})
    return JsonResponse(subcategories, safe=False)


from django.utils.decorators import method_decorator
from .decorators import admin_required

@method_decorator(admin_required, name='dispatch')
class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'addexpense.html'
    success_url = reverse_lazy('expense-list')

    def get_success_url(self):
        user_type = self.object.user.user_type  # Get the user_type of the transaction's user
        return reverse_lazy('ted_s2l_expense_list', kwargs={'user_type': user_type})
    
    def get_queryset(self):
        return Transaction.objects.all()

    def form_valid(self, form):
        with transaction.atomic():
            transaction_obj = self.get_object()
            # Lock the transaction row for update
            transaction_obj = Transaction.objects.select_for_update().get(pk=transaction_obj.pk)
            user = User.objects.select_for_update().get(pk=transaction_obj.user.pk)

            original_amount = transaction_obj.ammount
            new_amount = form.cleaned_data['ammount']
            amount_diff = new_amount - original_amount

            if amount_diff > 0 and user.balance < amount_diff:
                form.add_error('ammount', 'Insufficient balance to cover the increase.')
                return self.form_invalid(form)

            user.balance -= amount_diff
            user.save()

            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ExpenseCategory.objects.filter(
            created_by=self.request.user
        ).order_by('-created_at')
        context['subcategories'] = []
        context['is_update'] = True  # Flag to indicate an update view
        return context

# views.py
class ExpenseListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'expenselist.html'
    context_object_name = 'expenses'
    paginate_by = 100
    
    def get_queryset(self):
        qs = Transaction.objects.filter(user=self.request.user)
        
        # Filters
        date_str = self.request.GET.get('date')
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                qs = qs.filter(created_at__date=date_obj)
            except ValueError:
                pass

        category = self.request.GET.get('category')
        if category:
            qs = qs.filter(category_id=category)
        
        voucher = self.request.GET.get('voucher')
        if voucher:
            qs = qs.filter(voucher=voucher)

        transaction_type = self.request.GET.get('transaction_type')
        if transaction_type:
            qs = qs.filter(transaction_type=transaction_type)

        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_add_button'] = True
        context['show_button'] = self.request.user.user_type == 'admin'
        return context

  
class ExpenseDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        try:
            with transaction.atomic():
                # Lock the transaction and user rows
                expense = Transaction.objects.select_for_update().get(pk=pk)
                user = User.objects.select_for_update().get(pk=expense.user.pk)

                user.balance += expense.ammount
                user.save()

                expense.delete()
                return JsonResponse({'success': True})
        except Transaction.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Expense not found.'}, status=404)

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import LoanRequest, User
from .forms import LoanRequestForm

@login_required
def create_loan_request(request):
    # Only allow TED and S2L users to create a loan request.
    if request.user.user_type not in ['ted', 's2l']:
        messages.error(request, "Only TED and S2L departments can create loan requests.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoanRequestForm(request.POST, user=request.user)
        if form.is_valid():
            loan_request = form.save(commit=False)
            # Automatically set the “from_department” as the current user’s department.
            loan_request.from_department = request.user.user_type
            loan_request.save()
            messages.success(request, "Loan request submitted successfully.")
            return redirect('loan_ted_s2l')
    else:
        form = LoanRequestForm(user=request.user)
    
    # List all loan requests from the current user’s department.
    allocations = LoanRequest.objects.filter(from_department=request.user.user_type).order_by('-requested_at')
    return render(request, 'loan_ted_s2l.html', {'form': form, 'allocations': allocations})

# Helper function for admin check
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from .models import LoanRequest, User
from .forms import LoanRequestForm

def is_admin(user):
    return user.user_type == 'admin'

@login_required
@user_passes_test(is_admin)
def loan_admin(request):
    # Retrieve all loan requests (regardless of status)
    loans = LoanRequest.objects.all().order_by('-requested_at')
    
    # Get today's date
    today = timezone.now().date()
    
    # Aggregate approved loans taken today by department.
    # For example, if a department takes a loan, its department code is stored in from_department.
    ted_today = LoanRequest.objects.filter(
        status='approved',
        requested_at__date=today,
        from_department='ted'
    ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    s2l_today = LoanRequest.objects.filter(
        status='approved',
        requested_at__date=today,
        from_department='s2l'
    ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    # Aggregate overall approved loans by department.
    ted_total = LoanRequest.objects.filter(
        status='approved',
        from_department='ted'
    ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    s2l_total = LoanRequest.objects.filter(
        status='approved',
        from_department='s2l'
    ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    context = {
        'loans': loans,
        'ted_today': ted_today,
        's2l_today': s2l_today,
        'ted_total': ted_total,
        's2l_total': s2l_total,
    }
    return render(request, 'loan_admin.html', context)

@login_required
@user_passes_test(is_admin)
def approve_loan_request(request, pk):
    loan_request = get_object_or_404(LoanRequest, pk=pk)
    try:
        loan_request.approve(request.user)
        messages.success(request, f"Loan request #{loan_request.id} approved.")
    except Exception as e:
        messages.error(request, f"Error approving loan request: {str(e)}")
    return redirect('loan_admin')

@login_required
@user_passes_test(is_admin)
def decline_loan_request(request, pk):
    loan_request = get_object_or_404(LoanRequest, pk=pk)
    try:
        loan_request.decline(request.user)
        messages.success(request, f"Loan request #{loan_request.id} declined.")
    except Exception as e:
        messages.error(request, f"Error declining loan request: {str(e)}")
    return redirect('loan_admin')