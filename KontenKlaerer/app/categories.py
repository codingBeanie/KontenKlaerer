from .models import Category
from django.utils.safestring import mark_safe


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


def get_all_categories_html():
    query = Category.objects.filter(parent=None)
    categories = []
    for result in query:
        identations = get_indentations(result)
        categories.append((result.name, identations))
        get_children_html(result, categories)
    return (categories)


def get_children_html(parent, categories):
    query = Category.objects.filter(parent=parent)
    for result in query:
        identations = get_indentations(result)
        categories.append((result.name, identations))
        get_children_html(result, categories)
    return (categories)


def create_category(name, parent_id):
    # case ategory already exists
    if Category.objects.filter(name=name).exists():
        return ("Kategorie existiert bereits")

    # case has valid parent
    if parent_id != "0":
        parent = Category.objects.get(id=parent_id)
        category = Category(name=name, parent=parent)
        category.save()
        return ("Erfolgreich gespeichert")

    # case has no parent
    if parent_id == "0":
        category = Category(name=name)
        category.save()
        return ("Erfolgreich gespeichert")
