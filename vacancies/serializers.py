from rest_framework import serializers, routers
from rest_framework.validators import UniqueValidator

from vacancies.models import Vacancies, Skills
from django.contrib.auth.models import User


class VacancyStatusValidator:
    def __init__(self, statuses):
        if not isinstance(statuses, list):
            statuses = [statuses]
        self.statuses = statuses

    def __call__(self, value):
        if value in self.statuses:
            raise serializers.ValidationError("Incorrect status.")


class VacancySerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)

    skill = serializers.SlugRelatedField(
        slug_field="skill",
        many=True,
        read_only=True
    )

    class Meta:
        model = Vacancies
        fields = ["id", "text", "slug", "status", "created", "skill", "user", "username", "min_experience"]


class VacancyCreateSerializer(serializers.ModelSerializer):
    skill = serializers.SlugRelatedField(
        required=False,
        queryset=Skills.objects.all(),
        many=True,
        slug_field="skill"
    )
    id = serializers.IntegerField(required=False)
    slug = serializers.CharField(max_length=50, validators=[UniqueValidator(queryset=Vacancies.objects.all())])
    status = serializers.CharField(max_length=6, validators=[VacancyStatusValidator('closed')])

    class Meta:
        model = Vacancies
        fields = "__all__"

    def is_valid(self, raise_exception=False):
        self._skills = self.initial_data.pop("skill", [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        vacancy = Vacancies.objects.create(**validated_data)

        for skill in self._skills:
            skill_obj, _ = Skills.objects.get_or_create(skill=skill)
            vacancy.skill.add(skill_obj)

        vacancy.save()
        return vacancy


class VacancyUpdateSerializer(serializers.ModelSerializer):
    skill = serializers.SlugRelatedField(
        required=False,
        queryset=Skills.objects.all(),
        many=True,
        slug_field="skill"
    )

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created = serializers.DateField(read_only=True)

    class Meta:
        model = Vacancies
        fields = ["id", "text", "status", "slug", "skill", "user", "created"]

    def is_valid(self, raise_exception=False):
        self._skills = self.initial_data.pop("skill")
        return super().is_valid(raise_exception=raise_exception)

    def save(self, validated_data):
        vacancy = super().save()

        for skill in self._skills:
            skill_obj, _ = Skills.objects.get_or_create(skill=skill)
            vacancy.skill.add(skill_obj)

        vacancy.save()
        return vacancy


class VacancyDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)

    skill = serializers.SlugRelatedField(
        slug_field="skill",
        many=True,
        read_only=True
    )

    class Meta:
        model = Vacancies
        fields = "__all__"


class VacancyDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancies
        fields = ["id"]


class SkillListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = "__all__"

