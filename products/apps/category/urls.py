from django.urls import path

from .views import *

urlpatterns = [
    path('list', ListCategoriesView.as_view()),
    path('list/primary/', PrimaryCategoriesView.as_view()),
    path('list/secondary/<slug>/', SubCategoriesView.as_view()),
    path('list/tertiary/<str:slug>/', TertiaryCategoriesView.as_view()),

    path('details/<slug>', CategoryDetailView.as_view()),
    path('create', CategoryCreateView.as_view()),
    path('edit', CategoryEditView.as_view()),
    path('delete', CategoryDeleteView.as_view()),
    path('popular/', ListPopularTopicsView.as_view()),
]
