from django.db import models

from blog.models import Post  # 此处会有相对导入的问题，报红并不是出错，只是pycharm不知道路径
# from ..blog.models import Post  相对导入不行


class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    target = models.ForeignKey(Post, verbose_name='评论文章对象', on_delete=models.CASCADE)
    content = models.CharField(max_length=200, verbose_name='内容')
    nickname = models.CharField(max_length=20, verbose_name='昵称')
    website = models.URLField(verbose_name='网站')
    email = models.EmailField(verbose_name='邮箱')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS,
                                         verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '评论'
