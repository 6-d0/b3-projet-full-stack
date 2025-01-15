import re

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.text import slugify
from reviewcopies.models import BaseModel

__all__ = [
    "Branch",
    "Course",
    "Schedule",
    "Session",
    "Registration",
    "Timeslot",
]


def get_unique_slug(instance, name):
    """
    Check if instance.slugify(name) is unique, else try to define
    slugify(name)-incr

    """

    model = instance.__class__
    slug = slugify(name)
    if not model.objects.filter(slug=slug).exists():
        return slug

    slug_expr = rf"^{re.escape(slug)}-([0-9]+)$"

    suffixes = model.objects.filter(slug__regex=slug_expr).values_list(
        "slug", flat=True
    )
    suffixes = [int(re.match(slug_expr).group(1)) for suffix in suffixes]
    suffix = sorted(set(range(1, len(suffixes) + 2)).difference(suffixes))[0]

    slug += f"-{suffix}"
    return slug


class Branch(BaseModel):
    name = models.CharField(unique=True, max_length=250)
    courses = models.ManyToManyField("reviewcopies.Course", related_name="branches")
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = get_unique_slug(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Course(BaseModel):
    name = models.CharField(unique=True, max_length=250)
    teacher = models.ForeignKey(
        "reviewcopies.User", on_delete=models.CASCADE, related_name="courses"
    )
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "teacher"], name="one_course_per_teacher"
            )
        ]

    def save(self, *args, **kwargs):
        self.slug = get_unique_slug(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Schedule(BaseModel):
    date = models.DateField(help_text="Open date for registration")
    can_subscribe = models.BooleanField(help_text="Open/Close registration")
    classroom = models.CharField(
        help_text="Classroom where meeting occurs", blank=True, max_length=50
    )
    can_subscribe_until = models.DateTimeField(
        help_text="Students can subscribe until this date if provided",
        null=True,
        blank=True,
    )
    session = models.ForeignKey(
        "reviewcopies.Session",
        related_name="schedules",
        on_delete=models.CASCADE,
    )

    teacher = models.ForeignKey(
        "reviewcopies.User", related_name="schedules", on_delete=models.CASCADE
    )


class SessionManager(models.Manager):
    def registrables(self):
        return self.filter(
            Q(schedules__can_subscribe=True)
            | (
                ~Q(schedules__can_subscribe_until=None)
                & Q(schedules__can_subscribe_until__gte=timezone.now())
            )
        ).distinct()


class Session(BaseModel):
    name = models.CharField("Session name", unique=True, max_length=250)
    courses = models.ManyToManyField("reviewcopies.Course", related_name="sessions")
    slug = models.SlugField(unique=True, blank=True)
    objects = SessionManager()

    def save(self, *args, **kwargs):
        self.slug = get_unique_slug(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Registration(BaseModel):
    date = models.DateTimeField(
        help_text="Student registration date", auto_now_add=True
    )
    comment = models.TextField(blank=True)
    course = models.ForeignKey(
        "reviewcopies.Course", related_name="registrations", on_delete=models.CASCADE
    )
    student = models.ForeignKey(
        "reviewcopies.User", related_name="registrations", on_delete=models.CASCADE
    )
    slot = models.OneToOneField(
        "reviewcopies.Timeslot", related_name="registration", on_delete=models.CASCADE
    )

    def validate_unique(self, *args, **kwargs):
        super().validate_unique(*args, **kwargs)
        if Registration.objects.filter(
            course=self.course,
            student=self.student,
            slot__schedule__session=self.slot.schedule.session,
        ).exists():
            raise ValidationError(
                "A student can't subscribe twice in a course of a same session"
            )


class Timeslot(BaseModel):
    schedule = models.ForeignKey(
        "reviewcopies.Schedule", on_delete=models.CASCADE, related_name="slots"
    )
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
