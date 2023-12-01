from django.urls import path
from . import views, models

urlpatterns = [
    path('', views.pageData, name='pageData'),
    path("deletecsv/<str:file_id>/",
         models.delete_data, name='delete_csv'),
    path('categories/', views.pageCategories, name='pageCategories'),
    path("categories/deletecategory/<str:category_name>/",
         views.delete_category, name='delete_category'),
    path("assign", views.pageAssign, name='pageAssign'),
    path("deleteassign/<str:keyword>/",
         views.delete_assign, name="delete_assign"),
    path("statistics", views.pageStatistics, name="pageStatistics"),
    path("statistics/<str:select_category>-<int:select_period>/",
         views.pageStatistics, name="pageStatistics"),
]
