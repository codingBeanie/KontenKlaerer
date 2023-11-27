from django.db import models
from datetime import datetime
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
import csv
import os
import uuid


class Data(models.Model):
    file_name = models.CharField(max_length=200)
    file_id = models.CharField(max_length=200)
    file_upload_time = models.CharField(max_length=200)
    date = models.DateField()
    month = models.IntegerField()
    year = models.IntegerField()
    paytype = models.CharField(max_length=200)
    payee = models.CharField(max_length=200)
    purpose = models.CharField(max_length=200)
    amount = models.FloatField()
    amount_display = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=200)
    expense = models.BooleanField(default=True)
    ignore = models.BooleanField(default=False)


class Assignment(models.Model):
    keyword = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

######################################################
#### File Management  ‚    ############################
######################################################


def post_file_upload(request):
    print("FILES", request.FILES)
    file = request.FILES["file_upload"]
    file_name = default_storage.save(file.name, file)
    insert_data(file.name)
    os.remove("./data/" + file_name)
    return redirect("pageData")

######################################################
#### Functions Data       ############################
######################################################


def insert_data(csv_name):
    # meta variables
    row_start = 7
    csv_file = "./data/" + csv_name
    unique_id = str(uuid.uuid4())
    time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    with open(csv_file, encoding="UTF-8") as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        for row in reader:
            if reader.line_num > row_start:
                if row[3] != "":
                    # create data object
                    data = Data(file_name=csv_name,
                                file_id=unique_id,
                                file_upload_time=time,
                                date=row[0][6:10] + "-" +
                                row[0][3:5] + "-" + row[0][0:2],
                                month=row[0][3:5],
                                year=row[0][6:10],
                                paytype=row[2],
                                payee=row[3],
                                purpose=row[4],
                                amount=row[7].replace(
                                    ".", "").replace(",", "."),
                                amount_display=row[7])
                data.save()
        apply_assignments()


def delete_data(request, file_id):
    data = Data.objects.filter(file_id=file_id)
    data.delete()
    return redirect("pageData")


######################################################
#### Functions Categories ############################
######################################################


def get_all_categories():
    query = Category.objects.all()
    categories = []
    for result in query:
        categories.append(result)
    return categories


""" def get_indentations(category):
    indentation = 0
    while category.parent != None:
        category = category.parent
        indentation += 1
    return indentation """


def get_categories_select(expense=True):
    query = Category.objects.filter(expense=expense)
    return query


""" def get_categories(expense=True):
    query = Category.objects.filter(parent=None, expense=expense)
    categories = []
    for result in query:
        identations = get_indentations(result)
        categories.append((result.name, identations, result.ignore))
        get_children(result, categories)
    return (categories) """


def get_categories(expense=True):
    query = Category.objects.filter(expense=expense)
    categories = []
    for result in query:
        categories.append(result)
    return (categories)


""" def get_children(parent, categories):
    query = Category.objects.filter(parent=parent)
    for result in query:
        identations = get_indentations(result)
        categories.append((result.name, identations))
        get_children(result, categories)
    return (categories) """


def create_category(request):
    # check if post in request has key "income" or "expense"
    if "name_expense" in request.POST:
        expense = True
        name = request.POST["name_expense"]
    else:
        expense = False
        name = request.POST["name_income"]

    if request.POST.get("ignore", False):
        ignore = True
    else:
        ignore = False

    # check if category already exists
    if not Category.objects.filter(name=name).exists():
        category = Category(name=name,
                            expense=expense, ignore=ignore)
        category.save()
    apply_assignments()
    return redirect("pageCategories")


def delete_category(request, category_name):
    category = Category.objects.get(name=category_name)
    category.delete()
    apply_assignments()
    return redirect("pageCategories")


######################################################
#### Functions Assignments ###########################
######################################################


def create_assignment(request):
    # get data from form
    keyword = request.POST["keyword"]
    category = request.POST["category"]
    # check if keyword already exists
    if not Assignment.objects.filter(keyword=keyword).exists():
        category = Category.objects.get(id=category)
        assignment = Assignment(keyword=keyword, category=category)
        assignment.save()
    apply_assignments()


def delete_assign(request, keyword):
    assignment = Assignment.objects.get(keyword=keyword)
    assignment.delete()
    apply_assignments()
    return redirect("pageAssign")


def apply_assignments():
    # set all categories to None
    data = Data.objects.all()
    for row in data:
        row.category = None
        row.save()

    # apply all assignments
    assignments = Assignment.objects.all()
    for assignment in assignments:
        type = assignment.category.expense
        # for purpose
        data = Data.objects.filter(purpose__icontains=assignment.keyword)
        for row in data:
            if type == True and row.amount < 0:
                row.category = assignment.category
                row.save()
            if type == False and row.amount > 0:
                row.category = assignment.category
                row.save()

        # for payee
        data = Data.objects.filter(payee__icontains=assignment.keyword)
        for row in data:
            if type == True and row.amount < 0:
                row.category = assignment.category
                row.save()
            if type == False and row.amount > 0:
                row.category = assignment.category
                row.save()
    return redirect("pageAssign")
