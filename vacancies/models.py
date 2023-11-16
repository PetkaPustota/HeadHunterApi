from django.core.validators import MinValueValidator
from django.db import models
from authentication.models import User
from datetime import date
from django.core.validators import ValidationError

# Create your models here.


def check_data_not_past(value: date):
    if value < date.today():
        raise ValidationError(f"{value}, date is not now")


class Skills(models.Model):
    skill = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.slug


class Vacancies(models.Model):
    STATUS = [
        ("draft", "Черновик"),
        ("open", "Открыта"),
        ("closed", "Закрыта")
    ]

    slug = models.SlugField(max_length=50)
    text = models.CharField(max_length=2000)
    status = models.CharField(max_length=6, choices=STATUS, default="draft")
    created = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    skill = models.ManyToManyField(Skills)

    likes = models.IntegerField(default=0)
    min_experience = models.IntegerField(null=True, validators=[MinValueValidator(0)])
    updated_at = models.DateField(null=True, validators=[check_data_not_past])

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

    def __str__(self):
        return self.slug

    @property
    def username(self):
        return self.user.username if self.user else None
