from django.contrib import admin

# Register your models here.
from .models import AthleteProfile, Pledge, ProgressUpdate

admin.site.register(AthleteProfile)
admin.site.register(Pledge)
admin.site.register(ProgressUpdate)

