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
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from users.models import User, Location, StudentNote, StudentGoal, StudentPracticeLog, StudentObjective, StudentWishList, StudentMaterial, StudentLabel
from users.serializers import UserSerializer, SimpleUserSerializer, UserLeaderBoardSerializer, LocationSerializer, StudentNoteSerializer, StudentGoalSerializer, StudentPracticeLogSerializer, StudentObjectiveSerializer, StudentWishListSerializer, StudentMaterialSerializer, StudentLabelSerializer
from users.tasks import send_basic_email


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

class SimpleUserViewSet(viewsets.ModelViewSet):

    lookup_field = 'id'
    queryset = User.objects.all()
    serializer_class = SimpleUserSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)


class UserLeaderBoardViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = User.objects.all()
    serializer_class = UserLeaderBoardSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)


class LocationViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)  


class StudentNoteViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = StudentNote.objects.all()
    serializer_class = StudentNoteSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def perform_create(self, serializer):
        if serializer.is_valid():
            student_id = self.request.data.pop('student')
            student = User.objects.get(id=student_id)
            serializer.save(student=student, note_created_by=self.request.user, **self.request.data)
  
    def perform_update(self, serializer):
        if serializer.is_valid():
            print "SRD == %s"%self.request.data
            serializer.save(note_updated_by=self.request.user, **self.request.data)


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
            send_basic_email.delay(student.id, 'UPD')
            serializer.save(student=student, objective_created_by=self.request.user, **self.request.data)

    def perform_update(self, serializer):
        if serializer.is_valid():
            objective = StudentObjective.objects.get(id=self.request.data['id'])
            send_basic_email.delay(objective.student.id, 'UPD')
            serializer.save(objective_updated_by=self.request.user, **self.request.data)


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
    authentication_classes = (JSONWebTokenAuthentication,)
    parser_classes = (MultiPartParser, FormParser, JSONParser,)

    def perform_create(self, serializer):
        if serializer.is_valid():
            if 'file' in self.request.data:
                temp_file = self.request.data.pop('file')

            file_dict = {}
            group = []
            label = {}

            for k, v in self.request.data.iteritems():
                if 'group_student' in k:
                    group.append(v.encode("utf-8"))

                if k in ['material_notes', 'material_name']:
                    item = self.request.data.get(k)
                    file_dict[k] = item

                if 'student' in k:
                    student_id = v
                    student = User.objects.get(id=student_id)

                if 'material_label' in k:
                    label_key = k[18:-1].encode("utf-8")
                    label_index = int(k[15])
                    if label_index in label:
                        label[label_index][label_key] = v.encode("utf-8")
                    else:
                        label[label_index] = {label_key:v.encode("utf-8")}

            file_dict['material_added_by'] = self.request.user

            for f in temp_file:
                file_dict['file'] = f

            serializer.save(student=student, group=group, label=label, **file_dict)

    def perform_update(self, serializer):
        if serializer.is_valid():

            file_dict = {}
            group = []
            label_temp = {}
            label = []

            if 'file' in self.request.data:
                temp_file = self.request.data.pop('file')
                for f in temp_file:
                    file_dict['file'] = f

            for k, v in self.request.data.iteritems():
                if 'group_student' in k:
                    group.append(v)

                if 'material_label' in k:
                    label_key = k[18:-1].encode("utf-8")
                    label_index = int(k[15])
                    if label_index in label_temp:
                        label_temp[label_index][label_key] = v.encode("utf-8")
                    else:
                        label_temp[label_index] = {label_key:v.encode("utf-8")}
                
                if k != 'file' and 'group_student' not in k: 
                    item = self.request.data.get(k)
                    file_dict[k] = item
            
            for key,val in label_temp.iteritems():
                label.append(val)

            file_dict['material_updated_by'] = self.request.user
            serializer.save(group=group, label=label, **file_dict)

class StudentLabelViewSet(viewsets.ModelViewSet):

    lookup_field = 'id'
    queryset = StudentLabel.objects.all()
    serializer_class = StudentLabelSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)


class LoginView(views.APIView):

    def post(self, request, format=None):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                serialized = UserSerializer(user)
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
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):

        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)
