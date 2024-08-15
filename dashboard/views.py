from rest_framework import generics, response
from rest_framework.exceptions import ValidationError
from dashboard import models, serializers
from django.db.models import Count
from django.db.models.functions import TruncMonth, ExtractYear
from django.utils.dateparse import parse_date
from datetime import datetime
from django.utils.timezone import now

from openpyxl import Workbook
from openpyxl.styles import Font
import io
from django.http import HttpResponse

class FindAllDashboardDataView(generics.ListAPIView):
    """
    API view to retrieve DashboardData objects with optional filtering and monthly count.
    """
    serializer_class = serializers.DashboardDataSerializer

    def get_queryset(self):
        """
        Retrieves the queryset of DashboardData objects, optionally filtering by the provided parameters.
        """
        queryset = models.DashboardData.objects.all()
        
        # Get filter parameters from the request
        start_date_str = self.request.query_params.get('startDate')
        end_date_str = self.request.query_params.get('endDate')
        location = self.request.query_params.get('location')
        type_device = self.request.query_params.get('type_device')
        browser = self.request.query_params.get('browser')

        # Filter by start date 
        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                queryset = queryset.filter(last_date_login__date__gte=start_date.date())
            except ValueError:
                raise ValidationError({"detail": "Invalid start date. Please provide a valid date in YYYY-MM-DD format."})
        
        # Filter by end date
        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                queryset = queryset.filter(last_date_login__date__lte=end_date.date())
            except ValueError:
                raise ValidationError({"detail": "Invalid end date. Please provide a valid date in YYYY-MM-DD format."})
        
        # Filter by location
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        # Filter by device type
        if type_device:
            queryset = queryset.filter(type_device__icontains=type_device)
        
        # Filter by browser
        if browser:
            queryset = queryset.filter(browser__icontains=browser)

        if not queryset.exists():
            raise ValidationError({"detail": "No data found for the given filters."})
        
        return queryset

    def get_monthly_counts(self, queryset):
        """
        Retrieves the count of DashboardData objects aggregated by month and year.
        """
        results = (queryset
                   .annotate(month=TruncMonth('last_date_login'))
                   .values('month')
                   .annotate(count=Count('id'))
                   .order_by('month'))

        # Format the month field to return month number and year
        formatted_results = []
        for result in results:
            month_date = result['month']
            month_number = month_date.month
            year = month_date.year
            formatted_results.append({
                'month': month_number,
                'year': year,
                'count': result['count']
            })
        
        return formatted_results

    def list(self, request, *args, **kwargs):
        """
        Overrides the list method to include monthly counts and browser categorization in the response.
        """
        queryset = self.get_queryset()
        monthly_counts = self.get_monthly_counts(queryset)

        # Update the browser field
        for data in queryset:
            if data.browser not in ['Chrome', 'Firefox', 'Edge', 'Safari']:
                data.browser = 'Outros'

        response_data = {
            'monthly_counts': monthly_counts,
            'data': serializers.DashboardDataSerializer(queryset, many=True).data
        }
        return response.Response(response_data)


class FindDashboardDataYearsView(generics.ListAPIView):
    """
    API view to retrieve DashboardData objects with optional filtering by year range.
    """
    serializer_class = serializers.DashboardDataSerializer

    def get_queryset(self):
        """
        Retrieves the queryset of DashboardData objects, filtering by the provided year range.
        """
        queryset = models.DashboardData.objects.all()
        
        # Get filter parameters from the request
        start_date_str = self.request.query_params.get('startDate', None)
        end_date_str = self.request.query_params.get('endDate', None)

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            except ValueError:
                raise ValidationError({"detail": "Invalid start date. Please provide a valid date in YYYY-MM-DD format."})
        else:
            start_date = None
        
        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            except ValueError:
                raise ValidationError({"detail": "Invalid end date. Please provide a valid date in YYYY-MM-DD format."})
        else:
            end_date = None
        
        if start_date and end_date:
            start_year = datetime(start_date.year, 1, 1)
            end_year = datetime(end_date.year, 12, 31)
            queryset = queryset.filter(last_date_login__range=[start_year, end_year])
        elif start_date:
            start_year = datetime(start_date.year, 1, 1)
            queryset = queryset.filter(last_date_login__gte=start_year)
        elif end_date:
            end_year = datetime(end_date.year, 12, 31)
            queryset = queryset.filter(last_date_login__lte=end_year)

        # Annotate and aggregate the data
        results = (queryset
                   .annotate(year=ExtractYear('last_date_login'))
                   .values('year')
                   .annotate(count=Count('id'))
                   .order_by('year'))

        # Format the results
        formatted_results = [{'year': result['year'], 'count': result['count']} for result in results]

        return formatted_results

    def list(self, request, *args, **kwargs):
        """
        Overrides the list method to return yearly totals in the response.
        """
        queryset = self.get_queryset()

        response_data = {
            'yearly_totals': queryset  # Since get_queryset already returns formatted results
        }

        return response.Response(response_data)

class GenCSV(generics.GenericAPIView):
    serializer_class = serializers.DashboardDataSerializer

    def get_queryset(self):
        """
        Retrieves the queryset of DashboardData objects, optionally filtering by the provided parameters.
        """
        queryset = models.DashboardData.objects.all()
        
        # Get filter parameters from the request
        start_date = self.request.query_params.get('startDate', None)
        end_date = self.request.query_params.get('endDate', None)
        location = self.request.query_params.get('location', None)
        type_device = self.request.query_params.get('type_device', None)
        browser = self.request.query_params.get('browser', None)
        
        # Filter by start date
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
            except ValueError:
                raise ValidationError({"detail": "Invalid start date. Please provide a valid date in yyyy/mm/dd format."})
            queryset = queryset.filter(last_date_login__date__gte=start_date.date())
        
        # Filter by end date
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                raise ValidationError({"detail": "Invalid end date. Please provide a valid date in yyyy/mm/dd format."})
            queryset = queryset.filter(last_date_login__date__lte=end_date.date())
        
        # Filter by location
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        # Filter by device type
        if type_device:
            queryset = queryset.filter(type_device__icontains=type_device)
        
        # Filter by browser
        if browser:
            queryset = queryset.filter(browser__icontains=browser)

        if not queryset.exists():
            raise ValidationError({"detail": "No data found for the given filters."})
        
        return queryset

    def generate_excel(self, data):
        """
        Gera um arquivo Excel com os dados fornecidos.
        
        :param data: Lista de dicionários contendo os dados a serem exportados.
        :return: Conteúdo do arquivo Excel como uma string.
        """
        # Create a new Workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Dashboard Data"

        # Define the headers
        headers = ['last_date_login', 'location', 'type_device', 'browser']
        ws.append(headers)

        bold_font = Font(bold=True)
        for cell in ws[1]:
            cell.font = bold_font

        # Add data rows
        for row in data:
            ws.append([row.get('last_date_login'), row.get('location'), row.get('type_device'), row.get('browser')])
        
        # Save the workbook to a virtual file
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        
        return output

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests for generating and downloading the Excel file.
        """
        queryset = self.get_queryset()
        data = serializers.DashboardDataSerializer(queryset, many=True).data
        excel_content = self.generate_excel(data)
        
        response = HttpResponse(excel_content, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="dashboard_data.xlsx"'
        
        return response