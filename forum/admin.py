from django.contrib import admin
from forum.models import Category, Topic, Message

class CategoryAdmin(admin.ModelAdmin):

    class Meta:
        model = Category

    list_display = ('category',)
    ordering = ('category',)
    filter_horizontal = ()

admin.site.register(Category, CategoryAdmin)

class TopicAdmin(admin.ModelAdmin):

    class Meta:
        model = Topic

admin.site.register(Topic, TopicAdmin)

class MessageAdmin(admin.ModelAdmin):

    class Meta:
        model = Message

admin.site.register(Message, MessageAdmin)