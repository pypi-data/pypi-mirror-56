# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from .models import RichTextImage


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = RichTextImage
        fields = ['image']