# -*- coding: utf-8 -*-
from django.contrib.auth import update_session_auth_hash
from datetime import date
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.response import Response
from forum.models import Category, Topic, Message
from users.serializers import SimpleUserSerializer


class MessageSerializer(serializers.ModelSerializer):
    message_user = SimpleUserSerializer(required=False)
    message_topic = serializers.CharField(required=False)

    class Meta:
        model = Message
        fields = ('id', 'message_topic', 'message_user', 'message', 'message_created', 'message_visible',)


class TopicSerializer(serializers.ModelSerializer):
    topic_message = MessageSerializer(many=True, required=False)
    topic_category = serializers.CharField(required=False)
    topic_created_by = serializers.CharField(required=False)

    class Meta:
        model = Topic
        fields = ('id', 'topic_category', 'topic', 'topic_created_by', 'topic_created', 'topic_message',)

    def create(self, validated_data):
        print "VAL DATA === %s" %validated_data.get('topic_created_by')
        user = validated_data.get('topic_created_by')
        if 'message' in validated_data:
            msg = validated_data.pop('message')
            print "MSG == %s" %msg
        else:
            msg = None

        topic = Topic.objects.create(**validated_data)
        topic.save()

        if msg:
            print "VAL DATA 2 === %s" %validated_data
            new_msg = Message.objects.create(message_topic=topic, message_user=user, message=msg)
            new_msg.save()
            print "New MSG == %s" %new_msg
        return topic


class CategorySerializer(serializers.ModelSerializer):
    category_topic = TopicSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'category', 'category_created', 'category_created_by', 'category_topic',)

