import xadmin

# from django.contrib import admin

from .models import Comment
# from MyBlog.custom_site import custom_site


@xadmin.sites.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
class CommentAdmin:
    list_display = ('target', 'nickname', 'content', 'website', 'created_time')
