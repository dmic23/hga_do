# -*- coding: utf-8 -*-
from django.contrib import admin
from forum.models import Category, Topic, ForumMessage, MessageFile

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

class MessageFileInLine(admin.StackedInline):
    model = MessageFile
    extra = 0

class ForumMessageAdmin(admin.ModelAdmin):

    inlines = [
        MessageFileInLine,
    ]

admin.site.register(ForumMessage, ForumMessageAdmin)
