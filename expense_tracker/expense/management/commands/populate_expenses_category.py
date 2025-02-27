from django.core.management.base import BaseCommand
from account.models import User
from expense.models import ExpenseCategory

class Command(BaseCommand):
    help = 'Populate the ExpenseCategory model with initial data'

    def handle(self, *args, **kwargs):
        # Fetch the user (replace 'username' with an actual username)
        created_by_user = User.objects.get(username='TED')

        expense_items = [
            'Utility Expenses', 'Repair And Maintenance Expenses', 'Transformer Oil Expenses', 
            'Raw Material Expenses', 'Electric Expenses', 'Conveyance Expenses', 'Tiffin Expenses',
            'Medical Allowance', 'IT Expenses', 'Office And Stationary Expenses', 'Water Expenses', 
            'Food Allowance', 'Lunch Expenses', 'Entertainment Expenses', 'Transport Expenses', 
            'Coureir Expenses', 'Sanitary Expenses', 'Labour Expenses', 'Cleaning Expenses', 
            'Paid To Bhai Bhai Engineering Works', 'Tips & Gift Expenses', 'Rent Expenses', 
            'Miscellaneous Expenses', 'Cash Paid To Rifat Sewing To Purchase Monthly Store Material', 
            'Cash Paid To Systech Digital Ltd For Software Reinstallation Purposes', 
            'Cash Paid To McDRY Desiccant Ltd To Purchase Super Dry', 'Transport Expense Uber', 
            'Repair & Maintenance Expenses', 'Furniture Expenses', 'Mobile Allowance', 
            'Standard Test Charges For Intertek', 'Miscellaouse Expenses', 'Thal Expenses', 
            'Thai Expenses', 'Cash Paid To Mr. Ataur For Generator Service Purposes', 'intertek'
        ]

        for item in set(expense_items):  # Ensuring only unique items are added
            ExpenseCategory.objects.get_or_create(name=item, defaults={'created_by': created_by_user})
        
        self.stdout.write(self.style.SUCCESS('Successfully populated ExpenseCategory with initial data'))
