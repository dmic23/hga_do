# -*- coding: utf-8 -*-
from __future__ import absolute_import
import datetime
# from datetime import date
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.utils import timezone
from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from schedule.models import CourseSchedule
from users.models import User, StudentPracticeLog


@shared_task
def send_create_email(user_id):
    user = User.objects.get(id=user_id)
    subject, from_email, to, bcc = 'Welcome to Hirsch Guitar Academy', 'hgatestacct@gmail.com', user.email, 'hgatestacct@gmail.com'
    text_content = 'Hi %s! Welcome to Hirsch Guitar Academy  You\'re account must be activated by Hirsch Guitar Academy' %user.first_name
    html_content = '<p>Hi %s!</hp><br/><p> Welcome to Hirsch Guitar Academy!</p><br/><p>You\'re account will be activated shortly on approval from Hirsch Guitar Acacdemy. You will receive a confirmation email once complete.</p><br/><p>Thank you,</p><br/><p>Hirsch Guitar Academy</p>' %user.first_name
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], [bcc])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def send_active_email(user_id):
    user = User.objects.get(id=user_id)
    subject, from_email, to, bcc = 'Hirsch Guitar Academy Activation', 'hgatestacct@gmail.com', user.email, 'hgatestacct@gmail.com'
    text_content = 'Hi %s! Welcome to Hirsch Guitar Academy  Login here: www.hirschguitaracademy.com' %user.first_name
    html_content = '<p>Hi %s!</hp><br/><p> Welcome to Hirsch Guitar Academy!</p><br/><p>You\'re account has been activated. Login here: <a href="hirschguitaracademy.com">hirschguitaracademy.com</a></p><br/><p>Thank you,</p><br/><p>Hirsch Guitar Academy</p>' %user.first_name
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], [bcc])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def send_update_email(user_id):
    user = User.objects.get(id=user_id)
    subject, from_email, to, bcc = 'Updates from Hirsch Guitar Academy', 'hgatestacct@gmail.com', user.email, 'hgatestacct@gmail.com'
    text_content = 'Hi %s!  You have new updates at Hirsch Guitar Academy. Login here: hirschguitaracademy.com Thank you, Hirsch Guitar Academy' %user.first_name
    html_content = '<p>Hi %s!</hp><br/><p>You have new updates at Hirsch Guitar Academy! Login here to see them: <a href="hirschguitaracademy.com">hirschguitaracademy.com</a></p><br/><p>Thank you,</p><br/><p>Hirsch Guitar Academy</p>' %user.first_name
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], [bcc])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def send_practice_reminder():
    prac_since = timezone.now() - timezone.timedelta(days=3, hours=5)
    user_practice = User.objects.exclude(student_log__practice_date__gt=prac_since).distinct() 
    
    for user in user_practice:
        subject, from_email, to, bcc = 'Practice Update from Hirsch Guitar Academy', 'hgatestacct@gmail.com', user.email, 'hgatestacct@gmail.com'
        text_content = 'Hi %s!  Practice makes perfect. It\'s been more than 3 days since your last practice. Login to add your practice. Login here: hirschguitaracademy.com Thank you, Hirsch Guitar Academy' %user.first_name
        html_content = '<p>Hi %s!</hp><br/><p>Practice makes perfect. It\'s been more than 3 days since your last practice. Login to add your practice! Login here: <a href="hirschguitaracademy.com">hirschguitaracademy.com</a></p><br/><p>Thank you,</p><br/><p>Hirsch Guitar Academy</p>' %user.first_name
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to], [bcc])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def send_schedule_course_confim(course_id, user_id):
    sched_course = CourseSchedule.objects.get(id=course_id)
    user = User.objects.get(id=user_id)

    subject, from_email, to, bcc = 'Class Scheduled with Hirsch Guitar Academy', 'hgatestacct@gmail.com', user.email, 'hgatestacct@gmail.com'
    text_content = 'Hi %s!  A class has been scheduled with Hirsch Guitar Academy. Scheduled class: %s on %s at %s. Login to view your class schedule. Login here: hirschguitaracademy.com Thank you, Hirsch Guitar Academy' %(user.first_name, sched_course.course.course_title, sched_course.schedule_date, sched_course.schedule_start_time.strftime("%I:%M %p"),)
    html_content = '<p>Hi %s!</p><br/><p>A class has been scheduled with Hirsch Guitar Academy. Scheduled class: %s on %s at %s. Login to view your class schedule. Login here: <a href="hirschguitaracademy.com">hirschguitaracademy.com</a></p><br/><p>Thank you,</p><br/><p>Hirsch Guitar Academy</p>' %(user.first_name, sched_course.course.course_title, sched_course.schedule_date, sched_course.schedule_start_time.strftime("%I:%M %p"),)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], [bcc])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def send_schedule_course_cancel(user_id, title, date, time):
    user = User.objects.get(id=user_id)

    subject, from_email, to, bcc = 'Class Cancelled with Hirsch Guitar Academy', 'hgatestacct@gmail.com', user.email, 'hgatestacct@gmail.com'
    text_content = 'Hi %s!  A class has been cancelled with Hirsch Guitar Academy. Cancelled class: %s on %s at %s. Login to view your class schedule. Login here: hirschguitaracademy.com Thank you, Hirsch Guitar Academy' %(user.first_name, title, date, time,)
    html_content = '<p>Hi %s!</p><br/><p>A class has been cancelled with Hirsch Guitar Academy. Cancelled class: %s on %s at %s. Login to view your class schedule. Login here: <a href="hirschguitaracademy.com">hirschguitaracademy.com</a></p><br/><p>Thank you,</p><br/><p>Hirsch Guitar Academy</p>' %(user.first_name, title, date, time,)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], [bcc])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def send_schedule_course_reminder():
    date_to = timezone.now() + timezone.timedelta(hours=21)
    sched_courses = CourseSchedule.objects.filter(schedule_date__range=[timezone.now(), date_to]).distinct()

    for course in sched_courses: 
        for user in course.student.all():
            subject, from_email, to, bcc = 'Upcoming Class with Hirsch Guitar Academy', 'hgatestacct@gmail.com', user.email, 'hgatestacct@gmail.com'
            text_content = 'Hi %s!  You have an upcoming Class scheduled with Hirsch Guitar Academy. Scheduled class: %s on %s at %s. Login to view your class schedule. Login here: hirschguitaracademy.com Thank you, Hirsch Guitar Academy' %(user.first_name, course.course.course_title, course.schedule_date, course.schedule_start_time.strftime("%I:%M %p"),)
            html_content = '<p>Hi %s!</p><br/><p>You have an upcoming Class scheduled with Hirsch Guitar Academy. Scheduled class: %s on %s at %s. Login to view your class schedule. Login here: <a href="hirschguitaracademy.com">hirschguitaracademy.com</a></p><br/><p>Thank you,</p><br/><p>Hirsch Guitar Academy</p>' %(user.first_name, course.course.course_title, course.schedule_date, course.schedule_start_time.strftime("%I:%M %p"),)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to], [bcc])
            msg.attach_alternative(html_content, "text/html")
            msg.send()


@shared_task
def update_recurring_credits():
    students = User.objects.filter(is_active=True)
    for student in students:
        student.user_credit = int(student.recurring_credit)
        student.save()


@shared_task
def update_recurring_schedule():
    today = datetime.date.today()
    next_scheduled_date = today + datetime.timedelta(days=7)
    daily_courses = CourseSchedule.objects.filter(schedule_date=today).exclude(schedule_recurring_user=None)
    for sched_course in daily_courses:
        for student in sched_course.schedule_recurring_user.all():
            # if int(student.user_credit) > int(sched_course.course.course_credit):
            new_course_sched, created = CourseSchedule.objects.get_or_create(course=sched_course.course, schedule_date=next_scheduled_date, schedule_start_time=sched_course.schedule_start_time, schedule_end_time=sched_course.schedule_end_time)
            new_course_sched.student.add(student)
            new_course_sched.schedule_recurring_user.add(student)
            new_course_sched.save()
            student.user_credit = int(student.user_credit) - int(sched_course.course.course_credit)
            student.save()

