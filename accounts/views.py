import requests
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import QuerySet
from django.shortcuts import render, get_object_or_404
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response

from utils.helper import random_string
from .serializers import RegistrationSerializer, UsersSerializer, ChangePasswordSerializer, UpdateProfileSerializer
from rest_framework import permissions
from .models import Account
from oauth2_provider.models import get_application_model
from django.contrib.auth.models import User


def check_superuser(request):
    try:
        client_id = request.data['client_id']
    except:
        client_id = None

    try:
        client_secret = request.data['client_secret']
    except:
        client_secret = None

    if not client_id:
        # return Response({'message': 'Please provide client id.'}, status=HTTP_400_BAD_REQUEST)
        return 'Please provide client id.'

    if not client_secret:
        # return Response({'message': 'Please provide client secret.'}, status=HTTP_400_BAD_REQUEST)
        return 'Please provide client secret.'

    outh_app_model = get_application_model().objects.filter(client_id=client_id, client_secret=client_secret)
    if outh_app_model.count() <= 0:
        # return Response({'message': 'Invalid client id or client secret.'}, status=HTTP_400_BAD_REQUEST)
        return 'Invalid client id or client secret.'

    return None


class CreateAccount(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        err_msg = check_superuser(request)
        if err_msg is not None:
            return Response({'message': err_msg}, status=HTTP_400_BAD_REQUEST)

        request_data = request.data
        try:
            if request_data['username'] == '':
                request_data['username'] = random_string() + random_string()
        except KeyError:
            request_data['username'] = random_string() + random_string()

        reg_serializer = RegistrationSerializer(data=request_data)
        if reg_serializer.is_valid():
            new_user = reg_serializer.save()
            if new_user:
                current_domain = get_current_site(request).domain
                r = requests.post(f'http://{current_domain}/api/token', data={
                    'username': new_user.email,
                    'password': request.data['password'],
                    'client_id': request.data['client_id'],
                    'client_secret': request.data['client_secret'],
                    'grant_type': 'password'
                })
                return Response(r.json(), status=status.HTTP_201_CREATED)

        serializer_errors = reg_serializer._errors

        error_massage = {}
        for key in serializer_errors:
            error_massage[key] = serializer_errors[key][0]

        return Response({'message': error_massage}, status=HTTP_400_BAD_REQUEST)


class CustomLogin(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):

        try:
            client_id = request.data['client_id']
        except:
            client_id = None

        try:
            client_secret = request.data['client_secret']
        except:
            client_secret = None

        if not client_id:
            return Response({'message': 'Please provide client id.'}, status=HTTP_400_BAD_REQUEST)

        if not client_secret:
            return Response({'message': 'Please provide client secret.'}, status=HTTP_400_BAD_REQUEST)

        outh_app_model = get_application_model().objects.filter(client_id=client_id, client_secret=client_secret)
        if outh_app_model.count() <= 0:
            return Response({'message': 'Invalid client id or client secret.'}, status=HTTP_400_BAD_REQUEST)

        grant_type = request.data['grant_type']
        data = {
            'client_id': request.data['client_id'],
            'client_secret': request.data['client_secret'],
            'grant_type': grant_type
        }

        if grant_type == 'refresh_token':
            data['refresh_token'] = request.data['refresh_token']
        if grant_type == 'password':
            data['username'] = request.data['email']
            data['password'] = request.data['password']

        current_domain = get_current_site(request).domain
        r = requests.post(f'http://{current_domain}/api/token', data=data)
        if 'error_description' in r.json():
            return Response({'message': r.json()['error_description']}, status=HTTP_400_BAD_REQUEST)
        elif 'error' in r.json():
            return Response({'message': r.json()['error']}, status=HTTP_400_BAD_REQUEST)
        return Response(r.json(), status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):

        try:
            client_id = request.data['client_id']
        except:
            client_id = None

        try:
            client_secret = request.data['client_secret']
        except:
            client_secret = None

        if not client_id:
            return Response({'message': 'Please provide client id.'}, status=HTTP_400_BAD_REQUEST)

        if not client_secret:
            return Response({'message': 'Please provide client secret.'}, status=HTTP_400_BAD_REQUEST)

        outh_app_model = get_application_model().objects.filter(client_id=client_id, client_secret=client_secret)
        if outh_app_model.count() <= 0:
            return Response({'message': 'Invalid client id or client secret.'}, status=HTTP_400_BAD_REQUEST)

        if request.data['old_password'] == request.data['new_password']:
            return Response({"message": "Old password and new password cannot be same."}, status=status.HTTP_400_BAD_REQUEST)

        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"message": {"old_password": "Wrong password."}}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'message': 'Password updated successfully',
            }

            return Response(response, status=status.HTTP_200_OK)

        serializer_errors = serializer._errors
        error_massage = {}
        for key in serializer_errors:
            error_massage[key] = serializer_errors[key][0]
        return Response({"message": error_massage}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordRequest(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):

        try:
            client_id = request.data['client_id']
        except:
            client_id = None

        try:
            client_secret = request.data['client_secret']
        except:
            client_secret = None

        if not client_id:
            return Response({'message': 'Please provide client id.'}, status=HTTP_400_BAD_REQUEST)

        if not client_secret:
            return Response({'message': 'Please provide client secret.'}, status=HTTP_400_BAD_REQUEST)

        outh_app_model = get_application_model().objects.filter(client_id=client_id, client_secret=client_secret)
        if outh_app_model.count() <= 0:
            return Response({'message': 'Invalid client id or client secret.'}, status=HTTP_400_BAD_REQUEST)

        current_domain = get_current_site(request).domain
        r = requests.post(f'http://{current_domain}/api/password_reset/', data=request.data)
        print(r.json())
        print(r.status_code)
        if r.status_code != 200:
            error_message = {}
            for key in r.json():
                error_message[key] = r.json()[key][0]
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Check your email for token."}, status=status.HTTP_200_OK)


class ResetPasswordConfirm(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):

        try:
            client_id = request.data['client_id']
        except:
            client_id = None

        try:
            client_secret = request.data['client_secret']
        except:
            client_secret = None

        if not client_id:
            return Response({'message': 'Please provide client id.'}, status=HTTP_400_BAD_REQUEST)

        if not client_secret:
            return Response({'message': 'Please provide client secret.'}, status=HTTP_400_BAD_REQUEST)

        outh_app_model = get_application_model().objects.filter(client_id=client_id, client_secret=client_secret)
        if outh_app_model.count() <= 0:
            return Response({'message': 'Invalid client id or client secret.'}, status=HTTP_400_BAD_REQUEST)

        current_domain = get_current_site(request).domain
        r = requests.post(f'http://{current_domain}/api/password_reset/confirm/', data=request.data)
        print(r.json())
        print(r.status_code)
        if r.status_code != 200:
            error_message = {}
            for key in r.json():
                value = r.json()[key]
                if type(value) == list:
                    value = value[0]
                error_message[key] = value
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Password changed."}, status=status.HTTP_200_OK)


#


# class UpdateProfile(generics.UpdateAPIView):
#     serializer_class = UpdateProfileSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#     queryset = Account.objects.all()
#
#     # def get_queryset(self):
#     #     assert self.queryset is not None, (
#     #             "'%s' should either include a `queryset` attribute, "
#     #             "or override the `get_queryset()` method."
#     #             % self.__class__.__name__
#     #     )
#     #
#     #     queryset = self.queryset
#     #     if isinstance(queryset, QuerySet):
#     #         # Ensure queryset is re-evaluated on each request.
#     #         queryset = queryset.all()
#     #     return queryset
#
#     # def get_object(self):
#     #     queryset = self.get_queryset()
#     #     obj = get_object_or_404(queryset, user=self.request.user)
#     #     return obj
#
#     def get_object(self):
#         # queryset = self.get_queryset()
#         # obj = get_object_or_404(queryset, user=self.request.user.email)
#         obj = get_object_or_404(self.queryset, id=self.request.user.id)
#         # obj = Account.objects.get(user=self.request.user.email)
#         print('obj', obj)
#         return obj
#
#     def update(self, request, *args, **kwargs):
#         # self.queryset = Account.objects.get(uuid=request.user.uuid)
#         # self.queryset = self.get_object()
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         print(instance)
#         # serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer = UpdateProfileSerializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=False)
#         self.perform_update(serializer)
#         return Response(serializer.data)


class UpdateProfile(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        err_msg = check_superuser(request)
        if err_msg is not None:
            return Response({'message': err_msg}, status=HTTP_400_BAD_REQUEST)

        request_data = request.data
        # ins = Account.objects.filter(uuid=request.user.uuid)
        ins = Account.objects.get(uuid=request.user.uuid)

        serializer = UpdateProfileSerializer(instance=ins, data=request_data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            # if updated:
            return Response({"message": "updated"}, status=status.HTTP_201_CREATED)

        serializer_errors = serializer._errors

        error_massage = {}
        for key in serializer_errors:
            error_massage[key] = serializer_errors[key][0]

        return Response({'message': error_massage}, status=HTTP_400_BAD_REQUEST)




class AllUsers(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Account.objects.all()
    serializer_class = UsersSerializer


class CurrentUser(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = UsersSerializer(self.request.user)
        return Response(serializer.data)
