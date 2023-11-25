from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import default_storage
from .dataframe import *
from .models import *
import os


def pageData(request):
    # handle file upload
    if request.method == "POST":
        file = request.FILES["file_upload"]
        file_name = default_storage.save(file.name, file)
        insert_data(file.name)
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
    active_page = "data"
    context = {"message": message, "files": files,
               "data_frame": data_frame, "num_rows": num_rows, "active_page": active_page}
    return render(request, "pageData.html", context)


def delete_csv(request, file_name):
    os.remove("./files/" + file_name)
    return redirect("pageData")


def pageCategories(request):
    message = ""
    if request.method == "POST":
        # get data from form
        parent = request.POST["parent"]

        # check the type of input category
        if request.POST.get("name_income"):
            name = request.POST["name_income"]
            create_category(name, parent, False)
        else:
            name = request.POST["name_expense"]
            create_category(name, parent, True)

    categories_expense_tree = get_categories(expense=True)
    categories_expense_select = get_categories_select(expense=True)
    categories_income_tree = get_categories(expense=False)
    categories_income_select = get_categories_select(expense=False)

    active_page = "categories"

    context = {"categories_expense_tree": categories_expense_tree, "categories_income_tree": categories_income_tree,
               "categories_income_select": categories_income_select, "categories_expense_select": categories_expense_select, "active_page": active_page}
    return render(request, "pageCategories.html", context)


def delete_category(request, category_name):
    category = Category.objects.get(name=category_name)
    category.delete()
    return redirect("pageCategories")


def pageAssign(request):
    if request.POST:
        # get data from form
        keyword = request.POST["keyword"]
        category = request.POST["category"]
        # check if keyword already exists
        if not Assignment.objects.filter(keyword=keyword).exists():
            category = Category.objects.get(id=category)
            assignment = Assignment(keyword=keyword, category=category)
            assignment.save()

    data_frame = create_data_frame()
    data_frame = data_frame[data_frame.category.isnull()]
    num_rows = len(data_frame.index)

    assignments = Assignment.objects.all()
    categories = Category.objects.all()

    active_page = "assign"
    context = {"active_page": active_page,
               "data_frame": data_frame, "num_rows": num_rows, "assignments": assignments, "categories": categories}
    return render(request, "pageAssign.html", context)


def delete_assign(request, keyword):
    assignment = Assignment.objects.get(keyword=keyword)
    assignment.delete()
    return redirect("pageAssign")
