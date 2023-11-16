from django.urls import path
from rest_framework import routers

from vacancies.views import SkillViewSet, LikeVacancyView
from vacancies import views
from vacancies.views import VacancyView, VacancyDetailView, VacancyCreateView, VacancyUpdateView, VacancyDeleteView, UserVacancyView

urlpatterns = [
    path('', VacancyView.as_view()),
    path('<int:pk>/', VacancyDetailView.as_view()),
    path('create/', VacancyCreateView.as_view()),
    path('<int:pk>/update/', VacancyUpdateView.as_view()),
    path('<int:pk>/delete/', VacancyDeleteView.as_view()),
    path('by_user/', UserVacancyView.as_view()),
    path('like/', LikeVacancyView.as_view()),
]

