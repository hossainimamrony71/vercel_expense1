from django.urls import path
from .views import FinanceReportView,dashboard,generate_report

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('finance-report/', FinanceReportView.as_view(), name='finance_report'),
 
    path('generate_report_pdf/<int:month>/<int:year>/', generate_report, name='generate_report_pdf'),
]
