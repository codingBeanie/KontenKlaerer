from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .statistics import *
import os
from datetime import date
from django.core.cache import cache


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


def pageStatistics(request, select_category=None, select_period=2):
    # get min and max period
    periods = get_periods()
    print(periods[0])
    date_from = str(periods[0]["year"]) + \
        "-" + str(periods[0]["month"]) + "-01"
    date_to = str(periods[-1]["year"]) + \
        "-" + str(periods[-1]["month"]) + "-01"

    # get data
    income = get_statistics(
        expense=False, from_date=date_from, to_date=date_to)
    income_subtotal = get_total(
        expense=False, from_date=date_from, to_date=date_to)
    expense = get_statistics(
        expense=True, from_date=date_from, to_date=date_to)
    expense_subtotal = get_total(
        expense=True, from_date=date_from, to_date=date_to)
    total = get_total(expense=None, from_date=date_from,
                      to_date=date_to)
    row_start_stats = len(periods) + 1

    selection = {"category": select_category, "period": select_period}
    select_category = select_category
    select_period = periods[select_period - 2]
    detail_statistics = get_details(select_category, select_period)
    print(income)

    # prepare context
    context = {"active_page": "statistics", "row_start_stats": row_start_stats,
               "income": income, "expense": expense, "income_subtotal": income_subtotal,
               "expense_subtotal": expense_subtotal, "total": total, "periods": periods,
               "select_category": select_category, "select_period": select_period,
               "detail_statistics": detail_statistics, "selection": selection, "select_period_from": date_from,
               "select_period_to": date_to, "message": "Dieses Feature funktioniert gerade nicht!"}
    return render(request, "pageStatistics.html", context)
