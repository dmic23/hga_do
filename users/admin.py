from django.contrib import admin
from users.models import User, StudentGoal, StudentPracticeLog, StudentObjective, StudentWishList, StudentMaterial

class StudentGoalInline(admin.StackedInline):
    model = StudentGoal
    extra = 0
    fk_name = 'student'

class StudentPracticeLogInline(admin.StackedInline):
    model = StudentPracticeLog
    extra = 0
    fk_name = 'student'

class StudentObjectiveInline(admin.StackedInline):
    model = StudentObjective
    extra = 0
    fk_name = 'student'

class StudentWishListInline(admin.StackedInline):
    model = StudentWishList
    extra = 0
    fk_name = 'student'

class StudentMaterialInline(admin.StackedInline):
    model = StudentMaterial
    extra = 0
    fk_name = 'student'

class UserAdmin(admin.ModelAdmin):

    inlines = [
        StudentGoalInline,
        StudentPracticeLogInline,
        StudentObjectiveInline,
        StudentWishListInline,
        StudentMaterialInline,
    ]

    list_display = ('username', 'first_name', 'last_name', 'user_created',)
    list_filter = ('username', 'first_name', 'last_name', 'user_created',)
    ordering = ('-user_created',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)

