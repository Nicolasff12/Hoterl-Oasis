from django.contrib import admin
from .models import Task
from .models import Huespedes,Personal,Hoteles

admin.site.register(Huespedes)
admin.site.register(Personal)
admin.site.register(Hoteles)

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
  readonly_fields = ('created', )

admin.site.register(Task, TaskAdmin)







