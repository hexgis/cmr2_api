from django.utils.translation import ugettext_lazy as _

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import (
    response,
    permissions,
    views,
    status
)


class ChangePassword(views.APIView):
    """ChangePassword APIView."""

    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request):
        """Method to receive POST data from request.

        Args:
            oldPassword (str): old password
            newPassword (str): new password

        Returns:
            response: response data
        """

        old_password = request.data['oldPassword']
        new_password1 = request.data['newPassword1']
        user = request.user

        if user.check_password(old_password):
            user.set_password(new_password1)
            user.save()

            refresh = RefreshToken.for_user(user)

            return response.Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            message = _('Incorrect password.')

        error_response = response.Response(
            {'message': message}, status=status.HTTP_400_BAD_REQUEST
        )
        return error_response
