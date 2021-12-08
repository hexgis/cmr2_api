from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken


class ChangePassword(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        old_password = request.data['oldPassword']
        new_password1 = request.data['newPassword1']
        user = request.user

        if user.check_password(old_password):
            user.set_password(new_password1)
            user.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            message = 'Senha de usuário incorreta.'

        error_response = Response({'message': message}, status=400)
        return error_response
