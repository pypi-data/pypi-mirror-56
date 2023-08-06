#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bee'

from django.conf.urls import include, url
from . import views

app_name = 'bee_django_richtext'

urlpatterns = [
    # 图片上传
    url(r'^upload_image$', views.upload_image, name='upload_image'),

]
