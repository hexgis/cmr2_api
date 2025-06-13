from rest_framework import generics, response, status
from rest_framework.exceptions import ValidationError, ParseError
from django.db.models import Count
from django.db.models.functions import TruncMonth, ExtractYear
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from rest_framework.permissions import IsAuthenticated
from dashboard import models, serializers
from openpyxl import Workbook
from openpyxl.styles import Font

import io


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
            start_date = parse_date(start_date_str)
            if not start_date:
                raise ParseError(
                    {"detail": "Invalid start date. Please provide a valid date in YYYY-MM-DD format."})
            queryset = queryset.filter(last_date_login__date__gte=start_date)

        # Filter by end date
        if end_date_str:
            end_date = parse_date(end_date_str)
            if not end_date:
                raise ParseError(
                    {"detail": "Invalid end date. Please provide a valid date in YYYY-MM-DD format."})
            queryset = queryset.filter(last_date_login__date__lte=end_date)

        # Filter by location
        if location:
            queryset = queryset.filter(location__icontains=location)

        # Filter by device type
        if type_device:
            queryset = queryset.filter(type_device__icontains=type_device)

        # Filter by browser
        if browser:
            queryset = queryset.filter(browser__icontains=browser)

        return queryset

    def get_monthly_counts(self, queryset):
        """
        Retrieves the count of DashboardData objects aggregated by month and year.
        """
        results = (
            queryset.annotate(month=TruncMonth('last_date_login'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )

        # Format the month field to return month number and year
        formatted_results = [
            {
                'month': result['month'].month,
                'year': result['month'].year,
                'count': result['count']
            }
            for result in results
        ]

        return formatted_results

    def list(self, request, *args, **kwargs):
        """
        Overrides the list method to include monthly counts and browser categorization in the response.
        """
        queryset = self.get_queryset()
        monthly_counts = self.get_monthly_counts(queryset)

        # Update the browser field without modifying the original queryset
        serialized_data = serializers.DashboardDataSerializer(
            queryset, many=True).data
        for data in serialized_data:
            if data['browser'] not in ['Chrome', 'Firefox', 'Edge', 'Safari']:
                data['browser'] = 'Outros'

        response_data = {
            'monthly_counts': monthly_counts,
            'data': serialized_data
        }
        return response.Response(response_data, status=status.HTTP_200_OK)


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
        start_date_str = self.request.query_params.get('startDate')
        end_date_str = self.request.query_params.get('endDate')

        # Parse the start date
        if start_date_str:
            start_date = parse_date(start_date_str)
            if not start_date:
                raise ParseError(
                    {"detail": "Invalid start date. Please provide a valid date in YYYY-MM-DD format."})
            queryset = queryset.filter(
                last_date_login__year__gte=start_date.year)

        # Parse the end date
        if end_date_str:
            end_date = parse_date(end_date_str)
            if not end_date:
                raise ParseError(
                    {"detail": "Invalid end date. Please provide a valid date in YYYY-MM-DD format."})
            queryset = queryset.filter(
                last_date_login__year__lte=end_date.year)

        return queryset

    def list(self, request, *args, **kwargs):
        """
        Overrides the list method to return yearly totals in the response.
        """
        queryset = self.get_queryset()

        # Annotate and aggregate the data by year
        results = (
            queryset.annotate(year=ExtractYear('last_date_login'))
            .values('year')
            .annotate(count=Count('id'))
            .order_by('year')
        )

        # Format the results
        formatted_results = [{'year': result['year'],
                              'count': result['count']} for result in results]

        response_data = {
            'yearly_totals': formatted_results
        }

        return response.Response(response_data, status=status.HTTP_200_OK)


class GenCSV(generics.GenericAPIView):
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
            start_date = parse_date(start_date_str)
            if not start_date:
                raise ParseError(
                    {"detail": "Invalid start date. Please provide a valid date in YYYY-MM-DD format."})
            queryset = queryset.filter(last_date_login__date__gte=start_date)

        # Filter by end date
        if end_date_str:
            end_date = parse_date(end_date_str)
            if not end_date:
                raise ParseError(
                    {"detail": "Invalid end date. Please provide a valid date in YYYY-MM-DD format."})
            queryset = queryset.filter(last_date_login__date__lte=end_date)

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
            raise ParseError(
                {"detail": "No data found for the given filters."})

        return queryset

    def generate_csv(self, data):
        """
        Gera um arquivo Excel com os dados fornecidos.

        :param data: Lista de dicionários contendo os dados a serem exportados.
        :return: Conteúdo do arquivo Excel como um objeto BytesIO.
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
            ws.append([row.get('last_date_login'), row.get(
                'location'), row.get('type_device'), row.get('browser')])

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
        data = self.serializer_class(queryset, many=True).data
        excel_content = self.generate_csv(data)

        response = HttpResponse(
            excel_content,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="dashboard_data.xlsx"'

        return response


class FindUserDashboardDataView(generics.ListAPIView):
    """
    Returns the access records (DashboardData) for a specific user.
    """
    serializer_class = serializers.DashboardDataSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')

        if not user_id:
            raise response.Response(
                {"detail": "Parâmetro 'user_id' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return models.DashboardData.objects.filter(user_id=user_id).order_by('-last_date_login')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serialized_data = self.serializer_class(queryset, many=True).data
        return response.Response(serialized_data, status=status.HTTP_200_OK)
