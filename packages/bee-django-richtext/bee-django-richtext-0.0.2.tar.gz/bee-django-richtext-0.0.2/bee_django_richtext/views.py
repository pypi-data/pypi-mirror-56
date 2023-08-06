# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Create your views here.


from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse

from .forms import UploadImageForm


@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        file = request.FILES.get("image")
        app_name = request.POST.get("app_name")
        model_name = request.POST.get("model_name")
        max_size = request.POST.get("max_size")
        if not max_size:
            max_size = 2
        max_size = int(max_size) * 1024 * 1024
        if file.size > max_size:
            return HttpResponse("error|图片大小超过" + max_size.__str__() + "M")

        # 保存图片。用户上传的图片，与用户的对应关系也保存到数据库中
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            user_image = form.save(commit=False)
            if request.user.is_authenticated:
                user_image.user = request.user
            if app_name:
                user_image.app_name = app_name
            if model_name:
                user_image.model_name = model_name
            user_image.save()
            return HttpResponse(user_image.image.url)
        else:
            return HttpResponse("error|文件存储错误")
    else:
        return HttpResponse("error|请求错误")
