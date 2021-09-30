from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from .serializers import CourseSerializer
from ..models import Subject, Course, StudentList
from .serializers import SubjectSerializer, StudentListSerializer, CourseWithContentsSerializer
from .permissions import IsEnrolled

from utils.helper import get_user_uuid


class StudentListCreateView(generics.ListCreateAPIView):
    serializer_class = StudentListSerializer

    # permission_classes = [permissions.AllowAny]

    # def get_queryset(self):
    #     return StudentList.objects.all()

    def create(self, request, *args, **kwargs):
        token = request.headers.get('token')
        if not token:
            return Response({'success': False, 'message': 'Please provide user token.'}, status=HTTP_400_BAD_REQUEST)
        user_uuid = get_user_uuid(token)
        if not user_uuid:
            return Response({'success': False, 'message': 'User cannot be validated.'}, status=HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={'uuid': user_uuid})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


# class CourseEnrollView(APIView):
#
#     def post(self, request, pk, format=None):
#         token = request.headers.get('token')
#         if not token:
#             return Response({'success': False, 'message': 'Please provide user token.'}, status=HTTP_400_BAD_REQUEST)
#         user_uuid = get_user_uuid(token)
#         if not user_uuid:
#             return Response({'success': False, 'message': 'User cannot be validated.'}, status=HTTP_400_BAD_REQUEST)
#
#         course = get_object_or_404(Course, pk=pk)
#         student = get_object_or_404(StudentList, uuid=user_uuid)
#         course.students.add(student)
#         return Response({'enrolled': True})


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        return Course.objects.all()

    def list(self, request):
        token = request.headers.get('token')
        if not token:
            return Response({'success': False, 'message': 'Please provide user token.'}, status=HTTP_400_BAD_REQUEST)
        user_uuid = get_user_uuid(token)
        if not user_uuid:
            return Response({'success': False, 'message': 'User cannot be validated.'}, status=HTTP_400_BAD_REQUEST)

        courses = Course.objects.all()
        courses_serializer = CourseSerializer(courses, many=True)
        data = courses_serializer.data
        return Response({'success': True, 'data': data}, status=HTTP_200_OK)

    def retrieve(self, request, pk=None):
        token = request.headers.get('token')
        if not token:
            return Response({'success': False, 'message': 'Please provide user token.'}, status=HTTP_400_BAD_REQUEST)
        user_uuid = get_user_uuid(token)
        if not user_uuid:
            return Response({'success': False, 'message': 'User cannot be validated.'}, status=HTTP_400_BAD_REQUEST)

        # course = get_object_or_404(Course, pk=pk)
        # course_serializer = CourseSerializer(course)
        # data = course_serializer.data
        # return Response({'success': True, 'data': data}, status=HTTP_200_OK)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def enroll(self, request, *args, **kwargs):
        token = request.headers.get('token')
        if not token:
            return Response({'success': False, 'message': 'Please provide user token.'}, status=HTTP_400_BAD_REQUEST)
        user_uuid = get_user_uuid(token)
        if not user_uuid:
            return Response({'success': False, 'message': 'User cannot be validated.'}, status=HTTP_400_BAD_REQUEST)

        student = get_object_or_404(StudentList, uuid=user_uuid)

        course = self.get_object()
        course.students.add(student)
        return Response({'enrolled': True})

    @action(detail=True, methods=['get'], serializer_class=CourseWithContentsSerializer, permission_classes=[IsEnrolled])
    # @action(detail=True, methods=['get'], serializer_class=CourseWithContentsSerializer)
    def contents(self, request, pk=None, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
        # token = request.headers.get('token')
        # if not token:
        #     return Response({'success': False, 'message': 'Please provide user token.'}, status=HTTP_400_BAD_REQUEST)
        # user_uuid = get_user_uuid(token)
        # if not user_uuid:
        #     return Response({'success': False, 'message': 'User cannot be validated.'}, status=HTTP_400_BAD_REQUEST)
        #
        # course = get_object_or_404(Course, pk=pk)
        # course_serializer = CourseWithContentsSerializer(course)
        # # print('course_serializer:', course_serializer)
        # data = course_serializer.data
        # print('data:', data)
        # return Response({'success': True, 'data': data}, status=HTTP_200_OK)
