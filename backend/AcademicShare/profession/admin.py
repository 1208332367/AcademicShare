from django.contrib import admin
from profession.models import profession

class professionAdmin(admin.ModelAdmin):
    list_display = ['ProfessionID', 'name', 'status', 'ctime', 'mtime']
    ordering = ['ctime']

# Register your models here.
admin.site.register(profession, professionAdmin)
