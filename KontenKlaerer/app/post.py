from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from .models import *
import os


def post_file_upload(request):
    print("FILES", request.FILES)
    file = request.FILES["file_upload"]
    file_name = default_storage.save(file.name, file)
    insert_data(file.name)
    os.remove("./data/" + file_name)
    return redirect("pageData")
