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
    periods_all = get_periods()
    period_all_range = {"period_from": str(periods_all[0]["month"]) + "-" + str(
        periods_all[0]["year"]), "period_to": str(periods_all[-1]["month"]) + "-" + str(periods_all[-1]["year"])}

    # check cache
    if cache.get("periods") != None:
        periods = cache.get("periods")
        period_range = {"period_from": str(periods[0]["month"]) + "-" + str(
            periods[0]["year"]), "period_to": str(periods[-1]["month"]) + "-" + str(periods[-1]["year"])}
    else:
        periods = periods_all
        period_range = period_all_range

    # get input periods or default to min/max
    period_from = request.POST.get(
        "period_from", period_range["period_from"])
    date_from = period_from.split("-")
    date_from = date(int(date_from[1]), int(date_from[0]), 1)
    period_to = request.POST.get("period_to", period_range["period_to"])
    date_to = period_to.split("-")
    date_to = date(int(date_to[1]), int(date_to[0]), 1)

    select_period_from = period_from
    select_period_to = period_to
    message = ""

    # check if selection is valid, else set to min/max
    if date_from > date_to:
        select_period_from = period_all_range["period_from"]
        select_period_to = period_all_range["period_to"]
        message = "Das Von-Datum darf nicht nach dem Bis-Datum liegen."
    if date_from < date(int(periods_all[0]["year"]), int(periods_all[0]["month"]), 1):
        select_period_from = period_all_range["period_from"]
        message = "Das Von-Datum darf nicht vor dem ersten verfügbaren Monat liegen."
    if date_to > date(int(periods_all[-1]["year"]), int(periods_all[-1]["month"]), 1):
        select_period_to = period_all_range["period_to"]
        message = "Das Bis-Datum darf nicht nach dem letzten verfügbaren Monat liegen."

    final_date_from = select_period_from.split("-")
    final_date_from = date(int(final_date_from[1]), int(final_date_from[0]), 1)
    final_date_to = select_period_to.split("-")
    final_date_to = date(int(final_date_to[1]), int(final_date_to[0]), 1)
    periods = get_periods(final_date_from, final_date_to)

    # store to cache
    cache.set("periods", periods)

    # get data
    income = get_statistics(
        expense=False, from_date=final_date_from, to_date=final_date_to)
    income_subtotal = get_total(
        expense=False, from_date=final_date_from, to_date=final_date_to)
    expense = get_statistics(
        expense=True, from_date=final_date_from, to_date=final_date_to)
    expense_subtotal = get_total(
        expense=True, from_date=final_date_from, to_date=final_date_to)
    total = get_total(expense=None, from_date=final_date_from,
                      to_date=final_date_to)
    row_start_stats = len(periods) + 1

    selection = {"category": select_category, "period": select_period}
    select_category = select_category
    select_period = periods[select_period - 2]
    detail_statistics = get_details(select_category, select_period)

    # prepare context
    context = {"active_page": "statistics", "row_start_stats": row_start_stats,
               "income": income, "expense": expense, "income_subtotal": income_subtotal,
               "expense_subtotal": expense_subtotal, "total": total, "periods": periods,
               "select_category": select_category, "select_period": select_period,
               "detail_statistics": detail_statistics, "selection": selection, "select_period_from": select_period_from,
               "select_period_to": select_period_to, "message": message}
    return render(request, "pageStatistics.html", context)
