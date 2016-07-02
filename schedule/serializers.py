# -*- coding: utf-8 -*-
from datetime import date
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.response import Response
from schedule.models import Course, CourseSchedule
from users.serializers import UserSerializer
from users.tasks import send_schedule_course_confim

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('id', 'course_title', 'course_subtitle', 'course_length',  'course_start_time', 'course_end_time','course_created', 'course_created_by', 'course_age_min', 'course_age_max',
        	'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'practice_min', 'course_credit', 'max_student', 'course_private', 'course_private_student',
        	'white', 'red', 'yellow', 'green', 'blue', 'purple', 'brown', 'black',)


class CourseScheduleSerializer(serializers.ModelSerializer):
	course = CourseSerializer(required=False)
	student = UserSerializer(many=True, required=False)
	schedule_created_by = serializers.CharField(required=False)

	class Meta:
		model = CourseSchedule
		fields = ('id', 'course', 'student', 'schedule_date', 'schedule_start_time', 'schedule_end_time', 'schedule_created', 'schedule_created_by', 'schedule_updated', 'schedule_updated_by',)

	def create(self, validated_data):
		student = validated_data.pop('student')
		user = validated_data.pop('user')
		course_schedule, created = CourseSchedule.objects.get_or_create(**validated_data)
		if course_schedule.student.count() < int(course_schedule.course.max_student):
			course_schedule.student.add(student)
			course_schedule.save()
			send_schedule_course_confim.delay(course_schedule.id, student.id)
		return course_schedule