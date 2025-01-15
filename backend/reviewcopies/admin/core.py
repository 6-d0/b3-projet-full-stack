import reviewcopies.models.core as models
from django.contrib import admin


@admin.register(models.Branch)
class BranchAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Session)
class SessionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Registration)
class RegistrationAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Timeslot)
class TimeslotAdmin(admin.ModelAdmin):
    pass
