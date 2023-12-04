from .models import Data, Category
from django.db.models import Sum
import statistics


def get_statistics(expense=True, from_date=None, to_date=None):
    # get data
    data = Data.objects.all()
    result = []

    # filter entries (no null, no ignore, expense/income type)
    data = data.filter(category__isnull=False)
    data = data.filter(category__expense=expense)
    data = data.filter(category__ignore=False)

    # get periods
    periods = get_periods(from_date, to_date)

    # get unique categories
    categories = data.values("category").distinct()

    # iterate over categories and calculate the statistics for each category
    for category in categories:
        # set up
        subresult = []
        name = Category.objects.get(pk=category["category"]).name
        subresult.append(name)

        # starting/default values
        total = 0
        average = 0
        median = 0
        rows_data = 0

        # get sum for each period
        for period in periods:
            sum = data.filter(
                category=category["category"], month=period["month"], year=period["year"]).aggregate(Sum("amount"))
            if sum["amount__sum"] == None:
                sum["amount__sum"] = int(0)
            else:
                sum["amount__sum"] = int(sum["amount__sum"])
            subresult.append(sum["amount__sum"])
            rows_data += 1
            total += sum["amount__sum"]

        # calculate average and median
        average = int(total / rows_data)
        median = int(statistics.median(subresult[1:]))

        # append values to data
        subresult.append(total)
        subresult.append(average)
        subresult.append(median)

        result.append(subresult)

        # sort result by average
        if expense:
            result = sorted(
                result, key=lambda category: category[-2], reverse=False)
        else:
            result = sorted(
                result, key=lambda category: category[-2], reverse=True)

    # format all integers
    for subresult in result:
        for i in range(1, len(subresult)):
            subresult[i] = format(subresult[i], ",d").replace(",", ".")

    return result


def get_total(expense=True, from_date=None, to_date=None):
    # get data
    data = Data.objects.all()
    result = []

    # filter entries (no null, no ignore, expense/income type)
    data = data.filter(category__isnull=False)
    if expense != None:
        data = data.filter(category__expense=expense)
    data = data.filter(category__ignore=False)

    # get periods
    periods = get_periods(from_date, to_date)

    # starting/default values
    total = 0
    average = 0
    median = 0
    rows_data = 0

    # get sum for each period
    for period in periods:
        sum = data.filter(
            month=period["month"], year=period["year"]).aggregate(Sum("amount"))
        if sum["amount__sum"] == None:
            sum["amount__sum"] = int(0)
        else:
            sum["amount__sum"] = int(sum["amount__sum"])
        result.append(sum["amount__sum"])
        rows_data += 1
        total += sum["amount__sum"]

    # calculate average and median
    average = int(total / rows_data)
    median = int(statistics.median(result))

    # append values to data
    result.append(total)
    result.append(average)
    result.append(median)

    # format all integers
    for i in range(0, len(result)):
        result[i] = format(result[i], ",d").replace(",", ".")
    return result


def get_periods(from_date=None, to_date=None):
    data = Data.objects.all()
    if from_date == None or to_date == None:
        periods = data.values("month", "year").distinct()
    else:
        periods = data.filter(date__gte=from_date, date__lte=to_date).values(
            "month", "year").distinct()
    # sort by year and month
    periods = sorted(periods, key=lambda month: month["year"])
    periods = sorted(periods, key=lambda month: month["month"])
    return periods


def get_details(select_category=None, select_period=None):
    if select_category != None:
        category = Category.objects.get(name=select_category)
        data = Data.objects.all().filter(
            month=select_period["month"], year=select_period["year"], category=category)
        return data
