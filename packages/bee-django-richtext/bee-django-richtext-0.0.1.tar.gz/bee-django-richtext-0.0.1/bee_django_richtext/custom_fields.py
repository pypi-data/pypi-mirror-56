# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import inspect, os, re
from django.db import models
from django import forms
from django.conf import settings
from django.template import loader


# model field
class RichTextField(models.TextField):
    description = "RichTextField"

    # app_name：默认None
    # model_name：默认None
    # emotion：是否支持emoji表情，默认False
    # img：是否支持上传图片，默认False
    # undo_redo：是否支持撤销重做，默认False
    # text_min_length：文字最小长度，默认5，还未支持
    # image_max_size：图片最大尺寸，单位M，默认2M
    def __init__(self, app_name=None, model_name=None, emotion=False, img=False, undo_redo=False, text_min_length=5,
                 image_max_size=2, *args, **kwargs):
        self.app_name = app_name
        self.model_name = model_name
        self.emotion = emotion
        self.img = img
        self.undo_redo = undo_redo
        self.text_min_length = text_min_length
        self.image_max_size = image_max_size
        super(RichTextField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(RichTextField, self).deconstruct()
        if self.app_name:
            kwargs['app_name'] = self.app_name
        if self.model_name:
            kwargs['model_name'] = self.model_name
        kwargs['emotion'] = self.emotion
        kwargs['img'] = self.img
        kwargs['undo_redo'] = self.undo_redo
        kwargs['text_min_length'] = self.text_min_length
        kwargs['image_max_size'] = self.image_max_size

        return name, path, args, kwargs

    # 为模型字段指定表单字段
    def formfield(self, **kwargs):
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        # defaults = {'form_class': RichTextFormField, "image_max_size": self.image_max_size}
        defaults = {"widget": RichtextWidget(app_name=self.app_name, model_name=self.model_name, emotion=self.emotion,
                                             img=self.img, undo_redo=self.undo_redo,
                                             text_min_length=self.text_min_length, image_max_size=self.image_max_size)}
        defaults.update(kwargs)
        return super(RichTextField, self).formfield(**defaults)


# form field
class RichTextFormField(forms.CharField):
    def __init__(self, app_name=None, model_name=None, emotion=False, img=False, undo_redo=False, text_min_length=5,
                 image_max_size=2, *args, **kwargs):
        self.app_name = app_name
        self.model_name = model_name
        self.emotion = emotion
        self.img = img
        self.undo_redo = undo_redo
        self.text_min_length = text_min_length
        self.image_max_size = image_max_size
        defaults = {"widget": RichtextWidget(app_name=self.app_name, model_name=self.model_name, emotion=self.emotion,
                                             img=self.img, undo_redo=self.undo_redo,
                                             text_min_length=self.text_min_length, image_max_size=self.image_max_size)}
        defaults.update(kwargs)
        super(RichTextFormField, self).__init__(*args, **kwargs)

    # def to_python(self, value):
    #     "Returns a Unicode object."
    #     if value in self.empty_values:
    #         return self.empty_value
    #     value = force_text(value)
    #     if self.strip:
    #         value = value.strip()
    #     return value

    # def widget_attrs(self, widget):
    #     attrs = super(RichTextFormField, self).widget_attrs(widget)
    #     if self.image_max_size:
    #         # The HTML attribute is maxlength, not max_length.
    #         attrs['image_max_size'] = str(self.image_max_size)
    #     return attrs


# form field widget
class RichtextWidget(forms.Textarea):
    template_name = 'bee_django_richtext/widgets/richtext.html'

    def __init__(self, app_name=None, model_name=None, emotion=False, img=False, undo_redo=False, text_min_length=5,
                 image_max_size=2, attrs=None):
        # Use slightly better defaults than HTML's 20x2 box
        self.app_name = app_name
        self.model_name = model_name
        self.emotion = emotion
        self.img = img
        self.undo_redo = undo_redo
        self.text_min_length = text_min_length
        self.image_max_size = image_max_size
        default_attrs = {'cols': '40', 'rows': '10'}
        if attrs:
            default_attrs.update(attrs)
        super(RichtextWidget, self).__init__(default_attrs)

    def get_context(self, name, value, attrs):
        context = super(RichtextWidget, self).get_context(name, value, attrs)
        if self.image_max_size:
            context['value'] = value
            context['widget_name'] = name
            context['widget_id'] = attrs["id"]
            context['app_name'] = self.app_name
            context['model_name'] = self.model_name
            context['emotion'] = self.emotion
            context['img'] = self.img
            context['undo_redo'] = self.undo_redo
            context['text_min_length'] = self.text_min_length
            context['image_max_size'] = self.image_max_size
        return context

    # 引入需要的js、css文件
    class Media:
        css = {"all": ("bee_django_richtext/wangEditor/css/wangEditor.css",)}
        js = ("bee_django_richtext/wangEditor/js/wangEditor.js",)

    # 渲染你要展示字段的样式，通常返回html字符串
    # def render(self, name, value, attrs=None, renderer=None):
    #     output = loader.render_to_string(self.template_name,
    #                                      {'widget_name': name, "widget_id": attrs["id"],
    #                                       "image_max_size": self.image_max_size})
    #     return output
