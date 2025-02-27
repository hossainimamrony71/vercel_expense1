from django.core.management.base import BaseCommand
from expense.models import Transaction

class Command(BaseCommand):
    help = 'Delete all transactions'

    def handle(self, *args, **kwargs):
        # Count the number of transactions to be deleted
        total_transactions = Transaction.objects.count()
        
        if total_transactions == 0:
            self.stdout.write(self.style.WARNING('No transactions to delete.'))
            return

        # Delete all transactions
        Transaction.objects.all().delete()
        
        # Confirm deletion
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {total_transactions} transactions.'))
