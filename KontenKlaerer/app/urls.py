from django.urls import path
from . import views

urlpatterns = [
    path('', views.pageData, name='pageData'),
    path("deletecsv/<str:file_name>/", views.delete_csv, name='delete_csv'),
    path('categories/', views.pageCategories, name='pageCategories'),
    path("categories/deletecategory/<str:category_name>/",
         views.delete_category, name='delete_category'),
]
