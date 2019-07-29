from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html


from .models import Post, Category, Tag
from .adminforms import PostAdminForms
from MyBlog.custom_site import custom_site
from MyBlog.base_admin import BaseOwnerAdmin


class PostInline(admin.TabularInline):  # 获取不同的展示样式
    fields = ('title', 'desc')
    extra = 1
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline]
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    # fields = ('name', 'status', 'is_nav', 'owner')　owner字段有问题
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户分类"""
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForms
    list_display = [
        'title', 'category', 'status', 'created_time', 'operator'
    ]
    list_display_links = []

    list_filter = [CategoryOwnerFilter]  # 自定义分类过滤器进行分类
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
    # exclude = ('owner', )
    fieldsets = (
        ('抬头信息', {
            'description': '抬头信息描述',
            'fields': (
                'title', 'category', 'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc', 'content',
            ),
        }),
        ('添加标签', {
            'classes': ('collapse', ),
            'fields': ('tag', ),
        })
    )
    filter_horizontal = ('tag', )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'
