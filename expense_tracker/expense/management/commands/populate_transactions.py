from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from account.models import User
from expense.models import ExpenseCategory, ExpenseSubCategory, Transaction
from django.utils import timezone
import random
import decimal
from datetime import datetime, timedelta
import pytz

class Command(BaseCommand):
    help = 'Populate the Transaction model with sample data for a given year, from February 1st to December 31st, with 10 to 20 transactions per day.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--year',
            type=int,
            required=True,
            help='Specify the year (e.g. 2023) for which transactions will be generated from February 1st to December 31st'
        )

    def handle(self, *args, **options):
        # Fetch the user (replace 'TED' with your desired username)
        User = get_user_model()
        try:
            user = User.objects.get(username='TED')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User "TED" does not exist. Please create this user or adjust the username.'))
            return

        # Fetch all expense categories
        categories = ExpenseCategory.objects.all()
        if not categories.exists():
            self.stdout.write(self.style.ERROR('No ExpenseCategory instances found. Please populate ExpenseCategory first.'))
            return

        # Sample sources for transactions
        sources = ['cash', 'bank transfer', 'credit card', 'mobile payment']

        # Get the year from the command-line arguments
        year = options.get('year')
        tz = pytz.timezone('UTC')  # Adjust the timezone if needed

        # Set start_date as February 1st and end_date as December 31st for the specified year
        start_date = tz.localize(datetime(year, 2, 1, 0, 0, 0))
        end_date = tz.localize(datetime(year, 12, 31, 23, 59, 59, 999999))

        # Calculate total days between start_date and end_date (inclusive)
        total_days = (end_date.date() - start_date.date()).days + 1

        total_transactions_created = 0

        for day_offset in range(total_days):
            current_date = start_date + timedelta(days=day_offset)
            # Create between 10 and 20 transactions per day
            transactions_count = random.randint(10, 20)
            transactions_created = 0

            for _ in range(transactions_count):
                # Select a random expense category
                category = random.choice(categories)

                # Fetch subcategories for the selected category
                subcategories = ExpenseSubCategory.objects.filter(parent=category)
                if subcategories.exists():
                    subcategory = random.choice(subcategories)
                else:
                    # Create a subcategory if none exists
                    subcategory_name = f"Subcategory {random.randint(1, 10000)}"
                    subcategory = ExpenseSubCategory.objects.create(
                        parent=category,
                        name=subcategory_name,
                        created_by=user
                    )

                # Generate a random amount between 50.00 and 10000.00
                amount_value = decimal.Decimal(random.uniform(50.0, 10000.0)).quantize(decimal.Decimal('0.01'))

                # Randomly select a source
                source = random.choice(sources)

                # Generate a unique voucher identifier
                voucher = f"VOUCHER-{timezone.now().strftime('%Y%m%d%H%M%S%f')}-{random.randint(1, 100000)}"

                # Generate a random time on the current day
                random_hour = random.randint(0, 23)
                random_minute = random.randint(0, 59)
                random_second = random.randint(0, 59)
                created_at = current_date.replace(hour=random_hour, minute=random_minute, second=random_second)

                # Create the transaction record
                Transaction.objects.create(
                    user=user,
                    ammount=amount_value,
                    category=category,
                    subcategory=subcategory,
                    source=source,
                    voucher=voucher,
                    created_at=created_at
                )

                transactions_created += 1
                total_transactions_created += 1

            self.stdout.write(self.style.SUCCESS(
                f"Created {transactions_created} transactions for {current_date.strftime('%Y-%m-%d')}"
            ))

        self.stdout.write(self.style.SUCCESS(
            f"Successfully created a total of {total_transactions_created} transactions from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}."
        ))
