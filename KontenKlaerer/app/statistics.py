from .models import Data, Category
from django.db.models import Sum


def get_basic_statistics():
    data = Data.objects.all()

    # income without ignore categories
    income = data.filter(category__expense=False)
    income = income.filter(category__ignore=False)

    # expense without ignore categories
    expense = data.filter(category__expense=True)
    expense = expense.filter(category__ignore=False)

    # get categories without parent
    categories = data.filter(category__parent=None)

    # list of months
    periods = data.values("month", "year").distinct()
    # sort by year and month
    periods = sorted(periods, key=lambda month: month["year"])
    periods = sorted(periods, key=lambda month: month["month"])

    # iterate over months
    result = []
    for period in periods:
        year = period["year"]
        month = period["month"]

        # income all
        income_month = income.filter(
            month=period["month"], year=period["year"]).aggregate(total_amount=Sum('amount'))
        income_month["total_amount"] = int(income_month["total_amount"])

        # expense all
        expense_month = expense.filter(
            month=period["month"], year=period["year"]).aggregate(total_amount=Sum('amount'))
        expense_month["total_amount"] = int(expense_month["total_amount"])

        # balance
        balance = income_month["total_amount"] + expense_month["total_amount"]

        for category in categories:
            pass

        # append to result
        result.append({"year": year, "month": month, "income": income_month["total_amount"],
                       "expense": expense_month["total_amount"], "balance": balance})
    return result
