# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import permissions, status, views, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from forum.models import Category, Topic, Message
from forum.serializers import CategorySerializer, TopicSerializer, MessageSerializer
from users.models import User


class CategoryViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (IsAuthenticated,)

    # def perform_create(self, serializer):
    #     if serializer.is_valid():
    #         studentId = self.request.data.pop('student')
    #         student = User.objects.get(id=studentId)
    #         serializer.save(student=student, goal_created_by=self.request.user, **self.request.data)

    # def perform_update(self, serializer):
    #     if serializer.is_valid():
    #         serializer.save(goal_updated_by=self.request.user, **self.request.data)

class TopicViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            print 'SRD --- %s' %self.request.data
            user = self.request.user
            cat_id = self.request.data.pop('category_id')
            cat = Category.objects.get(id=cat_id)
            serializer.save(topic_category=cat, topic_created_by=user, **self.request.data)


class MessageViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            user = self.request.user
            topic_id = self.request.data.pop('topic_id')
            topic = Topic.objects.get(id=topic_id)
            serializer.save(message_user=user, message_topic=topic, **self.request.data)