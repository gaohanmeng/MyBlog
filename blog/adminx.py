import xadmin
from xadmin.layout import Row, Fieldset, Container
from xadmin.filters import manager
from xadmin.filters import RelatedFieldListFilter

# from django.contrib import admin
# from django.urls import reverse
from django.utils.html import format_html


from .models import Post, Category, Tag
from .adminforms import PostAdminForms
# from MyBlog.custom_site import custom_site
from MyBlog.base_admin import BaseOwnerAdmin


# class PostInline(admin.TabularInline):  # 获取不同的展示样式
#     fields = ('title', 'desc')
#     extra = 1
#     model = Post

class PostInline:
    form_layout = (
        Container(
            Row('title', 'desc')
        )
    )
    extra = 1
    model = Post


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    # inlines = [PostInline]
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    # fields = ('name', 'status', 'is_nav', 'owner')　owner字段有问题
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


# class CategoryOwnerFilter(admin.SimpleListFilter):
#     """自定义过滤器只展示当前用户分类"""
#     title = '分类过滤器'
#     parameter_name = 'owner_category'
#
#     def lookups(self, request, model_admin):
    #     return Category.objects.filter(owner=request.user).values_list('id', 'name')
    #
    # def queryset(self, request, queryset):
    #     category_id = self.value()
    #     if category_id:
    #         return queryset.filter(category_id=self.value())
    #     return queryset


class CategoryOwnerFilter(RelatedFieldListFilter):
    """自定义过滤器只展示当前用户分类"""
    @classmethod
    # 确认字段是否被当前过滤器处理
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    # 重写父类的__init__方法
    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        # 重新获取lookup_choices,根据owner过滤
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')


# 将自定义的过滤器注册到过滤器管理器中
manager.register(CategoryOwnerFilter, take_priority=True)


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForms
    list_display = (
        'title', 'category', 'status', 'created_time', 'operator'
    )
    list_display_links = None

    list_filter = ('category', 'tag')
    search_fields = ['title', 'category__name']

    #  actions_on_top = True
    actions_on_bottom = True

    #  save_on_top = True

    # fields = (
    #     'category',
    #     'title',
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )
    exclude = ('owner', )
    form_layout = (
        Fieldset(
            '基础信息',
            Row('title', ),
            'status',
            'is_title',
        ),
        Fieldset(
            '分区信息',
            'category',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'is_md',
            'content_ck',
            'content_md',
            'content',
        ),
        # Field('category', id='category'),
        # Field('tag', style='color： #333;', css_class=None, id='tag')
    )

    # fieldset = (
    #     ('抬头信息', {
    #         'description': '抬头信息描述',
    #         'fields': (
    #             'title', 'category', 'status',
    #         ),
    #     }),
    #     ('内容', {
    #         'fields': (
    #             'desc', 'content',
    #         ),
    #     }),
    #     ('添加标签', {
    #         'classes': ('collapse', ),
    #         'fields': ('tag', ),
    #     })
    # )
    filter_horizontal = ('tag', )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            # reverse('xadmin:blog_post_change', args=(obj.id,))
            self.model_admin_url('change', obj.id)
        )
    operator.short_description = '操作'
