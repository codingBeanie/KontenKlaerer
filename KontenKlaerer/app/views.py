from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import default_storage
from .categories import *
from .dataframe import *
import os


def pageData(request):
    # handle file upload
    if request.method == "POST":
        file = request.FILES["file_upload"]
        file_name = default_storage.save(file.name, file)
        message = "Datei hochgeladen: " + file_name

    # no file uploaded / default state
    else:
        message = "Wählen Sie eine CSV-Datei für den Upload aus."

    # get a list of all csv files
    files = os.listdir("./files")

    # create data frame for data display
    data_frame = create_data_frame()
    num_rows = len(data_frame.index)

    # prepare context
    context = {"message": message, "files": files,
               "data_frame": data_frame, "num_rows": num_rows}
    return render(request, "pageData.html", context)


def delete_csv(request, file_name):
    os.remove("./files/" + file_name)
    return redirect("pageData")


def pageCategories(request):
    message = ""
    if request.method == "POST":
        # get data from form
        name = request.POST["name"]
        parent = request.POST["parent"]
        message = create_category(name, parent)

    categories_html = get_all_categories_html()
    categories = get_all_categories()
    context = {"categories_html": categories_html,
               "categories": categories, "message": message}
    return render(request, "pageCategories.html", context)


def delete_category(request, category_name):
    category = Category.objects.get(name=category_name)
    category.delete()
    return redirect("pageCategories")
