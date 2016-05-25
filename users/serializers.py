# -*- coding: utf-8 -*-
from datetime import date
from django.contrib.auth import update_session_auth_hash
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from rest_framework import serializers, status
# from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from users.models import User, StudentGoal, StudentPracticeLog, StudentObjective, StudentWishList, StudentMaterial

class StudentGoalSerializer(serializers.ModelSerializer):
    goal = serializers.CharField(required=False)
    student = serializers.CharField(required=False)
    goal_target_date = serializers.DateTimeField(format=None, input_formats=None, required=False)
    goal_complete_date = serializers.DateTimeField(format=None, input_formats=None, required=False)

    class Meta:
        model = StudentGoal
        fields = ('id', 'student', 'goal', 'goal_target_date', 'goal_complete', 'goal_complete_date', 'goal_notes', 'goal_created',)


class StudentPracticeLogSerializer(serializers.ModelSerializer):
    practice_category_display = serializers.SerializerMethodField(source='practice_category', required=False)
    practice_date = serializers.DateTimeField(format=None, input_formats=None, required=False)


    class Meta:
        model = StudentPracticeLog
        fields = ('id', 'student', 'practice_category', 'practice_category_display', 'practice_item', 'practice_time', 'practice_speed', 'practice_notes', 'practice_date', 'practice_item_created',)

    def get_practice_category_display(self,obj):
        return obj.get_practice_category_display();

class StudentObjectiveSerializer(serializers.ModelSerializer):
    objective = serializers.CharField(required=False)
    student = serializers.CharField(required=False)
    objective_complete_date = serializers.DateTimeField(format=None, input_formats=None, required=False)


    class Meta:
        model = StudentObjective
        fields = ('id', 'student', 'objective', 'objective_complete', 'objective_complete_date', 'objective_notes', 'objective_created',)


class StudentWishListSerializer(serializers.ModelSerializer):
    wish_item = serializers.CharField(required=False)
    student = serializers.CharField(required=False)

    class Meta:
        model = StudentWishList
        fields = ('id', 'student', 'wish_item', 'wish_item_complete', 'wish_item_complete_date', 'wish_item_notes', 'wish_item_created',)

class StudentMaterialSerializer(serializers.ModelSerializer):
    student = serializers.CharField(required=False)
    material_added = serializers.DateTimeField(format=None, input_formats=None, required=False)
    material_added_by = serializers.CharField(required=False)
    file = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = StudentMaterial
        fields = ('id', 'student', 'file', 'material_name', 'material_notes', 'material_added', 'material_added_by',)

class SimpleUserSerializer(serializers.ModelSerializer):

    recent_goal = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'is_active', 'user_pic', 'first_name', 'last_name', 'recent_goal', 'play_level')

    def get_recent_goal(self, obj):
        goal = StudentGoal.objects.filter(goal_complete=False).order_by('goal_target_date')
        return {'goal':goal[0].goal, 'goal_target_date':goal[0].goal_target_date}


def send_create_email(user):
    subject, from_email, to, bcc = 'Welcome to Hirsch Guitar Academy', 'hgatestacct@gmail.com', user.email, 'hgatestacct@gmail.com'
    text_content = 'Hi %s! Welcome to Hirsch Guitar Academy  Login here:' %user.first_name
    html_content = '<p>Hi %s!</hp><br/><p> Welcome to Hirsch Guitar Academy!</p><br/><p>Login here:</p>' %user.first_name
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], [bcc])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


class UserSerializer(serializers.ModelSerializer):
    play_level_display = serializers.CharField(source='get_play_level_display', required=False)
    email = serializers.CharField(required=False, allow_blank=True)
    user_pic = serializers.CharField(required=False, allow_blank=True)
    student_goal = StudentGoalSerializer(many=True, required=False)
    student_log = StudentPracticeLogSerializer(many=True, required=False)
    student_objective = StudentObjectiveSerializer(many=True, required=False)
    student_wishlist = StudentWishListSerializer(many=True, required=False)
    student_material = StudentMaterialSerializer(many=True, required=False)
    
    class Meta:
        model = User
        fields = ('id', 'user_created', 'user_updated', 'is_active', 'is_admin', 'is_staff', 'username', 'first_name', 'last_name', 'user_pic',
                'location', 'play_level', 'play_level_display', 'email', 'student_goal', 'student_log', 'student_objective', 'student_wishlist', 'student_material',)
        read_only_fields = ('id', 'user_created', 'is_admin', 'is_staff',)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        send_create_email(user)
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.location = validated_data.get('location', instance.location)
        instance.play_level = validated_data.get('play_level', instance.play_level)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.user_pic = validated_data.get('user_pic', instance.user_pic)
        instance.save()
        password = validated_data.get('password', None)
        confirm_password = validated_data.get('confirm_password', None)

        if password and confirm_password and password == confirm_password:
            instance.set_password(password)
            instance.save()

            update_session_auth_hash(self.context.get('request'), instance)

        return instance



