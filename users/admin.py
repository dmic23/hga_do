from django.contrib import admin
from users.models import User, StudentGoal, StudentPracticeLog, StudentObjective, StudentWishList, StudentMaterial

class UserAdmin(admin.ModelAdmin):

    class Meta:
        model = User

    list_display = ('username', 'first_name', 'last_name', 'is_active', 'user_created', 'location', 'play_level',)
    list_filter = ('is_active', 'username', 'first_name', 'last_name', 'user_created', 'location', 'play_level', 'is_admin',)
    ordering = ('-user_created',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)

class StudentGoalAdmin(admin.ModelAdmin):

    class Meta:
        model = StudentGoal

    list_display = ('student', 'goal_target_date', 'goal_complete', 'goal_complete_date', 'goal',)
    list_filter = ('student', 'goal_target_date', 'goal_complete', 'goal_complete_date', 'goal_created',)
    ordering = ('-goal_created',)
    filter_horizontal = ()

admin.site.register(StudentGoal, StudentGoalAdmin)

class StudentObjectiveAdmin(admin.ModelAdmin):

    class Meta:
        model = StudentObjective

    list_display = ('student', 'objective_created', 'objective', 'objective_complete',)
    list_filter = ('student', 'objective_created', 'objective_complete', 'objective_complete_date',)
    ordering = ('-objective_created',)
    filter_horizontal = ()

admin.site.register(StudentObjective, StudentObjectiveAdmin)

class StudentPracticeLogAdmin(admin.ModelAdmin):

    class Meta:
        model = StudentPracticeLog

    list_display = ('student', 'practice_date', 'practice_category', 'practice_item', 'practice_time', 'practice_speed',)
    list_filter = ('student', 'practice_date', 'practice_category', 'practice_time', 'practice_speed', 'practice_item_created',)
    ordering = ('-practice_item_created',)
    filter_horizontal = ()

admin.site.register(StudentPracticeLog, StudentPracticeLogAdmin)

class StudentWishListAdmin(admin.ModelAdmin):

    class Meta:
        model = StudentWishList

    list_display = ('student', 'wish_item_created', 'wish_item', 'wish_item_complete', 'wish_item_complete_date',)
    list_filter = ('student', 'wish_item_created', 'wish_item', 'wish_item_complete',)
    filter_horizontal = ()

admin.site.register(StudentWishList, StudentWishListAdmin)

class StudentMaterialAdmin(admin.ModelAdmin):

    class Meta:
        model = StudentMaterial

    list_display = ('student', 'material_name', 'material_added', 'material_added_by',)
    list_filter = ('student', 'material_name', 'material_added', 'material_added_by',)
    ordering = ('-material_added',)
    filter_horizontal = ()

admin.site.register(StudentMaterial, StudentMaterialAdmin)



