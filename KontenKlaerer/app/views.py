from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .statistics import *
import os


def pageData(request):
    # handle file upload
    if request.method == "POST":
        post_file_upload(request)

    # get data
    files = Data.objects.values(
        "file_name", "file_upload_time", "file_id").distinct()
    data = Data.objects.all()
    num_rows = data.count()

    # prepare context
    active_page = "data"
    context = {"files": files,
               "data": data, "num_rows": num_rows, "active_page": active_page}
    return render(request, "pageData.html", context)


def pageCategories(request):
    # handle post request
    if request.method == "POST":
        create_category(request)

    # get data
    categories_expense_tree = get_categories(expense=True)
    categories_income_tree = get_categories(expense=False)

    # prepare context
    active_page = "categories"
    context = {"categories_expense_tree": categories_expense_tree, "categories_income_tree": categories_income_tree,
               "active_page": active_page}
    return render(request, "pageCategories.html", context)


def pageAssign(request):
    # handle post request
    if request.POST:
        create_assignment(request)

    # get data
    data = Data.objects.filter(category=None)
    num_rows = data.count()
    assignments = Assignment.objects.all()
    categories = sorted(get_all_categories(),
                        key=lambda category: category.name)

    # prepare context
    active_page = "assign"
    context = {"active_page": active_page,
               "data": data, "num_rows": num_rows, "assignments": assignments, "categories": categories}
    return render(request, "pageAssign.html", context)


def pageStatistics(request):
    # get data
    basic_statistics = get_basic_statistics()

    # prepare context
    context = {"active_page": "statistics",
               "basic_statistics": basic_statistics}
    return render(request, "pageStatistics.html", context)
