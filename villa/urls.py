from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

app_name = "villa"

urlpatterns = [
    path('properties/', views.PropertiesListView.as_view(), name='properties'),
    path('properties/detail/<int:pk>/', views.PropertyDetailView.as_view(), name='property_detail'),
    path('properties/category/<int:apartment_category_id>/', views.PropertiesListView.as_view(), name='category'),
    path('properties/page/<int:page>/', views.PropertiesListView.as_view(), name='paginator'),
    path('properties/category/<int:apartment_category_id>/page/<int:page>/', views.PropertiesListView.as_view(),
         name='paginator_filter'),
    path('contacts/', cache_page(30)(views.ContactView.as_view()), name='contacts'),
    path('baskets/add/<int:apartment_id>/', views.basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', views.basket_remove, name='basket_remove'),
]
