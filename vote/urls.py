from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('results/question/<slug:question_id>/', views.question_results, name='question_results'),
]
