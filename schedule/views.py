# -*- coding: utf-8 -*-
import json
import datetime
import pytz
from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import permissions, status, views, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from schedule.models import Course, CourseSchedule
from schedule.serializers import CourseSerializer, CourseScheduleSerializer
from users.models import User, StudentPracticeLog
from users.tasks import send_schedule_course_cancel


class CourseViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def list(self, request, id=None):
        if self.request.user.is_admin:
            queryset = self.queryset.filter(course_active=True)
        else:
            queryset = self.queryset.filter(course_active=True).exclude(Q(course_private=True) & ~Q(course_private_student=self.request.user))
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)        
    

class CourseScheduleViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = CourseSchedule.objects.all()
    serializer_class = CourseScheduleSerializer

    def list(self, request, id=None):
        if self.request.user.is_admin:
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(student=self.request.user).exclude(schedule_date__lt=timezone.now())
        serializer = CourseScheduleSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        if serializer.is_valid():
            course_id = self.request.data.pop('course_id')
            course = Course.objects.get(id=course_id)
            user_id = self.request.data.pop('student_id')
            student = User.objects.get(id=user_id)
            serializer.save(course=course, student=student, user=self.request.user, **self.request.data)


class RemoveCourseScheduleViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = CourseSchedule.objects.all()
    serializer_class = CourseScheduleSerializer

    def perform_update(self, serializer):
        if serializer.is_valid():
            course_id = self.request.data.pop('course_id')
            sched_id = self.request.data.pop('schedule')
            user_id = self.request.data.pop('student_id')
            student = User.objects.get(id=user_id)
            instance = serializer.save()
            if student in instance.student.all():
                title = str(instance.course.course_title)
                date = str(instance.schedule_date)
                time = instance.schedule_start_time.strftime("%I:%M %p") 
                send_schedule_course_cancel.apply_async((student.id, title, date, time))
                instance.student.remove(student)
                start_date = datetime.datetime.combine(instance.schedule_date, instance.schedule_start_time)
                if start_date > datetime.datetime.now() + datetime.timedelta(hours=24):
                    student.user_credit = int(student.user_credit) + int(instance.course.course_credit)
                    student.save()
            if instance.student.count() == 0:
                course_schedule = CourseSchedule.objects.get(id=instance.id)
                course_schedule.delete()
            else:    
                instance.save()





