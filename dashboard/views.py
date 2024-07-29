from rest_framework import generics, response
from rest_framework.exceptions import ValidationError
from dashboard import models, serializers
from django.db.models import Count
from django.db.models.functions import TruncMonth
from datetime import datetime

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
        start_date = self.request.query_params.get('startDate', None)
        end_date = self.request.query_params.get('endDate', None)
        location = self.request.query_params.get('location', None)
        type_device = self.request.query_params.get('type_device', None)
        browser = self.request.query_params.get('browser', None)
        
        # Filter by start date
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%d/%m/%Y')
            except ValueError:
                raise ValidationError({"detail": "Invalid start date. Please provide a valid date in dd/mm/yyyy format."})
            queryset = queryset.filter(last_date_login__date__gte=start_date.date())
        
        # Filter by end date
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%d/%m/%Y')
            except ValueError:
                raise ValidationError({"detail": "Invalid end date. Please provide a valid date in dd/mm/yyyy format."})
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
        Overrides the list method to include monthly counts in the response.
        """
        queryset = self.get_queryset()
        monthly_counts = self.get_monthly_counts(queryset)
        
        response_data = {
            'monthly_counts': monthly_counts,
            'data': serializers.DashboardDataSerializer(queryset, many=True).data
        }
        return response.Response(response_data)
