from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import AthleteProfile, Pledge, ProgressUpdate, Badge

admin.site.register(AthleteProfile)
admin.site.register(Pledge)
admin.site.register(ProgressUpdate)
admin.site.register(Badge)
