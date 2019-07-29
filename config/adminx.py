import xadmin
from xadmin.layout import Row, Fieldset

# from django.contrib import admin

from .models import SideBar, Link
# from MyBlog.custom_site import custom_site
from MyBlog.base_admin import BaseOwnerAdmin


@xadmin.sites.register(Link)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'created_time')
    fields = ('title', 'href', 'status', 'weight')
    # form_layout = (
    #     Fieldset(
    #         'title', 'href', 'status', 'weight'),
    #     )

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin, self).save_modle(request, obj, form, change)


@xadmin.sites.register(SideBar)
class SideBarAdmin(BaseOwnerAdmin):
    list_display = ('title', 'display_type', 'content', 'created_time')
    # fields = ('title', 'display_type', 'content')
    form_layout = (
        Fieldset(
            'title', 'display_type', 'content'
        ),
    )

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SideBarAdmin, self).save_model(request, obj, form, change)
