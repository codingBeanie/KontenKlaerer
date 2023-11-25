from django.db import models
import csv
import os


class Data(models.Model):
    file_name = models.CharField(max_length=200)
    file_timestamp = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    month = models.IntegerField()
    year = models.IntegerField()
    paytype = models.CharField(max_length=200)
    payee = models.CharField(max_length=200)
    purpose = models.CharField(max_length=200)
    amount = models.FloatField()
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, null=True, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
    expense = models.BooleanField(default=True)


class Assignment(models.Model):
    keyword = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


######################################################
#### Functions Data       ############################
######################################################
def insert_data(csv_name):
    # meta variables
    row_start = 7
    csv_file = "./files/" + csv_name
    with open(csv_file, encoding="UTF-8") as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        for row in reader:
            if reader.line_num > row_start:
                # create data object
                data = Data(file_name=csv_name,
                            date=row[0][6:10] + "-" +
                            row[0][3:5] + "-" + row[0][0:2],
                            month=row[0][3:5],
                            year=row[0][6:10],
                            paytype=row[2],
                            payee=row[3],
                            purpose=row[4],
                            amount=row[7].replace(".", "").replace(",", "."))
                data.save()


######################################################
#### Functions Categories ############################
######################################################


def get_all_categories():
    query = Category.objects.all()
    categories = []
    for result in query:
        categories.append(result)
    return categories


def get_indentations(category):
    indentation = 0
    while category.parent != None:
        category = category.parent
        indentation += 1
    return indentation


def get_categories_select(expense=True):
    query = Category.objects.filter(expense=expense)
    return query


def get_categories(expense=True):
    query = Category.objects.filter(parent=None, expense=expense)
    categories = []
    for result in query:
        identations = get_indentations(result)
        categories.append((result.name, identations))
        get_children(result, categories)
    return (categories)


def get_children(parent, categories):
    query = Category.objects.filter(parent=parent)
    for result in query:
        identations = get_indentations(result)
        categories.append((result.name, identations))
        get_children(result, categories)
    return (categories)


def create_category(name, parent_id, expense):
    # case ategory already exists
    if Category.objects.filter(name=name).exists():
        return ("Kategorie existiert bereits")

    # case has valid parent
    if parent_id != "0":
        parent = Category.objects.get(id=parent_id)
        category = Category(name=name, parent=parent, expense=expense)
        category.save()
        return ("Erfolgreich gespeichert")

    # case has no parent
    if parent_id == "0":
        category = Category(name=name, expense=expense)
        category.save()
        return ("Erfolgreich gespeichert")

######################################################
#### Functions Assignments ###########################
######################################################
