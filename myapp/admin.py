from django.contrib import admin

# Register your models here.

from django.contrib import admin
from myapp.models import Pac

# Register your models here.
class PacAdmin(admin.ModelAdmin):
    list_display=('id','time')
    ordering = ('-id',)


admin.site.register(Pac,PacAdmin)

