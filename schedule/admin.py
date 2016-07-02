from django.contrib import admin
from schedule.models import Course, CourseSchedule

class CourseAdmin(admin.ModelAdmin):

    class Meta:
        model = Course

    list_display = ('course_title', 'course_active',)
    ordering = ('course_title',)
    filter_horizontal = ()

    fieldsets = (
        ('Course Details', {'fields': ('course_title', 'course_subtitle', 'course_active',)}),
        ('Course Availability', {'fields': ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
            'course_start_time', 'course_end_time',)}),
        ('Stundent Requirements', {'fields': ('course_age_min', 'course_age_max', 'white', 'red', 'yellow', 'green',
            'blue', 'purple', 'brown', 'black', 'practice_min',)}),
        ('Course Extra', {'fields': ('max_student', 'course_credit', 'course_private', 'course_private_student', 'course_created_by',)}),
    )

admin.site.register(Course, CourseAdmin)

class CourseScheduleAdmin(admin.ModelAdmin):

    class Meta:
        model = CourseSchedule

    list_display = ('course', 'schedule_date',)
    ordering = ('course', 'schedule_date',)
    filter_horizontal = ()

admin.site.register(CourseSchedule, CourseScheduleAdmin)