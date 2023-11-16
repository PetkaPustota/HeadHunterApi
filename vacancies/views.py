import json

from django.core.paginator import Paginator
from django.db.models import Count, Avg, F
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, UpdateView, DeleteView, CreateView
from rest_framework import viewsets, serializers
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from head_hunter import settings

from vacancies.models import Vacancies, Skills, User
from vacancies.permissions import VacancyCreatePermission
from vacancies.serializers import VacancySerializer, VacancyCreateSerializer, VacancyUpdateSerializer, \
    VacancyDetailSerializer, VacancyDestroySerializer, SkillListSerializer


# Create your views here.

def hello(request):
    return HttpResponse("Hello world")


@method_decorator(csrf_exempt, name="dispatch")
class VacancyView(ListAPIView):
    queryset = Vacancies.objects.all()
    serializer_class = VacancySerializer

    def get(self, request, *args, **kwargs):
        vacancy_text = request.GET.get("text", None)

        if vacancy_text:
            self.queryset = self.queryset.filter(text__contains=vacancy_text)

        return super().get(request, *args, **kwargs)


class VacancyDetailView(RetrieveAPIView):
    queryset = Vacancies.objects.all()
    serializer_class = VacancyDetailSerializer
    permission_classes = [IsAuthenticated]


@method_decorator(csrf_exempt, name="dispatch")
class VacancyCreateView(CreateAPIView):
    queryset = Vacancies.objects.all()
    serializer_class = VacancyCreateSerializer
    permission_classes = [IsAuthenticated, VacancyCreatePermission]


@method_decorator(csrf_exempt, name="dispatch")
class VacancyUpdateView(UpdateAPIView):
    queryset = Vacancies.objects.all()
    serializer_class = VacancyUpdateSerializer


@method_decorator(csrf_exempt, name="dispatch")
class VacancyDeleteView(DeleteView):
    queryset = Vacancies.objects.all()
    serializer_class = VacancyDestroySerializer


class UserVacancyView(ListView):
    # queryset = User.objects.annotate(vacancy=Count("vacancies"))

    def get(self, request):
        qr_user = User.objects.annotate(vacancy=Count("vacancies"))

        paginator = Paginator(qr_user, settings.TOTAL_ON_LIST)
        page_num = request.GET.get("page")
        page_obj = paginator.get_page(page_num)

        users = []

        for user in page_obj:
            users.append({
                "id": user.id,
                "username": user.username,
                "vacancies": user.vacancy,
            })

        response = {
            "items": users,
            "total": paginator.count,
            "page": paginator.num_pages,
            "avg": qr_user.aggregate(Avg("vacancy"))
        }

        return JsonResponse(response)


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skills.objects.all()
    serializer_class = SkillListSerializer


class LikeVacancyView(UpdateAPIView):
    queryset = Vacancies.objects.all()
    serializer_class = VacancyDetailSerializer

    def put(self, request, *args, **kwargs):
        Vacancies.objects.filter(pk__in=request.data).update(likes=F('likes') + 1)

        return JsonResponse(VacancyDetailSerializer(Vacancies.objects.filter(pk__in=request.data), many=True).data,
                            safe=False)

