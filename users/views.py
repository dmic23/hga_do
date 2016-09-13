# -*- coding: utf-8 -*-
import json
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.utils import timezone
from io import BytesIO
from rest_framework import permissions, status, views, viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from users.models import User,StudentGoal, StudentPracticeLog, StudentObjective, StudentWishList, StudentMaterial
from users.serializers import UserSerializer, LocationSerializer, StudentNoteSerializer, StudentGoalSerializer, StudentPracticeLogSerializer, StudentObjectiveSerializer, StudentWishListSerializer, StudentMaterialSerializer
from users.tasks import send_update_email


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(),)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user, **self.request.data)
        else:
            return Response({
                'status': 'Bad request',
                'message': 'Account could not be created with received data.'
            }, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        if serializer.is_valid():
            temp_file = self.request.data.pop('user_pic')
            file_dict = {}
            for i in self.request.data:
                if i != 'user_pic': 
                    item = self.request.data[i]
                    file_dict[i] = item
            for f in temp_file:
                file_dict['user_pic'] = f

            serializer.save(user=self.request.user, **file_dict)
    

class StudentGoalsViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = StudentGoal.objects.all()
    serializer_class = StudentGoalSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def perform_create(self, serializer):
        if serializer.is_valid():
            studentId = self.request.data.pop('student')
            student = User.objects.get(id=studentId)
            serializer.save(student=student, goal_created_by=self.request.user, **self.request.data)

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save(goal_updated_by=self.request.user, **self.request.data)


class StudentPracticeLogViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = StudentPracticeLog.objects.all()
    serializer_class = StudentPracticeLogSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, )

    def perform_create(self, serializer):
        if serializer.is_valid():
            studentId = self.request.data.pop('student')
            student = User.objects.get(id=studentId)
            serializer.save(student=student, practice_item_created_by=self.request.user, **self.request.data)

    def perform_update(self, serializer):
        if serializer.is_valid():
            studentId = self.request.data.pop('student')
            serializer.save(practice_item_updated_by=self.request.user, **self.request.data)


class StudentObjectiveViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = StudentObjective.objects.all()
    serializer_class = StudentObjectiveSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def perform_create(self, serializer):
        if serializer.is_valid():
            studentId = self.request.data.pop('student')
            student = User.objects.get(id=studentId)
            # check_priority(self.request.data.get('objective_priority'))
            send_update_email.delay(student.id);
            serializer.save(student=student, objective_created_by=self.request.user, **self.request.data)

    def perform_update(self, serializer):
        if serializer.is_valid():
            objective = StudentObjective.objects.get(id=self.request.data['id'])
            send_update_email.delay(objective.student.id);
            serializer.save(objective_updated_by=self.request.user, **self.request.data)

    # def update_priority(student, priority):
    #     print "OBJ PRIOR === %s"% obj
    #     try:
    #         objectives = StudentObjective.objects.filter(student=student)
    #         for objective in objectives:
    #             if objective.objective_priority == priority:
    #                 objective.objective_priority += 1
    #                 objective.save()
    #     except:
    #         pass

class StudentWishListViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = StudentWishList.objects.all()
    serializer_class = StudentWishListSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, )

    def perform_create(self, serializer):
        if serializer.is_valid():
            studentId = self.request.data.pop('student')
            student = User.objects.get(id=studentId)
            serializer.save(student=student, wish_item_created_by=self.request.user, **self.request.data)

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save(wish_item_updated_by=self.request.user, **self.request.data)


class StudentMaterialsViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = StudentMaterial.objects.all()
    serializer_class = StudentMaterialSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, )

    def perform_create(self, serializer):
        if serializer.is_valid():
            if 'file' in self.request.data:
                temp_file = self.request.data.pop('file')

            file_dict = {}
            for i in self.request.data:
                if i != 'file': 
                    item = self.request.data[i]
                    file_dict[i] = item
            for f in temp_file:
                file_dict['file'] = f
            studentId = file_dict.pop('student')
            student = User.objects.get(id=studentId)
            send_update_email.delay(student.id);
            serializer.save(student=student, material_added_by=self.request.user, **file_dict)

    def perform_update(self, serializer):
        if serializer.is_valid():
            if 'file' in self.request.data:
                temp_file = self.request.data.pop('file')

            file_dict = {}
            for i in self.request.data:
                item = self.request.data[i]
                file_dict[i] = item
            for f in temp_file:
                file_dict['file'] = f
            student_id = file_dict['id']
            material = StudentMaterial.objects.get(id=student_id)
            send_update_email.delay(material.student.id);
            serializer.save(**file_dict)


class LoginView(views.APIView):
    
    def post(self, request, format=None):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                serialized = UserSerializer(user)
                # jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                # jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                # print "SER DATA === %s" %serialized.data
                # payload = jwt_payload_handler(user)
                # print "PAYLOAD == %s" %payload
                # token = jwt_encode_handler(payload)
                # print "TOKEN === %s" %token
                # ip = get_ip(request)
                # log(
                #     user=user,
                #     company=user.user_company,
                #     not_action='user login',
                #     obj=user,
                #     notification=False,
                #     extra={
                #         'account_id':user.id,
                #         'account_first_name':user.first_name,
                #         'account_last_name':user.last_name,
                #         'login_ip':ip,
                #     }
                # )
                return Response(serialized.data)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username or password invalid'
            }, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(views.APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        user = self.request.user
        # ip = get_ip(request)
        # log(
        #     user=user,
        #     company=user.user_company,
        #     not_action='user logout',
        #     obj=user,
        #     notification=False,
        #     extra={
        #         'account_id':user.id,
        #         'account_first_name':user.first_name,
        #         'account_last_name':user.last_name,
        #         'login_ip':ip,
        #     }
        # )
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)