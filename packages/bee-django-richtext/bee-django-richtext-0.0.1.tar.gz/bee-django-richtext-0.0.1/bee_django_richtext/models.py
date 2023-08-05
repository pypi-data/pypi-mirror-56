# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings


# textarea中上传的图片
class RichTextImage(models.Model):
    app_name = models.CharField(verbose_name='app名', max_length=180, null=True)
    model_name = models.CharField(verbose_name='model名', max_length=180, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    image = models.ImageField(verbose_name='图片', upload_to='bee_django_richtext/image')
    upload_at = models.DateTimeField(verbose_name='时间', auto_now_add=True)

    class Meta:
        db_table = 'bee_django_richtext_image'
