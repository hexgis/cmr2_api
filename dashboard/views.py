from rest_framework import generics, response
from rest_framework.exceptions import NotFound, ValidationError
from dashboard import (models, serializers)
from django.contrib.auth.models import User


class FindAllDashboardDataView(generics.ListAPIView):
    """
        API view to retrieve DashboardData objects with optional filtering by user ID.

        Attributes:
        - serializer_class: The serializer class to be used for the response.
        
        Methods:
        - get_queryset: Returns a queryset of DashboardData objects filtered by user ID if provided.
    """
    serializer_class = serializers.DashboardDataSerializer

    def get_queryset(self):
        """
            Retrieves the queryset of DashboardData objects, optionally filtering by user ID.

            The method checks if a `user_id` parameter is provided in the request. 
            If so, it filters the queryset based on the user ID. Handles cases where:
            - The user ID is not a valid integer.
            - No user exists with the given user ID.
            - No data is found for the given user ID.

            Args:
            - self: The instance of the class.

            Returns:
            - queryset: A queryset of DashboardData objects, potentially filtered by user ID.
            
            Raises:
            - ValidationError: If the `user_id` is not valid or if no data is found for the given user ID.
        """
        # Get all DashboardData objects
        queryset = models.DashboardData.objects.all()
        
        # Get the user_id parameter from the request
        user_id = self.request.query_params.get('user_id', None)
        
        # If user_id is provided and not empty
        if user_id is not None and user_id != '':
                    try:
                        # Convert user_id to an integer
                        user_id = int(user_id)
                    except ValueError:
                        # Raise an error if user_id is not a valid integer
                        raise ValidationError({"detail": "Invalid user ID. Please provide a valid integer."})
                    
                    # Check if a user with the given user_id exists
                    if not User.objects.filter(id=user_id).exists():
                        raise ValidationError({"detail": "No user found for the given user ID."})
                        
                    # Filter the queryset by the given user_id
                    queryset = queryset.filter(user_id=user_id)
                    
                    # If the filtered queryset is empty, raise an error
                    if not queryset.exists():
                        raise ValidationError({"detail": "No data found for the given user ID."})

        # Return the final queryset
        return queryset
        
        