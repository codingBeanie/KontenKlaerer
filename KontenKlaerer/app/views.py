from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import default_storage
from .models import *
from .post import *
from .statistics import *
import os


def pageData(request):
    # handle file upload
    if request.method == "POST":
        post_file_upload(request)

    # get a list of all csv files
    files = Data.objects.values(
        "file_name", "file_upload_time", "file_id").distinct()
    # create data frame for data display
    data = Data.objects.all()
    num_rows = data.count()

    # prepare context
    active_page = "data"
    context = {"files": files,
               "data": data, "num_rows": num_rows, "active_page": active_page}
    return render(request, "pageData.html", context)


def pageCategories(request):
    if request.method == "POST":
        create_category(request)

    categories_expense_tree = get_categories(expense=True)
    categories_expense_select = get_categories_select(expense=True)
    categories_income_tree = get_categories(expense=False)
    categories_income_select = get_categories_select(expense=False)

    active_page = "categories"

    context = {"categories_expense_tree": categories_expense_tree, "categories_income_tree": categories_income_tree,
               "categories_income_select": categories_income_select, "categories_expense_select": categories_expense_select, "active_page": active_page}
    return render(request, "pageCategories.html", context)


def pageAssign(request):
    if request.POST:
        create_assignment(request)

    data = Data.objects.filter(category=None)
    num_rows = data.count()

    assignments = Assignment.objects.all()
    categories = sorted(get_categories_selection(),
                        key=lambda category: category.name)

    active_page = "assign"
    context = {"active_page": active_page,
               "data": data, "num_rows": num_rows, "assignments": assignments, "categories": categories}
    return render(request, "pageAssign.html", context)


def pageStatistics(request):
    basic_statistics = get_basic_statistics()
    context = {"active_page": "statistics",
               "basic_statistics": basic_statistics}
    return render(request, "pageStatistics.html", context)
